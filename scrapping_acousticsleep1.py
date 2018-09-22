## Goal: get the thread that is top 100 popular: by views, by replies
## Write function to sort by reviews or replies
## .csv file to contain: link_to_thread, name_of_thread, views, replies, last_post_time, last_post_date




import time
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
import base64




def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 3)
    return driver


def lookup_commissions(driver, sd, ed):
    # Log in first
    driver.get('https://www.affiliatly.com/login.html')
    driver.find_element_by_link_text("Affiliates").click()

    driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
    ele_captcha = driver.find_element_by_xpath("//img[contains(./@src, 'image.php')]")

    # get the captcha as a base64 string
    img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
          ele.removeEventListener('load', fn, false);
          var cnv = document.createElement('canvas');
          cnv.width = this.width; cnv.height = this.height;
          cnv.getContext('2d').drawImage(this, 0, 0);
          callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, ele_captcha)

    with open(r"image.php", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))


    user = driver.find_element_by_xpath("//input[@id='InputEmail1']")
    user.clear()
    user.send_keys("mwolla@verticalscope.com")
    password = driver.find_element_by_xpath("//input[@id='InputPassword1']")
    password.clear()
    password.send_keys("Vscope700!")

    driver.switch_to_frame('Main')
    sec_code = driver.find_element_by_xpath("//input[@id='security_code_input']")
    sec_code.clear()
    sec_code.send_keys('image.php')

    # date picker
    datepicker_from = driver.find_element_by_xpath("//input[@name='date_from']")
    driver.execute_script("arguments[0].value='"+sd+"';", datepicker_from)
    driver.execute_script(sd, datepicker_from)
    print('from', datepicker_from.get_attribute('value'))

    datepicker_to = driver.find_element_by_xpath("//input[@name='date_to']")
    driver.execute_script("arguments[0].value='"+ed+"';", datepicker_to)
    print('now', datepicker_to.get_attribute('value'))

    # Go to conversions
    #driver.find_element_by_link_text("Show").click()
    driver.find_element_by_xpath("//button[@class='btn btn-success show_summary_data']").click()

    # now get conversion data
    post_dict = {'date':[], 'visitors': [], 'order': [], 'earnings': [], 'conversions':[]}

    rows = driver.find_element_by_xpath('//div[@class="table_responsive_holder"]').find_elements_by_tag_name('tr')
    cols = driver.find_element_by_xpath('//div[@class="table_responsive_holder"]').find_elements_by_tag_name('td')
    print('here', rows[1].find_elements_by_tag_name('td')[0].text)

    for i in range(1,len(rows)):
    #for col in cols:
        print('here', rows[i].find_elements_by_tag_name('td')[0].text)
        post_dict['date'].append(rows[i].find_elements_by_tag_name('td')[0].text)
        post_dict['visitors'].append(rows[i].find_elements_by_tag_name('td')[1].text)
        post_dict['order'].append(rows[i].find_elements_by_tag_name('td')[2].text)
        post_dict['earnings'].append(rows[i].find_elements_by_tag_name('td')[3].text)
        post_dict['conversions'].append(rows[i].find_elements_by_tag_name('td')[4].text)

    print(post_dict)

    return post_dict



def process_df(post_dict):
    post_dict['date'] = (post_dict.date.apply(lambda x:pd.to_datetime(x)))
    post_dict['earnings'] = (post_dict.commission.str.replace('$', ''))
    post_dict['earnings'] = post_dict['commission'].astype(float)
    post_dict['visitors'] = post_dict['visitors'].astype(float)

    return post_dict



if __name__ == '__main__':
    driver = init_driver()
    ed = (dt.datetime.now() - dt.timedelta(days=1))
    sd = (ed - dt.timedelta(days=65)).strftime('%m/%d/%Y')
    ed = ed.strftime('%m/%d/%Y')

    print('sd', sd)
    print('ed', ed)
    order_data = lookup_commissions(driver, sd, ed)
    order_data['site'] = 'thesleepjudge.com'
    print(order_data)

    order_data = pd.DataFrame.from_dict(order_data)
    order_data = process_df(order_data)
    sorted_order = order_data.sort_values('date', ascending=False)

    order_data.to_csv('commission.csv')

    driver.close()
