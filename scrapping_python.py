## Goal: get the thread that is top 100 popular: by views, by replies

## Write function to sort by reviews or replies


import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
 
 
def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 3)
    return driver
 
 
def lookup(driver):
    driver.get('http://www.f150ecoboost.net/forum/42-2015-ford-f150-ecoboost-chat')
    raw = driver.page_source
    #jsonD = json.dumps(raw)
    print(raw)
	
	
    '''
	elem=driver.find_element_by_tag_name('threadlist')
    content=elem.text
    print(content)
    #j=json.loads(content)
    '''
	
if __name__ == '__main__':
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    driver.quit()
	
	


#pip install git+https://github.com/robotframework/Selenium2Library.git


//*[@id="thread_16095"]/div/div/div/h3

//*[@id="thread_inlinemod_form"]/div[1]/div/div/span[1]