import requests
from bs4 import BeautifulSoup
from datetime import datetime

CKSMH_URL = 'https://www.cksmh.gov.tw/activitysoonlist_369'  # 中正紀念堂展館
MoCATaipeiURL = 'https://www.mocataipei.org.tw/tw/ExhibitionAndEvent/Exhibitions/Current%20Exhibition'  # 當代藝術館

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
            PictureLinkTmp = Soup.select(f'#fontsize > div:nth-child(3) > ul > li:nth-child({i+1}) > dl > dt > a > span > img')
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


    # 當代藝術館
    Response = requests.get(MoCATaipeiURL)
    Soup = BeautifulSoup(Response.content, "html.parser")

    # 從 HTML 抓取資訊
    Titles = Soup.find_all('h3', class_='imgTitle')  # 展名
    Years = Soup.find_all('span', class_='year')
    Dates = Soup.find_all('p', class_='day')
    ExihibitionList = []
    URL = 'https://www.mocataipei.org.tw/tw/ExhibitionAndEvent/Info'

    for i in range(len(Titles)):
        Title = Titles[i].text
        StartMonth = Dates[(i + 1) * 2 - 1].text.split(' ')
        EndMonth = Dates[(i + 1) * 2].text.split(' ')
        # print(StartMonth)
        # print(EndMonth)
        StartDate = f'{Years[i * 2 - 2].text}/{StartMonth[0]}/{StartMonth[2]}'
        EndDate = f'{Years[i * 2 - 1].text}/{EndMonth[0]}/{EndMonth[2]}'
        Dict = {
            'Title': Title,  # 展名
            'StartDate': StartDate,  # 起始日
            'EndDate': EndDate,  # 結束日
            'Time': '10:00~18:00',  # 時間
            'Location': '當代藝術館',  # 地點
            'ExhibitionLink': f'{URL}/{Title}',  # 連結
        }
        ExihibitionList.append(Dict)

    return ExihibitionList
