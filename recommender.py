import pandas as pd
import requests
import json
import math
import numpy as np

area = pd.read_csv('area.csv')
area.columns=['area_level','area_level_name','area_code','area_name','x','y','sigungu_code','dong_code','','date']

print(area)

headers = {
    'Authorization': 'KakaoAK a8e53fbbc3a4e197e7b7ce41ed995517',
}
data ={
    'query' : '서울 강남구 선릉로93길 26'
}

response = requests.get('https://dapi.kakao.com/v2/local/search/address.json', headers=headers,data=data)
##response.text
j = json.loads(response.text)
print(j)

print(j.get("documents")[0].get("road_address"))
WGS_y=j.get("documents")[0].get("road_address").get('y')
WGS_x=j.get("documents")[0].get("road_address").get('x')
print('y : '+WGS_y +", x : "+WGS_x)


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
print(j)
print(WTM_y)
print(WTM_x)

# 올림 내림 처리 ?

MIN = 999999
index = -1
for i in area.index:
    x = area.get_value(i,'x')
    y = area.get_value(i,'y')
    temp =math.pow(WTM_x-x,2) +math.pow(WTM_y-y,2)
    if temp<MIN:
        index = i
        MIN  = temp
print(index)

loc = area[index:index+1]
print(loc)
print(loc.shape)
num = area['area_code'][index]
print(num)

# 상권 인구 데이터
# 가장 최신년도 최근 분기 데이터만 사용
##
area_work_pop = pd.read_csv('area_work_Pop.csv')
area_work_pop.columns=['year','quater','area_level','area_level_name','area_code','area_code_name',
                       'total_worker_pop','ml_worker_pop','fml_worker_pop','age_10_pop','age_20_pop',
                      'age_30_pop','age_40_pop','age_50_pop','age_60_pop','mage_10_pop','mage_20_pop',
                       'mage_30_pop','mage_40_pop','mage_50_pop','mage_60_pop', 'fmage_10_pop',
                       'fmage_20_pop','fmage_30_pop','fmage_40_pop','fmage_50_pop','fmage_60_pop']
print(area_work_pop)

print(area_work_pop[area_work_pop.area_code==num])

target = area_work_pop[area_work_pop.area_code==num]
print(target)
area_work_pop[area_work_pop.area_code==num]

# .iloc[행번호] {결과 데이터에서 차례대로 }
#  .loc[인덱스번호]
target= target.iloc[0]
print(target)

print(target.age_60_pop)
print(target[0])

# 출력 print('포맷 {0}  {1}'.format( , ....))
# 반올림 round( {값}, {표현할 자리수})
print('여성: {0}'.format(round(target.fml_worker_pop/target.total_worker_pop*100,1)))
print('남성:',round(target.ml_worker_pop/target.total_worker_pop*100,1))

print('여성')
print('10대 {0}'.format(round(target.fmage_10_pop/target.fml_worker_pop*100,1)))
print('20대 {0}'.format(round(target.fmage_20_pop/target.fml_worker_pop*100,1)))
print('30대 {0}'.format(round(target.fmage_30_pop/target.fml_worker_pop*100,1)))
print('40대 {0}'.format(round(target.fmage_40_pop/target.fml_worker_pop*100,1)))
print('50대 {0}'.format(round(target.fmage_50_pop/target.fml_worker_pop*100,1)))
print('60대 이상{0}'.format(round(target.fmage_60_pop/target.fml_worker_pop*100,1)))

temp = 100/target.ml_worker_pop

print('남성')
for i in range(1,7):
    print('{0}대 {1}'.format(i*10,round(target[14+i]*temp,1)))

#### 소상공인협회에서 제공하는 상가 정보로 가게 데이터 입력
## 서울시에서 제공하는 카테고리로 분류 할 것이기 때문에
## 카테고리 매핑을 해야함

## xrld  패키지 설치되어있어야함

mapping = pd.read_excel('mapping.xlsx',skiprows=[0])

# fillna NaN 값을 다른 값으로 대치
# method = 'ffill''  : 앞의 값으로 nan 대치   vs  'bfil'  : 뒤의 값으로 nan 대치
mapping = mapping.fillna(method='ffill')
print(mapping)

# 필요 없는 column 삭제
mapping = mapping.drop(['세세분류코드','세세분류코드명','세분류코드명','소분류코드명','중분류코드명',
                       '대분류코드명','대분류코드','대분류코드명.1','중분류코드','중분류코드명.1'],1)
mapping.columns= ['대분류', '중분류', '소분류코드', '소분류']
print(mapping)

stores = pd.read_csv('stores_temp.csv')

stores = stores[stores['시도코드'] ==11]
stores = stores[0:1000]
stores = stores[0:180]
print(stores)

stores['area_code'] = np.nan
stores['y'] = np.nan
stores['x'] = np.nan
stores['target_m']=np.nan
stores['target_w'] = np.nan
stores['target_10'] = np.nan
stores['target_20'] = np.nan
stores['target_30'] = np.nan
stores['target_40'] = np.nan
stores['target_50'] = np.nan
stores['target_60'] = np.nan


for i in stores.index:
    WGS_y = stores.get_value(i,'위도')
    WGS_x = stores.get_value(i,'경도')
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
    MIN = 99999999
    index = -1
    for j in area.index:
        x = area.get_value(j,'x')
        y = area.get_value(j,'y')
        temp =math.pow(WTM_x-x,2) +math.pow(WTM_y-y,2)
        if temp<MIN:
            index = j
            MIN  = temp
    stores['area_code'][i] = area['area_code'][index]
print("#############################")
print(stores[['상호명','area_code']])


for i in stores.index:
    #print(stores['area_code'][i])
    target = area_work_pop[area_work_pop.area_code==stores['area_code'][i]]
    if target.shape[0] !=0:
        target = target.iloc[0]
        stores['target_m'][i] =round(target.ml_worker_pop/target.total_worker_pop*100,1)
        stores['target_w'][i] = round(target.fml_worker_pop/target.total_worker_pop*100,1)
        stores['target_10'][i] =round(target.age_10_pop/target.total_worker_pop*100,1)
        stores['target_20'][i] =round(target.age_20_pop/target.total_worker_pop*100,1)
        stores['target_30'][i] =round(target.age_30_pop/target.total_worker_pop*100,1)
        stores['target_40'][i] =round(target.age_40_pop/target.total_worker_pop*100,1)
        stores['target_50'][i] =round(target.age_50_pop/target.total_worker_pop*100,1)
        stores['target_60'][i] =round(target.age_60_pop/target.total_worker_pop*100,1)

stores= stores.dropna(subset=['target_m'])
stores[['area_code','target_m','target_w','target_10','target_20','target_30','target_40','target_50','target_60']]

influencer= stores[80:]
influencer =influencer.reset_index()
store=stores[:100]
store = store.reset_index()

ratings= pd.DataFrame(columns=['store_id','influencer_id','rating','gender','s_gender_m','i_gender_m','age'])
count = 0
for i in store.index:
    for j in influencer.index:
        rating = 0
        # 카테고리
        if store['소분류코드'][i] == influencer['소분류코드'][j]:
            rating = rating + 3
        elif store['중분류코드'][i] == influencer['중분류코드'][j]:
            rating = rating + 2
        elif store['대분류코드'][i] == influencer['대분류코드'][j]:
            rating = rating + 1
        # 지역
        if store['행정동코드'][i] == influencer['행정동코드'][j]:
            rating = rating + 3
        elif store['시군구코드'][i] == influencer['시군구코드'][j]:
            rating = rating + 2
        elif store['시도코드'][i] == influencer['시도코드'][j]:
            rating = rating + 1
        # 성별
        gender = 1 - math.pow(store['target_m'][i] - influencer['target_m'][j], 2) / 1000
        rating = rating + gender * 2
        # 연령
        age = math.pow(store['target_10'][i] - influencer['target_10'][j], 2)
        age = age + math.pow(store['target_20'][i] - influencer['target_20'][j], 2)
        age = age + math.pow(store['target_30'][i] - influencer['target_30'][j], 2)
        age = age + math.pow(store['target_40'][i] - influencer['target_40'][j], 2)
        age = age + math.pow(store['target_50'][i] - influencer['target_50'][j], 2)
        age = age + math.pow(store['target_60'][i] - influencer['target_60'][j], 2)
        age = 1 - math.sqrt(age) / 100
        rating = rating + age * 2
        ratings.loc[count] = [store['id'][i], influencer['id'][j], rating, gender, store['target_m'][i],
                              influencer['target_m'][j], age]
        count = count + 1
print(ratings)
temr= ratings[ratings['store_id'] == 20261400]
temr = temr.sort_values(by='rating',ascending=False)
print(temr)
#동일가게 rating 10




