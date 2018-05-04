## Goal: get the thread that is top 100 popular: by views, by replies
## Write function to sort by reviews or replies
## .csv file to contain: link_to_thread, name_of_thread, views, replies, last_post_time, last_post_date




import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 3)
    return driver


def lookup(driver):
    post_dict = {'link': [], 'title': [], 'stats': [], 'last_post_stats': []}
    driver.get('http://www.f150ecoboost.net/forum/68-2016-ford-f150-ecoboost-chat')
    #driver.get('http://www.f150ecoboost.net/forum/42-2015-ford-f150-ecoboost-chat')
    counter1 = 0

    while True:
        try:
            driver.find_element_by_xpath('''//*[@id="yui-gen11"]''').click()
            posts = driver.find_elements_by_xpath('''.//*[@id='threads']''')
            for post in posts:
                titles = post.find_elements_by_xpath('''//a[@class='title']''')
                for title in titles:
                    # print(title.text)
                    post_dict['title'].append(title.text)
                    # print(title.get_attribute('href'))
                    post_dict['link'].append(title.get_attribute('href'))
                subs_stats = post.find_elements_by_xpath('''.//*[@class='threadstats td alt']''')
                for sub_stats in subs_stats:
                    # print(sub_stats.text)
                    if sub_stats.text != '&nbsp;':
                        post_dict['stats'].append(sub_stats.text)
                subs_dates = post.find_elements_by_xpath('''.//*[@class='threadlastpost td']''')
                for sub_dates in subs_dates:
                    # print(sub_dates.text)
                    if sub_dates.text != '&nbsp;':
                        post_dict['last_post_stats'].append(sub_dates.text)
                counter1 += 1
            print(counter1)
            print(driver.current_url)
            page = driver.find_element_by_xpath('''//img[@alt='Next']''')
            page.click()
        except:
            return post_dict


def process_df(post_dict):
    post_dict['last_post_datetime'] = (post_dict.last_post_stats.apply(lambda x:x.split('\n'))).str[1]
    post_dict['Last_post_date'] = (post_dict.last_post_datetime.str.split(', ')).str[0]
    post_dict['Last_post_time'] = (post_dict.last_post_datetime.str.split(', ')).str[1]

    post_dict['repliesViews'] = post_dict.stats.apply(lambda x: x.replace(',',''))
    post_dict['counts'] = post_dict.repliesViews.apply(lambda x:[int(s) for s in x.split() if s.isdigit()])
    post_dict['Replies'] = post_dict.counts.str[0]
    post_dict['Views'] = post_dict.counts.str[1]
    post_dict.drop(['last_post_stats', 'stats', 'last_post_datetime', 'repliesViews', 'counts'], axis=1, inplace=True)

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
    data = pd.DataFrame.from_dict(data)
    data = process_df(data)
    sorted_data = sort_values_by(data, ['Replies', 'Views'], [False, False])
    #another use-case below:
    #another = sorted_data.groupby('Last_post_date').apply(pd.DataFrame.sort_values, 'Replies')
    sorted_data.to_csv('Top100_Posts.csv')