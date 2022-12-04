from datetime import datetime
from ExhibitionMongo import InitMongo

db = InitMongo()
db.exhibitions.insert_one({
    "Title": "共識覺",
    "StartDate": datetime.strptime("2022/11/05", '%Y/%m/%d'),
    "EndDate": datetime.strptime("2022/01/29", '%Y/%m/%d'),
    "Time": "10:00~18:00",
    "Location": "當代藝術館",
    "ExhibitionLink": "https://www.mocataipei.org.tw/tw/ExhibitionAndEvent/Info/共識覺"
})
