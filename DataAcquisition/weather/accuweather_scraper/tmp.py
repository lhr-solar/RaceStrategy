import requests
import time
import urllib.request
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

#function returns a dictionary where the keys relate to weather attributes
#keys: chances, status, visibility, UV_index, pressure, humidity, wind, now, sun_rise, and temp

def weather_data():
    weather = {}
    url = 'https://weather.com/weather/today/l/a9e8362791a8366662d2f306c08fc5496d43c98ec529f1044339f09454cc23a9'
    req = Request('https://weather.com/weather/today/l/a9e8362791a8366662d2f306c08fc5496d43c98ec529f1044339f09454cc23a9',headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read() # need this line to overrun mod security
    soup = BeautifulSoup(page, 'html.parser')
    name = soup.find("span", attrs={'class': "_-_-components-src-organism-TodayDetailsCard-TodayDetailsCard--feelsLikeTempValue--2icPt"})
    srise = soup.find("p", attrs={'class': "_-_-components-src-molecule-SunriseSunset-SunriseSunset--dateValue--3H780"})
    now = soup.find("span", attrs={'data-testid': "TemperatureValue"})
    wind = soup.find("span", attrs={'class': "_-_-components-src-atom-WeatherData-Wind-Wind--windWrapper--3Ly7c undefined"})
    humidity = soup.find("span", attrs={'data-testid': "PercentageValue"})
    dew_point = soup.find("span", attrs={'data-testid': "TemperatureValue"})
    pressure = soup.find("span", attrs={'data-testid': "PressureValue"})
    UV_index = soup.find("span", attrs={'data-testid': "UVIndexValue"})
    visibility = soup.find("span", attrs={'data-testid': "VisibilityValue"})
    chances = soup.find("div", attrs={'class': "_-_-components-src-organism-CurrentConditions-CurrentConditions--precipValue--2aJSf"})
    status = soup.find("div", attrs={'data-testid': "wxPhrase"})
    status = status.text.strip()
    weather['status'] = status;
    if chances != None:
        chances = chances.text.strip()
        weather['chances'] = chances
    visibility = visibility.text.strip()
    weather['visibility'] = visibility
    UV_index = UV_index.text.strip()
    weather['UV_index'] = UV_index
    pressure = pressure.text.strip()
    weather['pressure'] = pressure
    humidity = humidity.text.strip()
    weather['humidity'] = humidity
    wind = wind.text.strip()
    weather['wind'] = wind
    now = now.text.strip()
    weather['now'] = now
    sun_rise = srise.text.strip()
    weather['sun_rise'] = sun_rise
    temp = name.text.strip()
    weather['temp'] = temp
    print(f'The weather on the racetrack is {now} but the weather feels like {temp}. The wind is blowing at {wind} while visibility and humidity are at {visibility} and {humidity} respectively. Pressure today is at {pressure} and the UV index is at a {UV_index}')
    return(weather)


if __name__ == '__main__':
    weather_data()