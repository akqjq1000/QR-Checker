import os
import sys
import pandas as pd
import numpy as np
import joblib

# 머신러닝 알고리즘
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
# from lightgbm import LGBMClassifier # 필요시 추가 가능

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# schema.py에 정의된 피처 순서를 가져옴
from modules.schema import FEATURE_ORDER

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
try:
    from schema import FEATURE_ORDER
except ImportError:
    print("schema.py를 찾을 수 없습니다. 경로를 확인해주세요.")
    # 임시 우회 (실제 실행 시에는 지워주세요)
    FEATURE_ORDER = ['len_url', 'len_sub_domain', 'len_root_domain', 'len_suffix', 'len_encoding', 'len_query', 'count_sub_domain', 'count_file_path', 'count_special_char', 'count_url_dots', 'is_ip', 'is_private', 'is_filter', 'num_port', 'ratio_alpha_numeric', 'value_entropy_url']

def main():
    data_path = 'data/train_urls.csv'
    model_dir = 'models'
    
    # 1. 데이터 로드 (더미 데이터 생성 로직은 생략하고 실제 데이터가 있다고 가정)
    if not os.path.exists(data_path):
        print(f"오류: {data_path} 파일이 없습니다. 데이터를 먼저 준비해 주세요.")
        return
        
    print("1. 데이터를 로드하고 분할합니다...")
    df = pd.read_csv(data_path)
    
    # 타겟 컬럼명은 실제 환경에 맞게 'label' 또는 'is_malicious' 등으로 맞춰주세요.
    X = df[FEATURE_ORDER]
    y = df['label'] 
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # ==========================================
    # 2. 비교할 모델 정의 (원하는 모델을 얼마든지 추가/수정 가능)
    # ==========================================
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        "XGBoost": xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss', max_depth=6, learning_rate=0.1, n_estimators=100, random_state=42, use_label_encoder=False)
        # "LightGBM": LGBMClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    }
    
    results = []
    os.makedirs(model_dir, exist_ok=True)
    
    print("\n2. 모델 학습 및 평가를 시작합니다...\n")
    
    # 3. 모델 순차적 학습 및 평가
    for model_name, model in models.items():
        print(f"[{model_name}] 학습 중...")
        model.fit(X_train, y_train)
        
        # 예측 수행
        y_pred = model.predict(X_test)
        
        # 성능 지표 계산
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        # 결과 저장
        results.append({
            "Model": model_name,
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1-Score": f1
        })
        
        # 개별 모델 파일로 저장 (예: RandomForest_classifier.pkl)
        save_path = os.path.join(model_dir, f"{model_name}_classifier.pkl")
        joblib.dump(model, save_path)
        print(f"  -> 저장 완료: {save_path}\n")

    # 4. 최종 결과 비교 표 출력
    print("3. [ 최종 모델 성능 비교 ]")
    results_df = pd.DataFrame(results).set_index("Model")
    print(results_df.to_string())
    print("\n학습 프로세스가 모두 종료되었습니다.")

if __name__ == "__main__":
    main()