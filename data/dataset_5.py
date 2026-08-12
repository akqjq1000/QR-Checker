import pandas as pd

# dataset_5 불러오기
df5 = pd.read_csv('phishing_url_dataset_unique.csv')

# 필요한 컬럼만 선택
df5 = df5[['url', 'label']]

# label 통일
df5['label'] = df5['label'].map({
    1: 'bad',
    0: 'good'
})

# 결과 확인
print(df5.head())

print("\n컬럼명:")
print(df5.columns.tolist())

print("\n라벨 개수:")
print(df5['label'].value_counts())

# 표준화된 dataset_5 CSV 저장
df5.to_csv(
    'dataset_5.csv',
    index=False,
    encoding='utf-8-sig'
)

print("\ndataset_5.csv 생성 완료")


import os

file_name = 'dataset_5.csv'

print("파일 존재:", os.path.exists(file_name))
print("파일 경로:", os.path.abspath(file_name))
print("파일 크기:", os.path.getsize(file_name))

check_df = pd.read_csv(file_name)

print(check_df.head())
print(check_df.shape)
print(check_df.columns.tolist())