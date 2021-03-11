import requests
from peewee import *
from datetime import datetime

#id，城市名字，，温度，湿度，time
url="https://wis.qq.com/weather/common?source=pc&weather_type=observe%7Cforecast_1h%7Cforecast_24h%7Cindex%7Calarm%7Climit%7Ctips%7Crise&province=江苏&city=苏州&county=常熟"
r=requests.get(url)
r.encoding='utf-8'
weather_json=r.json()

# for key, value in weather_json.items():
#     print("\nKey: " + repr(key))
#     print("Value: " + repr(value))

data=weather_json['data']['observe']

city_name="常熟"
degree=data['degree']
humidity=data['humidity']
pressure=data['pressure']
weather=data['weather']
update_time=data['update_time']

print(degree+"度",weather,update_time)



db = MySQLDatabase('test',host ='127.0.0.1',user='root',passwd='123456',charset='utf8',port=3306,);

class Weather(Model):
    degree=IntegerField()
    humidity=IntegerField()
    pressure=IntegerField()
    weather=CharField()
    update_time = DateTimeField()
    city_name=CharField()

    class Meta:
        database = db # This model uses the "people.db" database.


time=datetime.strptime(update_time,"%Y%m%d%H%M")

print(time)
weather_today=Weather(degree=degree,city_name=city_name,humidity=humidity,pressure=pressure,weather=weather,update_time=time)
weather_today.save()
