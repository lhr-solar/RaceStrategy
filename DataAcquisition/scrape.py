from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox(executable_path="/Users/rohitneppalli/Downloads/geckodriver")
driver.get("https://weather.com/")
city = "Dallas"

driver.find_element_by_class_name("input__inputElement__1GjGE").click()
driver.find_element_by_class_name("input__inputElement__1GjGE").send_keys(city)
time.sleep(2)
driver.find_element_by_class_name("input__inputElement__1GjGE").send_keys(Keys.DOWN)
driver.find_element_by_class_name("input__inputElement__1GjGE").send_keys(Keys.ENTER)

previousURL = driver.current_url
WebDriverWait(driver, 15).until(EC.url_changes(previousURL))

url = str(driver.current_url)
url = url.replace("today", "hourbyhour")

request = requests.get(url)

soup = BeautifulSoup(request.text, 'html.parser')
rows = soup.find_all('tr', attrs={'class': 'clickable'})
classes = ['description', 'temp', 'feels', 'precip', 'humidity', 'wind']

for row in rows:
    row_soup = BeautifulSoup(str(row), 'html.parser')
    tds = row_soup('td')

    for c in classes:
        elem = row_soup.find('td', attrs={'class': c})
        if elem is not None:
            print(elem.text, end='\t')
    print("\n")

driver.close()