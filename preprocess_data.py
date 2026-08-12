import os
import pandas as pd
import numpy as np
import re
import math
from urllib.parse import urlparse

# ==========================================
# 1. 피처 추출 함수 정의
# ==========================================
def calculate_entropy(text):
    """문자열의 엔트로피(복잡도)를 계산합니다."""
    if not text:
        return 0.0
    entropy = 0
    for x in set(text):
        p_x = float(text.count(x)) / len(text)
        entropy += - p_x * math.log(p_x, 2)
    return float(entropy)

def extract_features_from_url(url):
    """단일 URL 문자열에서 16개의 피처를 추출하여 딕셔너리로 반환합니다."""
    url = str(url).strip()
    len_url = len(url)
    
    # 💡 악성 URL의 기형적인 문자열(예: 닫히지 않은 괄호)로 인한 파싱 오류 방지 로직
    try:
        parsed_url = urlparse(url if url.startswith('http') else 'http://' + url)
        domain = parsed_url.netloc
        path = parsed_url.path
        query = parsed_url.query
        # 포트 번호가 비정상적인 문자로 되어 있을 경우를 대비한 추가 예외 처리
        try:
            port = parsed_url.port
        except ValueError:
            port = -1
    except ValueError:
        # urlparse가 완전히 실패할 경우 문자열 기반으로 강제 분리
        clean_url = url.replace('http://', '').replace('https://', '')
        domain = clean_url.split('/')[0]
        path = '/' + '/'.join(clean_url.split('/')[1:]) if '/' in clean_url else ''
        query = ''
        port = -1
        
    # 도메인 분리
    parts = domain.split('.')
    if len(parts) > 2:
        sub_domain = '.'.join(parts[:-2])
        root_domain = parts[-2]
        suffix = parts[-1]
    elif len(parts) == 2:
        sub_domain = ''
        root_domain = parts[0]
        suffix = parts[1]
    else:
        sub_domain = ''
        root_domain = domain
        suffix = ''
        
    # --- 길이 관련 ---
    len_sub_domain = len(sub_domain)
    len_root_domain = len(root_domain)
    len_suffix = len(suffix)
    len_encoding = len(re.findall(r'%[0-9a-fA-F]{2}', url)) * 3
    len_query = len(query)
    
    # --- 개수 관련 ---
    count_sub_domain = len(sub_domain.split('.')) if sub_domain else 0
    count_file_path = path.count('/')
    count_special_char = len(re.findall(r'[^a-zA-Z0-9]', url))
    count_url_dots = url.count('.')
    
    # --- 구조적 특징 ---
    # IPv4 정규식 매칭
    is_ip = 1 if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', domain.split(':')[0]) else 0
    is_private = 1 if is_ip and (domain.startswith('192.168.') or domain.startswith('10.') or domain.startswith('172.')) else 0
    
    filter_words = ['login', 'verify', 'bank', 'secure', 'account', 'update']
    is_filter = 1 if any(word in url.lower() for word in filter_words) else 0
    
    num_port = port if port else -1
    
    # --- 비율/복잡도 ---
    alnum_count = len(re.findall(r'[a-zA-Z0-9]', url))
    ratio_alpha_numeric = alnum_count / len_url if len_url > 0 else 0.0
    value_entropy_url = calculate_entropy(url)

    return {
        'len_url': int(len_url),
        'len_sub_domain': int(len_sub_domain),
        'len_root_domain': int(len_root_domain),
        'len_suffix': int(len_suffix),
        'len_encoding': int(len_encoding),
        'len_query': int(len_query),
        'count_sub_domain': int(count_sub_domain),
        'count_file_path': int(count_file_path),
        'count_special_char': int(count_special_char),
        'count_url_dots': int(count_url_dots),
        'is_ip': int(is_ip),
        'is_private': int(is_private),
        'is_filter': int(is_filter),
        'num_port': int(num_port),
        'ratio_alpha_numeric': float(ratio_alpha_numeric),
        'value_entropy_url': float(value_entropy_url)
    }

# ==========================================
# 2. 메인 실행 로직
# ==========================================
def main():
    raw_data_path = 'data/data.csv'
    output_data_path = 'data/train_urls.csv'
    
    if not os.path.exists(raw_data_path):
        print(f"오류: {raw_data_path} 파일이 존재하지 않습니다.")
        return
        
    print(f"1. [{raw_data_path}]에서 원본 데이터를 불러옵니다...")
    df_raw = pd.read_csv(raw_data_path)
    
    # 2. 각 URL에 대해 피처 추출 함수 적용
    print("2. 16개의 피처를 추출하여 전처리를 진행합니다. (데이터 양에 따라 시간이 소요될 수 있습니다)")
    features_list = df_raw['url'].apply(extract_features_from_url).tolist()
    
    # 3. 추출된 딕셔너리 리스트를 새로운 데이터프레임으로 변환
    df_features = pd.DataFrame(features_list)
    
    # 4. 정답(Label) 맵핑 (bad -> 1:악성, good -> 0:정상)
    df_features['label'] = df_raw['label'].map({'bad': 1, 'good': 0})
    
    # 5. CSV 파일로 저장
    os.makedirs('data', exist_ok=True)
    df_features.to_csv(output_data_path, index=False)
    
    print(f"\n✅ 전처리 완료! 총 {len(df_features)}개의 데이터가 [{output_data_path}]에 성공적으로 저장되었습니다.")
    print("   이제 'python train_compare.py'를 실행하여 모델을 훈련하실 수 있습니다.")

if __name__ == "__main__":
    main()