import surprise
import pandas as pd
import numpy as np
import random
#소수점 표기
pd.options.display.float_format = '{:.0f}'.format

stores = pd.read_csv('gangnam.csv')
stores = stores.drop(['code'],axis=1)
stores.columns = ['id', 'store_name', 'code', 'code_name', 'city', 'sigungu_code', 'sigungu', 'dong_code',
                 'dong', 'jibun1', 'jibun2', 'addr', 'lon', 'lat', 'y', 'x','area_code']
for i in stores.index:
    stores['id'][i] = 10000000 +i
stores

stores = pd.read_csv('gangnam.csv')
stores = stores.drop(['code'],axis=1)
stores.columns = ['id', 'store_name', 'code', 'code_name', 'city', 'sigungu_code', 'sigungu', 'dong_code',
                 'dong', 'jibun1', 'jibun2', 'addr', 'lon', 'lat', 'y', 'x','area_code']
for i in stores.index:
    stores['id'][i] = 10000000 +i
stores

ratings = pd.DataFrame(columns=['store_id','influencer_id','rating'])
ratings

count =0
for i in range(0,1000):
    for j in influencers.index:
        ratings.loc[count]= [stores['id'][i], influencers['id'][j], random.randrange(1,10)]
        count += 1
ratings