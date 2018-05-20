## Goal: get the thread that is top 100 popular: by views, by replies
## Write function to sort by reviews or replies
## .csv file to contain: link_to_thread, name_of_thread, views, replies, last_post_time, last_post_date




import time
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select




def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 3)
    return driver


def lookup_commissions(driver, sd, ed):
    # Log in first
    driver.get('https://www.slumbercloud.com/affiliates/account/login/')


    user = driver.find_element_by_xpath("//input[@placeholder='Email Address']")
    password = driver.find_element_by_xpath("//input[@placeholder='Password']")
    user.clear()
    user.send_keys("mwolla@verticalscope.com")
    password.clear()
    password.send_keys("pIZeO8ec#3ld")
    driver.find_element_by_xpath("//button[@id='send2']").click()

    # Go to conversions
    driver.find_element_by_link_text("Commissions").click()

    # date picker
    datepicker_from = driver.find_element_by_xpath("//input[@name='created_time-from']")
    datepicker_from.click()

    datepicker_from.send_keys(sd)

    datepicker_to = driver.find_element_by_xpath("//input[@name='created_time-to']")
    datepicker_to.click()
    datepicker_to.send_keys(ed)

    # submit
    driver.find_element_by_xpath("//div[@class='affiliateplus-search-button']/button[2]").click()

    # now get conversion data
    post_dict = {'number':[], 'date': [], 'product_name': [], 'total_amount': [],
                 'commission':[], 'status':[]}

    total_items = driver.find_element_by_class_name("amount").text.strip().split(' ')[-2]
    print(total_items)


    #10 per page
    total_pages = int(int(total_items)/10)+1
    for p in range(1, int(total_pages)+1):
        if p == 1:
            pass
        else:
            try:
                driver.find_element_by_link_text(str(p)).click()
            except:
                pass

        rows = driver.find_element_by_xpath(
            '//table[@class="table table-bordered table-hover no-margin"]').find_elements_by_tag_name('tr')
        for i in range(len(rows)):
            #print(rows[i].text)
            cells = rows[i].text.strip().split(' ')
            if len(cells) >= 3 and 'No.' not in rows[i].text:
                #meta =rows[i].find_element_by_xpath('.//*[@data-toggle="table"]').get_attribute('data-original-title')
                #print(meta)
                print(cells)
                #post_dict['reason'].append(meta)
                post_dict['number'].append(cells[0])
                datetime = cells[1]+' '+cells[2]+','+cells[3]
                post_dict['date'].append(datetime)
                post_dict['total_amount'].append(cells[-3])
                post_dict['commission'].append(cells[-2])
                post_dict['status'].append(cells[-1])
                cells.pop(0)
                cells.pop(1)
                cells.pop(2)
                cells.pop(3)
                cells.pop(-1)
                cells.pop(-2)
                cells.pop(-3)
                post_dict['product_name'].append(' '.join(cells))



    return post_dict



def lookup_traffics(driver, sd, ed):
    driver.find_element_by_link_text("Traffics").click()
    # now get traffics data
    post_dict = {'traffic_source':[], 'clicks': [], 'uniuqe_clicks': [], 'store_view': [],
                 'landing_page':[]}

    total_items = driver.find_element_by_class_name("amount").text.strip().split(' ')[-2]
    print(total_items)


    #10 per page
    total_pages = int(int(total_items)/10)+1
    for p in range(1, int(total_pages)+1):
        if p == 1:
            pass
        else:
            #driver.get('https://www.slumbercloud.com/affiliates/index/listTransaction/?limit=10&p='+str(p))
            driver.find_element_by_link_text(str(p)).click()

        rows = driver.find_element_by_xpath('//table[@id="referer_grid"]').find_elements_by_tag_name('tr')
        for i in range(len(rows)):
            #print(rows[i].text)
            cells = rows[i].text.strip().split(' ')
            if len(cells) >= 5 and 'Source' not in cells:
                #meta =rows[i].find_element_by_xpath('.//*[@data-toggle="table"]').get_attribute('data-original-title')
                #print(meta)
                print(cells)
                #post_dict['reason'].append(meta)
                post_dict['traffic_source'].append(cells[0])
                post_dict['clicks'].append(cells[1])
                post_dict['uniuqe_clicks'].append(cells[2])
                post_dict['landing_page'].append(cells[-1])
                cells.pop(0)
                cells.pop(1)
                cells.pop(2)
                cells.pop(-1)
                post_dict['store_view'].append(' '.join(cells))

    return post_dict



def process_df(post_dict):
    if 'commission' in post_dict:
        post_dict['date'] = (post_dict.date.apply(lambda x:pd.to_datetime(x)))
        post_dict['total_amount'] = (post_dict.total_amount.str.replace('$', ''))
        post_dict['commission'] = (post_dict.commission.str.replace('$', ''))

        post_dict['total_amount'] = (post_dict.total_amount.str.replace(',', ''))
        post_dict['commission'] = (post_dict.commission.str.replace(',', ''))

        post_dict['total_amount'] = post_dict['total_amount'].astype(float)
        post_dict['commission'] = post_dict['commission'].astype(float)


    return post_dict



if __name__ == '__main__':
    driver = init_driver()
    ed = (dt.datetime.now() - dt.timedelta(days=1))
    sd = (ed - dt.timedelta(days=65)).strftime('%Y-%m-%d')
    ed = ed.strftime('%Y-%m-%d')

    print('sd', sd)
    print('ed', ed)
    comm_data = lookup_commissions(driver, sd, ed)
    traffic_data = lookup_traffics(driver, sd, ed)
    print(comm_data)
    print(traffic_data)

    for td in traffic_data:
        print(td)
        print(len(traffic_data[td]))

    #comm_data = pd.DataFrame.from_dict(comm_data)
    #comm_data = process_df(comm_data)
    #sorted_comm = comm_data.sort_values('date', ascending=False)

    traffic_data = pd.DataFrame.from_dict(traffic_data)
    traffic_data = process_df(traffic_data)
    traffic_data.to_csv('traffic.csv')

    driver.close()