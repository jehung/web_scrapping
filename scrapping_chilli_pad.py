## Goal: get the thread that is top 100 popular: by views, by replies
## Write function to sort by reviews or replies
## .csv file to contain: link_to_thread, name_of_thread, views, replies, last_post_time, last_post_date




import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select




def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 3)
    return driver


def lookup(driver, sd, ed):
    # Log in first
    driver.get('https://chilitechnology.refersion.com/affiliate/conversions')
    user = driver.find_element_by_name("email")
    password = driver.find_element_by_name("password")
    user.clear()
    user.send_keys("mwolla@verticalscope.com")
    password.clear()
    password.send_keys("vScopE2468")
    driver.find_element_by_id("login-btn").click()
    time.sleep(3)

    # Go to conversions
    driver.find_element_by_link_text("Conversions").click()

    # date picker
    datepicker_from = driver.find_element_by_xpath("//input[@name='from']")
    datepicker_from.click()
    time.sleep(2)
    datepicker_from.send_keys(sd)

    datepicker_to = driver.find_element_by_xpath("//input[@name='to']")
    datepicker_to.click()
    datepicker_to.send_keys(ed)

    # choose status from toggle
    select = Select(driver.find_element_by_name('status'))
    select.select_by_visible_text('Approved')

    # submit
    driver.find_element_by_xpath("//input[@type='submit']").click()

    # now get conversion data
    post_dict = {'conversion_id': [], 'datetime': [], 'status': [],
                 'pmt_status':[], 'total_itmes':[], 'curr':[], 'order_total':[],
                 'commission':[]}
    #driver.get('https://chilitechnology.refersion.com/affiliate/conversions')
    counter1 = 0

    has_more = True
    while has_more:
        try:
            button = driver.find_element_by_link_text('Load More')
            button.click()
        except: #href_data is None:
            has_more = False

    rows = driver.find_element_by_xpath('//table[@class="table table-hover table-striped table-bordered"]').find_elements_by_tag_name('tr')
    for row in rows:
        print(row.text)
        if len(row.text) >= 1 and 'Conversion' not in row.text and 'Load' not in row.text:
            cells = row.text.strip().split(' ')
            print(cells)
            post_dict['conversion_id'].append(cells[0])
            datetime = cells[1]+' '+cells[2]+','+cells[3]
            post_dict['datetime'].append(datetime)
            post_dict['status'].append(cells[6])
            post_dict['pmt_status'].append(cells[7])
            post_dict['total_itmes'].append(cells[8])
            post_dict['curr'].append(cells[9])
            post_dict['order_total'].append(cells[10])
            post_dict['commission'].append(cells[11])
            counter1 += 1

    return post_dict


def process_df(post_dict):
    post_dict['date'] = (post_dict.datetime.apply(lambda x:pd.to_datetime(x)))
    post_dict['order_total'] = (post_dict.order_total.str.replace('$', ''))
    post_dict['commission'] = (post_dict.commission.str.replace('$', ''))

    return post_dict



if __name__ == '__main__':
    driver = init_driver()

    data = lookup(driver, '2018-02-01', '2018-05-03')
    print(data)

    time.sleep(5)
    driver.quit()

    for d in data:
        print(d)
        print(len(data[d]))


    data = pd.DataFrame.from_dict(data)
    data = process_df(data)
    data['site]'] = 'thesleepjudge.com'
    sorted_data = data.sort_values('date')
    #another use-case below:
    #another = sorted_data.groupby('Last_post_date').apply(pd.DataFrame.sort_values, 'Replies')
    sorted_data.to_csv('cilli_conversions.csv')
