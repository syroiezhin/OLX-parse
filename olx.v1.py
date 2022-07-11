import requests
from bs4 import BeautifulSoup
import csv
# import pandas as pd

# I won't use it, of course, but I'll leave it here for you ^____^
# https://www.olx.ua/api/v1/offers/
main_url = 'https://www.olx.ua/list/' 

def write_csv(results):
    
    '''  
    # do using PANDAS library :
	print(result)
	df = pd.DataFrame(result)
	df.to_csv('result.csv', index=False, encoding='utf-8-sig') # for mac os
	with open('result.csv', "r") as f: print(f) # to find out the encoding we print
 	'''
    
    # do using CSV library :
    with open('olx_v1.csv', 'w', encoding='utf-8-sig') as f:
        # print(f) # to find out the encoding we print
        writer = csv.writer(f, delimiter=';')
        for item in results:
            writer.writerow( (item['name'],
						  	  item['price'],
						  	  item['address'],
						  	  item['url']
						  	 ))

def clean(text):
	return text.replace('\t','').replace('\n','').strip()

def get_page_data(page_url):
	reque = requests.get(page_url)
	soups = BeautifulSoup(reque.content, features="lxml")
	table = soups.find('table', {'id':'offers_table'})
	rows = table.find_all('tr' , {'class':'wrap'})
	
	result = []
	for row in rows:
		name = clean(row.find('h3').text)
		url = row.find('h3').find('a').get('href')
		price = clean(row.find('p', {'class':'price'}).text) # error occurs here : price may not be!
		bottom = row.find('td', {'valign':'bottom'})
		address= clean(bottom.find('small' , {'class':'breadcrumb x-normal'}).text)
		item = {'name':name,'price':price, 'address':address, 'url': url}
		result.append(item)
	return result

def main(main_url):
    req = requests.get(main_url)
    soup = BeautifulSoup(req.content, features="lxml")
    max_page = int(clean(soup.find('div', {'class':'pager rel clr'}).find_all('span', {'class':'item fleft'})[-1].text))
    result = []
    
    for i in range(1,max_page + 1):
        page_url = main_url + '?page=' + str(i)
        print(f'Parsing page #{i} of {max_page} : {page_url}')
        result += get_page_data(page_url)
    write_csv(result)
	
if __name__ == '__main__':      
	main(main_url)
