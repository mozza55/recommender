import pandas as pd
import requests
import json
import math
import numpy as np
import random

category = pd.read_csv('category.csv')

"""
df = pd.read_csv('shop.csv')
#유니크 벨류 세기
pd.value_counts(df['업종코드'].str.get(i=0))
df
#새로운 컬럼 추가
df['code'] = np.nan

# pandas 반복문
for i in df.index:
    code = df['업종코드'][i]
    for j in category.index:
        if code == category['code'][j]:
            df['code'][i] = category['code'][j]
            break

df.info()

hasnotCode = df[df['code'].isnull()]
hasnotCode.shape

hasCode = df[df['code'].notnull()]
pd.value_counts(hasCode['업종코드'].str.get(i=0))

# 인덱스 리셋
# drop=True 옵션 ; 인덱스를 컬럼에 추가하지 않는다
# pandas dataframe to csv
# index=False 옵션 ; 인덱스를 컬럼에 추가하지 않는다
stores = hasCode.reset_index(drop=True)
stores.to_csv('filtering_stores.csv',index=False)

"""

stores = pd.read_csv('filtering_stores.csv')
pd.value_counts(stores['업종코드'].str.get(i=0))
stores.columns

gangnam = stores[stores['시군구명']=='강남구']
print(gangnam.shape)
pd.value_counts(gangnam['업종코드'].str.get(i=0))
print(pd.value_counts(gangnam['code']))

# 상권 구분 테이블
area = pd.read_csv('area.csv')
area.head()

stores = gangnam
stores['y'] = np.nan
stores['x'] = np.nan
headers = {
    'Authorization': 'KakaoAK a8e53fbbc3a4e197e7b7ce41ed995517',
}
for i in stores.index:
    WGS_y = stores['위도'][i]
    WGS_x = stores['경도'][i]
    params = (
        ('x', WGS_x),
        ('y', WGS_y),
        ('input_coord', 'WGS84'),
        ('output_coord', 'WTM'),
    )
    response = requests.get('https://dapi.kakao.com/v2/local/geo/transcoord.json', headers=headers, params=params)
    j = json.loads(response.text)
    WTM_y = j.get("documents")[0].get("y")
    WTM_x = j.get("documents")[0].get("x")
    stores['y'][i]=WTM_y
    stores['x'][i]=WTM_x
###stores.to_csv('filtering_gangnam.csv')

stores['area_code'] = np.nan
for i in stores.index:
    MIN = 99999999
    index = -1
    for j in area.index:
        if(stores['행정동코드'][i]/100 == area['행정동_코드'][j]):
            x = area['x'][j]
            y = area['y'][j]
            temp =math.pow(stores['x'][i]-x,2) +math.pow(stores['y'][i]-y,2)
            if temp<MIN:
                index = j
                MIN  = temp
        elif (stores['행정동코드'][i]/100 < area['행정동_코드'][j]):
            break
    if index == -1:
        stores['area_code'][i]  = np.nan
    else :
        stores['area_code'][i] = area['상권_코드'][index]
stores[['상호명','area_code']]

stores[stores['area_code'].isnull()]
temp = stores[stores['area_code'].notnull()]
temp = temp.reset_index(drop =True)
print(temp)
##temp.to_csv('gangnam.csv',index=False)

stores = pd.read_csv('gangnam.csv')

### 인구 데이터

### 주위 상권 직장 인구 데이터
area_work = pd.read_csv('area_work_pop.csv')
side_work = pd.read_csv('areaside_work_pop.csv')

### 가장 최신 자료만 이용
"""
area_work = area_work[area_work['기준_년월_코드']==2019]
area_work.to_csv('area_work_pop.csv',index=False)
side_work = side_work[side_work['기준_년_코드']==2019]
side_work.to_csv('areaside_work_pop.csv',index=False)
"""

area_work.columns = ['year','quarter','quarter_code','area_class','area_code','area_name',
                    'total_pop','total_m','total_w','total_10','total_20','total_30','total_40','total_50','total_60',
                    'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60']
side_work.columns = ['year','quarter','quarter_code','area_class','area_code','area_name',
                    'total_pop','total_m','total_w','total_10','total_20','total_30','total_40','total_50','total_60',
                    'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60']

# pandas 데이터 프레임 컬럼만 생성
workers = pd.DataFrame(columns=('area_code','total_pop','total_m','total_w','total_10','total_20','total_30',
                               'total_40','total_50','total_60'))

workers['area_code'] =area['상권_코드']
# 값에 따라 오름차순 정렬
workers = workers.sort_values(['area_code'], ascending=True).reset_index(drop=True)
# 컬럼을 인덱스로 사용
workers  = workers.set_index('area_code')

area_work  = area_work.sort_values(['area_code']).reset_index(drop=True)
area_work = area_work.set_index('area_code')
area_work = area_work.drop(['year','quarter','quarter_code','area_class','area_name', 'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60'],axis=1)

side_work = side_work.sort_values(['area_code']).reset_index(drop=True)
side_work =side_work.set_index('area_code')
side_work = side_work.drop(['year','quarter','quarter_code','area_class','area_name', 'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60'],axis=1)

# 상권 직장 인구수 통계
for i in area_work.index:
    workers.loc[i] = area_work.loc[i]
for i in side_work.index:
    workers.loc[i] = workers.loc[i] + side_work.loc[i]

workers.info()


### 상권 거주 인구 데이터
area_live = pd.read_csv('area_live_pop.csv')
side_live = pd.read_csv('areaside_live_pop.csv')

### 가장 최신 자료만 이용

area_live = area_live[area_live['기준_년_코드']==2019]
area_live.to_csv('area_live_pop.csv',index=False)
side_live = side_live[side_live['기준_년_코드']==2019]
side_live.to_csv('areaside_live_pop.csv',index=False)

area_live.columns = ['year','quarter','quarter_code','area_class','area_code','area_name',
                    'total_pop','total_m','total_w','total_10','total_20','total_30','total_40','total_50','total_60',
                    'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60',
                     'total_family','apt_family','non_apt_family']
side_live.columns = ['year','quarter','quarter_code','area_class','area_code','area_name',
                    'total_pop','total_m','total_w','total_10','total_20','total_30','total_40','total_50','total_60',
                    'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60',
                    'total_family','apt_family','non_apt_family']

# pandas 데이터 프레임 컬럼만 생성
residents = pd.DataFrame(columns=('area_code','total_pop','total_m','total_w','total_10','total_20','total_30',
                               'total_40','total_50','total_60'))
residents.columns

residents['area_code'] =area['상권_코드']
# 값에 따라 오름차순 정렬
residents = residents.sort_values(['area_code'], ascending=True).reset_index(drop=True)
# 컬럼을 인덱스로 사용
residents  = residents.set_index('area_code')

area_live  = area_live.sort_values(['area_code']).reset_index(drop=True)
area_live = area_live.set_index('area_code')
area_live = area_live.drop(['year','quarter','quarter_code','area_class','area_name', 'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60','total_family','apt_family','non_apt_family'],axis=1)

side_live = side_live.sort_values(['area_code']).reset_index(drop=True)
side_live =side_live.set_index('area_code')
side_live = side_live.drop(['year','quarter','quarter_code','area_class','area_name', 'm_10','m_20','m_30', 'm_40', 'm_50', 'm_60', 'w_10', 'w_20', 'w_30', 'w_40', 'w_50', 'w_60','total_family','apt_family','non_apt_family'],axis=1)

# 상권 거주 인구수 통계
for i in area_live.index:
    residents.loc[i] = area_live.loc[i]
for i in side_live.index:
    residents.loc[i] = residents.loc[i] + side_live.loc[i]

residents.info()

### 거주 + 직장 인구 데이터

# NaN 결측 데이터 채우기
population = residents.fillna(value=0) + workers.fillna(value=0)
print(population.info())
population['workers'] = workers['total_pop'].fillna(0)
population['residents'] = residents['total_pop'].fillna(0)
population



### 인플루언서 타겟 데이터 생성

influencers = pd.read_csv('influencer.csv')

# 데이터 프레임 여러개의 컬럼 추가하기
# pd.concat
# sort = False  컬럼들을 정렬하지 않음
influencers = pd.concat([influencers,pd.DataFrame(columns =('target_m','target_w','target_10','target_20','target_30','target_40','target_50','target_60'))],sort=False)
influencers

# 랜덤값 생성
# randrange(1,100) ; 1 이상 100 미만의 난수 생성
x=random.randrange(1,100)
y = 100-x
print(x,y)