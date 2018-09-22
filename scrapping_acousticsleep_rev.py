
import time
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
import base64
from PIL import Image





def init_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.wait = WebDriverWait(driver, 3)
    return driver


def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x']
    top = location['y'] + 140
    right = location['x'] + size['width']
    bottom = location['y'] + size['height'] + 140

    image = image.crop((left, top, right, bottom))  # defines crop points
    #image.save(path, 'jpeg')  # saves new cropped image
    return image


def lookup_commissions(driver, sd, ed):
    # Log in first
    driver.get('https://www.affiliatly.com/af-1013747/affiliate.panel')

    user = driver.find_element_by_xpath("//input[@id='exampleInputEmail1']")
    user.clear()
    user.send_keys("mwolla@verticalscope.com")
    password = driver.find_element_by_xpath("//input[@id='exampleInputPassword1']")
    password.clear()
    password.send_keys("Vscope700!!")

    driver.find_element_by_xpath("//button[@name='login']").click()
    time.sleep(3)

    # date picker
    datepicker_from = driver.find_element_by_xpath("//input[@name='date_from']")
    driver.execute_script("arguments[0].value='"+sd+"';", datepicker_from)
    print('from', datepicker_from.get_attribute('value'))

    datepicker_to = driver.find_element_by_xpath("//input[@name='date_to']")
    driver.execute_script("arguments[0].value='"+ed+"';", datepicker_to)
    print('now', datepicker_to.get_attribute('value'))

    # Go to conversions
    driver.find_element_by_xpath("//button[@class='btn btn-success show_summary_data']").click()

    # now get conversion data
    post_dict = {'date':[], 'visitors': [], 'order': [], 'price':[], 'earnings': [], 'conversions':[]}

    rows = driver.find_element_by_xpath('//div[@class="table_responsive_holder"]').find_elements_by_tag_name('tr')
    cols = driver.find_element_by_xpath('//div[@class="table_responsive_holder"]').find_elements_by_tag_name('td')
    print('here', rows[1].find_elements_by_tag_name('td')[0].text)

    for i in range(1,len(rows)):
        #print(rows[i].text)
        #print('here', rows[i].find_elements_by_tag_name('td')[0].text)
        if 'Totals' not in rows[i].text:
            post_dict['date'].append(rows[i].find_elements_by_tag_name('td')[0].text)
            post_dict['visitors'].append(rows[i].find_elements_by_tag_name('td')[1].text)
            post_dict['order'].append(rows[i].find_elements_by_tag_name('td')[2].text)
            post_dict['price'].append(rows[i].find_elements_by_tag_name('td')[3].text)
            post_dict['earnings'].append(rows[i].find_elements_by_tag_name('td')[4].text)
            post_dict['conversions'].append(rows[i].find_elements_by_tag_name('td')[5].text)

    print(post_dict)

    return post_dict



def process_df(post_dict):
    post_dict['date'] = post_dict.date.apply(lambda x:pd.to_datetime(x, format='%d.%m.%Y'))
    post_dict['price'] = post_dict['price'].str.replace('$', '')
    post_dict['price'] = post_dict['price'].astype(float)
    post_dict['earnings'] = post_dict['earnings'].str.replace('$', '')
    post_dict['earnings'] = post_dict['earnings'].astype(float)

    return post_dict



if __name__ == '__main__':
    driver = init_driver()
    ed = (dt.datetime.now() - dt.timedelta(days=1))
    sd = (ed - dt.timedelta(days=65)).strftime('%d.%m.%Y')
    ed = ed.strftime('%d.%m.%Y')

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
