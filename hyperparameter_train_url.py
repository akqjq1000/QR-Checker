import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

# 추출된 피처 데이터 불러오기
df = pd.read_csv('train_urls_feature.csv')

# X / y 분리
X = df.drop('label', axis=1)
y = df['label']

#  학습 / 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Random Forest 기본 모델
rf_base = RandomForestClassifier(
    n_estimators=100,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

rf_base.fit(X_train, y_train)
rf_base_pred = rf_base.predict(X_test)

print("\n===== Random Forest 기본 모델 =====")
print(
    classification_report(
        y_test,
        rf_base_pred,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)

# Random Forest 튜닝 모델
rf_tuned = RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

rf_tuned.fit(X_train, y_train)
rf_tuned_pred = rf_tuned.predict(X_test)

print("\n===== Random Forest 튜닝 모델 =====")
print(
    classification_report(
        y_test,
        rf_tuned_pred,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)
# Random Forest 튜닝 모델
rf_tuned = RandomForestClassifier(
    n_estimators=200,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

rf_tuned.fit(X_train, y_train)
rf_tuned_pred = rf_tuned.predict(X_test)

print("\n===== Random Forest 튜닝 모델 =====")
print(
    classification_report(
        y_test,
        rf_tuned_pred,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)

# XGBoost 기본 모델
xgb_base = XGBClassifier(
    random_state=42,
    n_jobs=-1,
    eval_metric='logloss'
)

xgb_base.fit(X_train, y_train)
xgb_base_pred = xgb_base.predict(X_test)

print("\n===== XGBoost 기본 모델 =====")
print(
    classification_report(
        y_test,
        xgb_base_pred,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)

# XGBoost 튜닝
xgb_tuned1 = XGBClassifier(
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

xgb_tuned1.fit(X_train, y_train)
xgb_tuned1_pred = xgb_tuned1.predict(X_test)

print("\n===== XGBoost 1차 튜닝 =====")
print(
    classification_report(
        y_test,
        xgb_tuned1_pred,
        labels=[1, 0],
        target_names=['악성', '정상']
    )
)