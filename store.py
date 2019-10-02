import pandas as pd
import requests
import json
import math
import numpy as np

category = pd.read_csv('category.csv')


### 소상공인 데이터에서 등록된 카테고리에 포함하는 데이터만 필터링
'''
df = pd.read_csv('shop.csv')
print(pd.value_counts(df['업종코드'].str.get(i=0)))

df['code'] = np.nan
# pandas 반복문
for i in df.index:
    code = df['업종코드'][i]
    for j in category.index:
        if code == category['code'][j]:
            df['code'][i] = category['code'][j]
            break

print(df.info())
hasnotCode = df[df['code'].isnull()]
print(hasnotCode.shape)

hasCode = df[df['code'].notnull()]
print(pd.value_counts(hasCode['업종코드'].str.get(i=0)))

# 인덱스 리셋
# drop=True 옵션 ; 인덱스를 컬럼에 추가하지 않는다
# pandas dataframe to csv
# index=False 옵션 ; 인덱스를 컬럼에 추가하지 않는다
stores = hasCode.reset_index(drop=True)
stores.to_csv('filtering_stores.csv',index=False)
'''

stores = pd.read_csv('filtering_stores.csv')
print(stores)