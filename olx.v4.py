from selenium import webdriver
import time



'''functions ⤵ '''

def pause(seconds): 
    return time.sleep(seconds) # a pause is necessary to have time to work out the program code

def click():
    try:    driver.find_element_by_class_name("css-wqpdas-BaseStyles").click() #olx.ua
    except: driver.find_element_by_id("onetrust-accept-btn-handler").click()   #olx.pl
    finally:
        pause(1) 
        button = driver.find_element_by_class_name("css-65ydbw-BaseStyles").click()
        pause(1)

def copyPhone(): 
    for phoneNumber in driver.find_elements_by_class_name("css-v1ndtc"): return phoneNumber.text

def copyName():
    for user in driver.find_elements_by_class_name("css-1rbjef7-Text"): return user.text



'''program logic ⤵ '''

# the program works for olx.ua and olx.pl
url = ['https://www.olx.pl/d/oferta/budmat-venecja-d-matt-wysylka-cala-kraj-letnia-promocja-CID628-IDLZSay.html','https://www.olx.ua/d/obyavlenie/budinok-v-rumun-vlla-shale-poiana-soarelui-ilisesti-IDP1zGk.html']
# a list of product links can be obtained using the olx.v2.py program

driver = webdriver.Chrome(executable_path="/Users/v.syroiezhin/.wdm/drivers/chromedriver/mac64/103.0.5060.53/chromedriver")

try:
    for arrayReferenceNumber in range(0,len(url)):
        driver.get(url=url[arrayReferenceNumber])
        click()
        telephone = copyPhone()
        owner = copyName()
        print(arrayReferenceNumber+1, "/", len(url), "-", owner, "-", telephone, "-", url[arrayReferenceNumber])

except Exception as error: print(error)
finally: 
    driver.close()
    driver.quit()

''' GLORY TO UKRAINE '''