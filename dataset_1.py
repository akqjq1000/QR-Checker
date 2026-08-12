import pandas as pd

# dataset_1 불러오기
df1 = pd.read_csv('dataset_1.csv')

# 필요한 컬럼만 선택
df1 = df1[['URL', 'label']]

# URL 컬럼명 소문자로 변경
df1 = df1.rename(columns={
    'URL': 'url'
})

# label 통일
df1['label'] = df1['label'].map({
    1: 'good',
    0: 'bad'
})

# 결과 확인
print(df1.head())

print("\n컬럼명:")
print(df1.columns.tolist())

print("\n라벨 개수:")
print(df1['label'].value_counts())