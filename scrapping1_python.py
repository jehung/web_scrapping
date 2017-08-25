## Goal: get the thread that is top 100 popular: by views, by replies
## Write function to sort by reviews or replies
## .csv file to contain: link_to_thread, name_of_thread, views, replies, last_post_time, last_post_date



import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException



def init_driver():
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, 3)
    return driver


def lookup(driver):
    do_continue = True
    counter = 0
    driver.get('http://www.f150ecoboost.net/forum/68-2016-ford-f150-ecoboost-chat')
    driver.find_element_by_xpath('''//*[@id="yui-gen11"]''').click()

    page_number = 1

    while True:
        try:
            link = driver.find_element_by_link_text(str(page_number))
        except NoSuchElementException:
            break

        posts = driver.find_elements_by_class_name('threadtitle')
        for post in posts:
            print(post.find_element_by_css_selector('a').get_attribute('href'))
            print(post.text)

            #stats = post.find_element_by_xpath('''//*[@class='threadstats td alt']''')
            #for stat in stats:
            #print(stats.text)

        stats = driver.find_elements_by_xpath('''//*[@class='threadstats td alt']''')
        for stat in stats:
            print(stat.text)

            counter += 1
        link.click()
        print(driver.current_url)
        page_number += 1
    print(counter)


if __name__ == '__main__':
    driver = init_driver()
    lookup(driver)
    time.sleep(5)
    driver.quit()

