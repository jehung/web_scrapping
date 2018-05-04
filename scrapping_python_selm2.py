## Goal: get the thread that is top 100 popular: by views, by replies

## Write function to sort by reviews or replies


import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import Selenium2Library
 
 
def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 3)
    return driver
 
 

#pip install git+https://github.com/robotframework/Selenium2Library.git

import Selenium2Library
s = Selenium2Library.Selenium2Library()
s.open_browser('http://www.f150ecoboost.net/forum/42-2015-ford-f150-ecoboost-chat', 'chrome')
source = s.get_source()

jsonD = json.dumps(source)
print(jsonD)
print(type(jsonD))
json.load(jsonD)    
