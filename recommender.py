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