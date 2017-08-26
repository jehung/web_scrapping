## Goal: get the thread that is top 100 popular: by views, by replies
## Write function to sort by reviews or replies
## .csv file to contain: link_to_thread, name_of_thread, views, replies, last_post_time, last_post_date
## TODO: convert lastpost date/time to datetime


import time
import datetime
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

    while page_number==1:
        try:
            link = driver.find_element_by_link_text(str(page_number))
        except NoSuchElementException:
            break

        posts = driver.find_elements_by_xpath('''.//*[@class='rating0 nonsticky']''')
        for post in posts:
            title = post.find_element_by_xpath('''.//a[@class='title']''')
            print(title.text)
            post_dict['title'].append(title.text)
            print(title.get_attribute('href'))
            post_dict['link'].append(title.get_attribute('href'))
            #print(post.find_element_by_css_selector('a').get_attribute('href'))
            #post_dict['link'].append(post.find_element_by_css_selector('a').get_attribute('href'))
            #print(post.text)
            #post_dict['title'].append(post.find_element_by_xpath('''.//a[@class='title']''').text)
            print(post.find_element_by_xpath('''.//*[@class='threadstats td alt']''').text)
            post_dict['stats'].append(post.find_element_by_xpath('''.//*[@class='threadstats td alt']''').text)
            print(post.find_element_by_xpath('''.//*[@class='threadlastpost td']''').text)
            post_dict['last_post_date'].append(post.find_element_by_xpath('''.//*[@class='threadlastpost td']''').text)
            counter1 += 1
        print(counter1)




        link.click()
        print(driver.current_url)
        page_number += 1

    return post_dict


def process_df(post_dict):
    post_dict['Last_post_date'] = post_dict.last_post_stats.apply(lambda x: (x.split(',')[0]).split('\n')[1])
    post_dict['Last_post_time'] = post_dict.last_post_stats.apply(lambda x: x.split(',')[1])
    post_dict['Replies'] = post_dict.stats.apply(lambda x: int((x.split('\n')[0]).split(':')[1].replace(',', '')))
    post_dict['Views'] = post_dict.stats.apply(lambda x: int(((x.split('\n')[1]).split(': ')[1]).replace(',', '')))
    post_dict.drop(['last_post_stats', 'stats'], axis=1, inplace=True)

    return post_dict


def sort_values_by(df, by, ascending):
    sorted_df = df.sort_values(by=by, ascending=ascending)
    return sorted_df


if __name__ == '__main__':
    driver = init_driver()
    data = lookup(driver)
    time.sleep(5)
    driver.quit()


    for e in data:
        print(e)
        print(len(data[e]))
    #data = pd.DataFrame(data.items())#, columns=['link', 'title', 'stats', 'last_post_date'])
    data = pd.DataFrame.from_dict(data)
    data = process_df(data)
    print(data.head())