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
    do_continue = True
    counter = 0
    driver.get('http://www.f150ecoboost.net/forum/68-2016-ford-f150-ecoboost-chat')
    driver.find_element_by_xpath('''//*[@id="yui-gen11"]''').click()

    while do_continue:
        posts = driver.find_elements_by_class_name('threadtitle')
        for post in posts:
            print(post.text)

        try:
            driver.find_element_by_xpath('''//*[@id="yui-gen11"]/span[10]/a/img''').click()
            print('I am here')
            time.sleep(2)
        except:
            do_continue = False




    '''
    while do_continue:
        for review in driver.find_elements_by_xpath('//*[@id="yui-gen9"]/span[2]/a').click():
            title = review.find_element_by_class_name('threadtitle').text
            counter += 1
            #views = review.find_element_by_class_name('threadstats td alt').get_attribute('Views')
            #replies = review.find_element_by_xpath('threadstats td alt').get_attribute('Replies')
            print(counter)

        try:
            driver.find_element_by_link_text('Next').click()
        except:
            do_continue = False
    '''


if __name__ == '__main__':
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    driver.quit()

