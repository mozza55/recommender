#유하 사이트에서 youtuber 정보 긁어오기
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

#빈 데이터 프레임 생성
df = pd.DataFrame(columns=['category','channel','followers','views','comments','cost'])

#selenium
driver = webdriver.Chrome('chromedriver')
delay =3
driver.implicitly_wait(delay)
driver.get('https://www.youha.info/login/')
# PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
#driver = webdriver.PhantomJS('phantomjs-2.1.1-macosx/bin/phantomjs')
#id, password  값 입
driver.find_element_by_name('username').send_keys('id')
driver.find_element_by_name('password').send_keys('password')
driver.find_element_by_xpath('/html/body/div/form/div[1]/input[2]').click()

driver.get('https://www.youha.info/')
html=driver.page_source
soup = BeautifulSoup(html,'html.parser')
category = list()
for i in soup.find('div',class_='categoryMenu showMenu').find_all('a'):
    if i.get('style')!=None:
        continue
    category.append([i.get('href'),i.text.strip()])

del category[0] #필요없는 카테고리 제거
print(category)

idx =0
for cate in category:
    driver.get('https://www.youha.info{0}'.format(cate[0]))
    cate_name = cate[1]
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    count=1
    for i in soup.select('body > div > div.fit > div > div > a '):
        count +=1
    driver.implicitly_wait(delay)
    for i in range(2,3):
        driver.get('https://www.youha.info{0}?page={1}'.format(cate[0],i))
        driver.implicitly_wait(delay)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        for channel in soup.select('body > div > div.fit > form > div.scroll > table > tbody > tr '):
            channelname = channel.select(' td:nth-child(4) > a ')
            followers = channel.select('td:nth-child(5) ')
            views = channel.select('td:nth-child(6)')
            comments =  channel.select('td:nth-child(7)')
            cost =  channel.select('td:nth-child(8)')
            if channel.find('td') :
                #print(channelname[0].text.strip())
                #print(followers[0].text.strip())
                #print(views[0].text.strip()+' ' +comments[0].text.strip() +' ' + cost[0].text.strip())
                #데이터 프레임에 row 행 추가
                df.loc[idx] = [cate_name,channelname[0].text.strip(), followers[0].text.strip(), views[0].text.strip(),
                              comments[0].text.strip(),cost[0].text.strip() ]
                idx +=1
        driver.implicitly_wait(delay+2)
print(df)

#df.to_csv('influencer.csv')



