import requests
from bs4 import BeautifulSoup
from datetime import datetime

CKSMH_URL = 'https://www.cksmh.gov.tw/activitysoonlist_369'  # 中正紀念堂展館


def GetExihibitionInfo():
    ExihibitionList = []

    # 中正紀念堂展館
    for Page in range(1, 3):
        URL = f'{CKSMH_URL}_{Page}.html'
        Response = requests.get(URL)
        Soup = BeautifulSoup(Response.content, "html.parser")

        # 從 HTML 抓取內容
        Titles = Soup.find_all('div', class_='h3')            # 展名
        Dates = Soup.find_all('span', class_='date')          # 展期
        Locations = Soup.find_all('span', class_='location')  # 地點

        # 處理資料並存入 dictionary
        for i in range(len(Titles)):
            Title = Titles[i].text
            Date = Dates[i].text
            DateList = Date.replace(' ~ ', '').replace(' ', '').replace('\n', ',').split(',')
            StartDate = datetime.strptime(DateList[2], '%Y/%m/%d')
            EndDate = datetime.strptime(DateList[3], '%Y/%m/%d')
            DateTime = DateList[4]
            Location = Locations[i].text.strip('地點：')
            Link = Soup.find('a', title=Title+'「另開新視窗」').get('href')
            # PictureLinkTmp = Soup.select(f'#fontsize > div:nth-child(3) > ul > li:nth-child({i+1}) > dl > dt > a > span > img')
            ImgLinkTmp = Soup.find('ul', class_='exhibition-list')
            ImgLink = ImgLinkTmp.find('img').get('src')

            Dict = {
                'Title': Title,          # 展名
                'StartDate': StartDate,  # 起始日
                'EndDate': EndDate,      # 結束日
                'Time': DateTime,        # 時間
                'Location': Location,    # 地點
                'ExhibitionLink': Link,  # 連結
                'ImgLink': ImgLink       # 圖片
            }
            ExihibitionList.append(Dict)

    return ExihibitionList
