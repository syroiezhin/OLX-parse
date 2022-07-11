from bs4 import BeautifulSoup
import requests
import csv

main_url = 'https://www.olx.ua/list/'
# main_url = 'https://www.olx.ua/moda-i-stil/'

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
    price = clean(row.find('p', {'class':'price'}).text).replace(' грн.', '').replace('Бесплатно', '')
  except:
    price = ""
  return price

def write_csv(result):
  array_url = []
  with open('olx_v2.csv', 'w', encoding='utf-8-sig') as f:  
    writer = csv.writer(f, delimiter=';')
    for item in result:
      writer.writerow( (
        item['url'],
        item['name'],
        item['address'],
        item['price']))
      array_url.append(item['url'])
  return array_url

def parserPhone(url):
  print(f'\n{url}')
  
if __name__== '__main__':
  array_result = main(main_url)
  array_url = write_csv(array_result)
  parserPhone(array_url)