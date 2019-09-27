import pandas as pd
import requests
import json
import math

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

stores = pd.read_csv('stores.csv')

stores = stores[stores['시도코드'] ==11]
stores = stores[0:1000]
print(stores)