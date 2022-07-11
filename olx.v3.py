'''
Open the commented lines, and run the program. 
These lines are needed to install chromedriver on your macOS. 
In the terminal they will show the url address to your chromedriver.
'''

# from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
# driver = webdriver.Chrome(ChromeDriverManager().install()) 

# the program works for olx.ua and olx.pl
url = "https://www.olx.pl/d/oferta/budmat-venecja-d-matt-wysylka-cala-kraj-letnia-promocja-CID628-IDLZSay.html"
driver = webdriver.Chrome(executable_path="/Users/v.syroiezhin/.wdm/drivers/chromedriver/mac64/103.0.5060.53/chromedriver")

def slp(namber): return time.sleep(namber)

try:
    driver.get(url=url)
    button = driver.find_element_by_id("onetrust-accept-btn-handler").click()
    slp(5) # the pause is necessary for the program to work
    button = driver.find_element_by_class_name("css-65ydbw-BaseStyles").click()
    slp(5) # the pause is necessary for the program to work
    for element in driver.find_elements_by_class_name("css-v1ndtc"):
        print(element.text)
        break
    
except Exception as ex:
    print(ex)
    
finally: 
    driver.close()
    driver.quit()
    