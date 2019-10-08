import surprise
import pandas as pd
import numpy as np
import random
from surprise.model_selection import KFold
from surprise import Reader
from surprise.model_selection import cross_validate
from collections import defaultdict
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

influencers = pd.read_csv('influencer.csv')
influencers['id'] = np.nan
for i in influencers.index:
    influencers['id'][i] = 20000000 + i
#컬럼 순서 변경
cols = influencers.columns.tolist()
cols = cols[-1:] + cols[:-1]
influencers  = influencers[cols]
influencers

ratings = pd.DataFrame(columns=['store_id','influencer_id','rating'])
ratings


##ratings
count =0
for i in range(0,1000):
    for j in influencers.index:
        ratings.loc[count]= [stores['id'][i], influencers['id'][j], random.randrange(1,10)]
        count += 1
ratings = pd.read_csv('ratings.csv')
df_table = ratings.set_index(['store_id','influencer_id']).unstack()
df_table.shape

reader = Reader(rating_scale=(1,10))
data = surprise_test.Dataset.load_from_df(ratings, reader)


bsl_options ={
    'method' : 'als',
    'n_epochs' : 5,
    'reg_u' : 12,
    'reg_i' : 5
}
algo = surprise_test.BaselineOnly(bsl_options)
np.random.seed(0)
acc = np.zeros(3)
cv = KFold(3)
for i , (trainset, testset) in enumerate(cv.split(data)):
    algo.fit(trainset)
    predictions = algo.test(testset)
    acc[i] = surprise_test.accuracy.rmse(predictions, verbose= True)
acc.mean()


def get_Iu(uid):
    """ return the number of items rated by given user
    args:
      uid: the id of the user
    returns:
      the number of items rated by the user
    """
    try:
        return len(trainset.ur[trainset.to_inner_uid(uid)])
    except ValueError:  # user was not part of the trainset
        return 0


def get_Ui(iid):
    """ return number of users that have rated given item
    args:
      iid: the raw id of the item
    returns:
      the number of users that have rated the item.
    """
    try:
        return len(trainset.ir[trainset.to_inner_iid(iid)])
    except ValueError:
        return 0


df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
df['Iu'] = df.uid.apply(get_Iu)
df['Ui'] = df.iid.apply(get_Ui)
df['err'] = abs(df.est - df.rui)
best_predictions = df.sort_values(by='err')[:10]
worst_predictions = df.sort_values(by='err')[-10:]

print(df.head())
print(best_predictions)
print(worst_predictions)


algo.predict(10000000,20000000,verbose= True)

#Mean Squared Difference MSD 평균제곱차이
sim_options ={ 'name': 'msd'}
algo = surprise.KNNBasic(sim_options=sim_options)
cross_validate(algo,data)["test_mae"].mean()
#Cosine 유사도
sim_options = {'name': 'cosine'}
algo = surprise.KNNBasic(sim_options=sim_options)
cross_validate(algo, data)["test_mae"].mean()

#Pearson 유사도
sim_options = {'name': 'pearson'}
algo = surprise.KNNBasic(sim_options=sim_options)
cross_validate(algo, data)["test_mae"].mean()

#Pearson-Baseline Similarity
sim_options = {'name': 'pearson_baseline'}
algo = surprise.KNNBasic(sim_options=sim_options)
cross_validate(algo, data)["test_mae"].mean()

sim_options = {'name': 'pearson_baseline'}
algo = surprise.KNNWithMeans(sim_options=sim_options)
cross_validate(algo, data)["test_mae"].mean()

sim_options = {'name': 'pearson_baseline'}
algo = surprise.KNNBaseline(sim_options=sim_options)
cross_validate(algo, data)["test_mae"].mean()

def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

top_n = get_top_n(predictions,n=10)
print(top_n)
