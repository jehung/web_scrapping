## Goal: get the thread that is top 100 popular: by views, by replies
## Write function to sort by reviews or replies
## .csv file to contain: link_to_thread, name_of_thread, views, replies, last_post_time, last_post_date
## TODO: convert lastpost date/time to datetime


import time
import pandas as pd
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
    post_dict =  {'link':[], 'title':[], 'stats':[], 'last_post_date':[]}
    driver.get('http://www.f150ecoboost.net/forum/68-2016-ford-f150-ecoboost-chat')
    driver.find_element_by_xpath('''//*[@id="yui-gen11"]''').click()
    counter1 = 0
    counter2 = 0
    counter3 = 0
    page_number = 1

    while True==1:
        try:
            link = driver.find_element_by_link_text(str(page_number))
        except NoSuchElementException:
            break

        posts = driver.find_elements_by_class_name('threadtitle')
        for post in posts:
            #print(post.find_element_by_css_selector('a').get_attribute('href'))
            post_dict['link'].append(post.find_element_by_css_selector('a').get_attribute('href'))
            #print(post.text)
            post_dict['title'].append(post.text)
            counter1 += 1
        print(counter1)



        #stats_h = driver.find_elements_by_xpath('''//*[@class='threadstats td']''')
        post_dict['stats'].append(driver.find_elements_by_xpath('''//*[@class='threadstats td']'''))
        counter2 += 1
        stats = driver.find_elements_by_xpath('''//*[@class='threadstats td alt']''')
        for stat in stats:
            #print(stat.text)
            post_dict['stats'].append(stat.text)
            counter2 += 1
        print(counter2)

        postdates = driver.find_elements_by_xpath('''//*[@class='threadlastpost td']''')
        for postdate in postdates:
            #print(postdate.text)
            post_dict['last_post_date'].append(postdate.text.split(','))
            counter3 += 1
        print(counter3)

        link.click()
        print(driver.current_url)
        page_number += 1

    return post_dict


if __name__ == '__main__':
    driver = init_driver()
    data = lookup(driver)
    time.sleep(5)
    driver.quit()


    for e in data:
        print(e)
        print(len(data[e]))
    data = pd.DataFrame(data.items())#, columns=['link', 'title', 'stats', 'last_post_date'])
    #data = pd.DataFrame.from_dict(data)
    print(data.head())