import pandas as pd

# dataset_5 불러오기
df5 = pd.read_csv('dataset_5.csv')

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
    'df_dataset_5.csv',
    index=False,
    encoding='utf-8-sig'
)

print("\ndf_dataset_5.csv 생성 완료")
