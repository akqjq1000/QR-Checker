# 라이브러리 불러오기
import pandas as pd
import re
import math
import ipaddress
from urllib.parse import urlsplit
from sklearn.model_selection import train_test_split
from collections import Counter
from tqdm.auto import tqdm
import tldextract
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

# CSV 데이터 불러오기 및 기본 정보 확인
file_name = 'data.csv'
df = pd.read_csv(file_name)

# 결측값 제거
df = df.dropna(subset=['url', 'label'])

# URL 및 Label 데이터 전처리
df['url'] = df['url'].astype(str).str.strip()
df['label'] = df['label'].astype(str).str.strip().str.lower()

# Label 숫자 변환 (악성=1, 정상=0)
df['label'] = df['label'].map({
    'good': 0,
    'bad': 1
})

# 변환되지 않은 Label 제거
df = df.dropna(subset=['label'])

# label 충돌 제거
label_count = df.groupby('url')['label'].nunique()
conflict_urls = label_count[label_count > 1].index

df = df[~df['url'].isin(conflict_urls)]

# 중복 URL 제거
df = df.drop_duplicates(subset='url')
df = df.reset_index(drop=True)

# URL 도메인 분석 및 의심 키워드 설정
extractor = tldextract.TLDExtract(
    suffix_list_urls=None
)

suspicious_keywords = [
    'login',
    'signin',
    'verify',
    'verification',
    'secure',
    'security',
    'account',
    'update',
    'confirm',
    'password',
    'bank',
    'wallet',
    'payment',
    'paypal',
    'bonus',
    'recover',
    'support'
]
# URL 엔트로피 계산 함수
def calculate_entropy(text):
    if not text:
        return 0.0

    counts = Counter(text)
    length = len(text)

    entropy = 0.0

    for count in counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy

# URL 피처 추출 함수
def extract_features(url):
    url = str(url).strip()

    # http://, https://가 없는 URL도 분석하기 위해 임시로 추가
    parse_url = url

    if '://' not in parse_url:
        parse_url = 'http://' + parse_url

    try:
        parsed = urlsplit(parse_url)
    except:
        parsed = None

    if parsed:
        hostname = parsed.hostname or ''
        path = parsed.path or ''
        query = parsed.query or ''
    else:
        hostname = ''
        path = ''
        query = ''

    # 도메인 분석
    ext = extractor(hostname)

    subdomain = ext.subdomain or ''
    domain = ext.domain or ''
    suffix = ext.suffix or ''

    if suffix:
        root_domain = domain + '.' + suffix
    else:
        root_domain = domain

    # IP 주소 여부
    try:
        ip_obj = ipaddress.ip_address(hostname)
        is_ip = True
        is_private = ip_obj.is_private
    except:
        is_ip = False
        is_private = False

    # 포트 번호
    try:
        port = parsed.port if parsed and parsed.port else -1
    except:
        port = -1

    # 의심 키워드
    url_lower = url.lower()

    is_filter = any(
        keyword in url_lower
        for keyword in suspicious_keywords
    )
  
    # 알파벳 / 숫자 비율
    alpha_count = sum(char.isalpha() for char in url)
    numeric_count = sum(char.isdigit() for char in url)

    ratio_alpha_numeric = numeric_count / max(alpha_count, 1)
    
    # %20, %2F 같은 URL 인코딩
    encoded_list = re.findall(
        r'%[0-9a-fA-F]{2}',
        url
    )

    # 경로 깊이
    path_parts = [
        part
        for part in path.split('/')
        if part
    ]

    # 서브도메인 개수
    if subdomain:
        count_sub_domain = len(
            [x for x in subdomain.split('.') if x]
        )
    else:
        count_sub_domain = 0

    features = {
        'len_url': len(url),
        'len_sub_domain': len(subdomain),
        'len_root_domain': len(root_domain),
        'len_suffix': len(suffix),
        'len_encoding': len(encoded_list) * 3,
        'len_query': len(query),

        'count_sub_domain': count_sub_domain,
        'count_file_path': len(path_parts),
        'count_special_char': sum(
            not char.isalnum()
            for char in url
        ),
        'count_url_dots': url.count('.'),

        'is_ip': is_ip,
        'is_private': is_private,
        'is_filter': is_filter,
        'num_port': port,

        'ratio_alpha_numeric': ratio_alpha_numeric,
        'value_entropy_url': calculate_entropy(url)
    }
    return features

# 전체 URL에서 피처 추출
tqdm.pandas()

feature_list = df['url'].progress_apply(
    extract_features
)

features_df = pd.DataFrame(
    feature_list.tolist()
)

# 학습용 데이터 생성 및 CSV 저장
train_urls = features_df.copy()
train_urls['label'] = df['label'].values

train_urls.to_csv(
    'train_urls_feature.csv',
    index=False
)

# 입력 데이터(X)와 정답 데이터(y) 분리
X = train_urls.drop(
    'label',
    axis=1
)

y = train_urls['label']

# 학습 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Random Forest 기본 모델 학습
rf_model = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

rf_model.fit(
    X_train,
    y_train
)

y_pred = rf_model.predict(
    X_test
)

# Random Forest 기본 모델 성능 평가
print("===== Random Forest 기본 모델 =====")
print(
    classification_report(
        y_test,
        y_pred,
        labels=[1, 0],
        target_names=[
            '악성',
            '정상'
        ]
    )
)

#  Random Forest 하이퍼파라미터 튜닝
rf_model = RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

y_pred_tuned = rf_model.predict(X_test)

# Random Forest 튜닝 모델 성능 평가
print("===== Random Forest 튜닝 결과 =====")
print(
    classification_report(
        y_test,
        y_pred_tuned,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)

# XGBoost 기본 모델 학습
xgb_base = XGBClassifier(
    random_state=42,
    n_jobs=-1,
    eval_metric='logloss'
)

xgb_base.fit(X_train, y_train)
xgb_base_pred = xgb_base.predict(X_test)

print("===== XGBoost 기본 모델 =====")
print(
    classification_report(
        y_test,
        xgb_base_pred,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)

# XGBoost 1차 튜닝 모델 학습
xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    min_child_weight=2,
    subsample=0.8,
    colsample_bytree=0.8,
    gamma=0.1,
    random_state=42,
    n_jobs=-1,
    eval_metric='logloss'
)

xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)

# XGBoost 튜닝 모델 성능 평가
print("===== XGBoost 튜닝 결과 =====")
print(
    classification_report(
        y_test,
        xgb_pred,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)
