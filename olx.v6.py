from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import math
import csv

main_url = 'https://www.olx.ua/list/'
lastTimeInSecond = 0

def funcTime():
  global lastTimeInSecond
  nowTimeInSecond = int(round(time.time()))
  if lastTimeInSecond != 0: 
    h = math.floor((nowTimeInSecond - lastTimeInSecond)/3600)
    m = math.floor((nowTimeInSecond - lastTimeInSecond - 3600*h)/60)
    s = (nowTimeInSecond - lastTimeInSecond - 3600*h - 60*m)
    text = f"{h}h:{m}m:{s}s"
    return text
  lastTimeInSecond = nowTimeInSecond
  return "0h:0m:0s"

def main(main_url):
  soup = BeautifulSoup(requests.get(main_url).content, features="lxml")
  max_page = int(clean(soup.find('div', {'class':'pager rel clr'}).find_all('span', {'class':'item fleft'})[-1].text))
  result = []
  
  for i in range(1, max_page + 1):
    page_url = main_url + '?page=' + str(i)
    print(f'Parsing page #{i} of {max_page} : {page_url}')
    result += get_page_data(page_url)
  return result
  
def get_page_data(page_url):
  soup = BeautifulSoup(requests.get(page_url).content, features="lxml")
  rows = soup.find('table', {'id':'offers_table'}).find_all('tr' , {'class':'wrap'})
  result = []

  for row in rows:
    url = row.find('h3').find('a').get('href')
    name = clean(row.find('h3').text)
    address = clean(row.find('td', {'valign':'bottom'}).find('small' , {'class':'breadcrumb x-normal'}).text)
    price = priceSearch(row)
    
    item = {'name':name, 'address':address, 'price':price, 'url':url}
    result.append(item)
  return result

def clean(text):
	return text.replace('\t','').replace('\n','').strip()

def priceSearch(row):
  try:
    price = clean(row.find('p', {'class':'price'}).text).replace(' грн.', '')
  except:
    price = ""
  return price

def write_csv(result):
  array_url = []
  with open('olx_v6.csv', 'w', encoding='utf-8-sig') as f:  
    writer = csv.writer(f, delimiter=';')
    for item in result:
      writer.writerow( (
        item['url'],
        item['name'],
        item['address'],
        item['price']))
      array_url.append(item['url'])
  return array_url

def pause(seconds): 
    return time.sleep(seconds) # a pause is necessary to have time to work out the program code

def authorization():
  
  option = webdriver.ChromeOptions()
  option.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
  option.add_argument("--disable-blink-features=AutomationControlled")
  option.headless = True
  driver = webdriver.Chrome(executable_path="/Users/v.syroiezhin/.wdm/drivers/chromedriver/mac64/103.0.5060.53/chromedriver", options=option)
  driver.get(url="https://www.olx.ua/account/")
  driver.find_element_by_class_name("cookiesBarClose").click()
  driver.find_element_by_id("userEmail").send_keys("login@gmail.com")
  driver.find_element_by_id("userPass").send_keys("password")
  driver.find_element_by_id("se_userLogin").click()
  pause(2)
  return driver

def copyName(driver):
  for user in driver.find_elements_by_class_name("css-1rbjef7-Text"): break
  return user.text

def copyPhone(driver):
  pause(5) # waiting for the "Show phone" button to appear 
  try:
    try: driver.find_element_by_class_name("css-65ydbw-BaseStyles").click() # button "Show phone"
    except: driver.find_element_by_class_name("css-1p9kuvm-BaseStyles").click() # button "Show phone"
    finally:
      pause(5)
      for phoneNumber in driver.find_elements_by_class_name("css-v1ndtc"): break
      return phoneNumber.text
  except: return "None"

def parserPhone(driver,array_url):
  try: 
    for arrayReferenceNumber in range(0,len(array_url)): 
      driver.get(url=array_url[arrayReferenceNumber])
      print(funcTime(), " ", arrayReferenceNumber+1, "/", len(array_url), "-", copyName(driver), "-", copyPhone(driver), "-", array_url[arrayReferenceNumber])
  
  except Exception as error: print(error)
  finally: 
    driver.close()
    driver.quit()

if __name__== '__main__':
  array_result = main(main_url)
  array_url = write_csv(array_result)
  driver = authorization()
  parserPhone(driver,array_url)

''' GLORY TO UKRAINE '''
# interrupt program execution ctrl + C