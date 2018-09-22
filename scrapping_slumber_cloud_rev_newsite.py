
import time
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from dateutil.parser import parse
from selenium.webdriver.common.keys import Keys


def generate_table_name(name):
    """Generate a table name from a file path
    """
    return name


def get_clear_browsing_button(driver):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return driver.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')


def clear_cache(driver, timeout=60):
    """Clear the cookies and cache for the ChromeDriver instance."""
    # navigate to the settings page
    driver.get('chrome://settings/clearBrowserData')

    # wait for the button to appear
    wait = WebDriverWait(driver, timeout)
    wait.until(get_clear_browsing_button)

    # click the button to clear the cache
    get_clear_browsing_button(driver).click()

    # wait for the button to be gone before returning
    wait.until_not(get_clear_browsing_button)


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=/Users/jennyhung/Desktop/Default")  # Path to your chrome profile
    #options.add_argument('--proxy-server=192.168.1.64:8888')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()
    #google = 'https://accounts.google.com/ServiceLogin/signinchooser?hl=en&passive=true&continue=https%3A%2F%2Fwww.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    #driver.get(google)
    #driver.find_element_by_id("identifierId").send_keys('jehug.lostsoul@gmail.com')
    #driver.find_element_by_id("identifierNext").click()
    time.sleep(10)
    #driver.find_element_by_xpath("//input[@type='password']").send_keys('Mathgifted2016')
    #driver.find_element_by_id("passwordNext").click()
    #time.sleep(10)
    return driver


def lookup_commissions(driver, sd, ed):
    # Log in first
    driver.get('https://www.slumbercloud.com/affiliates/account/login/')

    '''
    user = driver.find_element_by_xpath("//input[@placeholder='Email Address']")
    password = driver.find_element_by_xpath("//input[@placeholder='Password']")
    user.clear()
    user.send_keys(cred['username'])
    password.clear()
    password.send_keys(cred['password'])
    driver.find_element_by_xpath("//button[@id='send2']").click()
    driver.save_screenshot('login.png')
    '''

    mouse = webdriver.ActionChains(driver)
    user = driver.find_element_by_xpath("//input[@name='login[username]']")
    password = driver.find_element_by_xpath("//input[@name='login[password]']")
    mouse.move_to_element(user).perform()
    user.clear()
    mouse.click(user).perform()
    mouse.send_keys("mwolla@verticalscope.com").perform()
    time.sleep(8)
    driver.save_screenshot('now.png')

    mouse = ActionChains(driver)
    mouse.move_to_element(password).perform()
    mouse.click(password).perform()
    password.clear()
    mouse.send_keys("pIZeO8ec#3ld").perform()
    driver.save_screenshot('now1.png')
    time.sleep(8)
    #driver.find_element_by_xpath("//button[@id='send2']").click()
    #driver.find_element_by_xpath("//div[@class='primary']/button[@id='send2']").click()
    mouse.click(driver.find_element_by_xpath("//button[@id='send2']/span")).perform()
    driver.save_screenshot('now2.png')
    time.sleep(8)

    # Go to commissions
    # driver.find_element_by_link_text("Commissions").click()
    driver.get('https://www.slumbercloud.com/affiliate/account/')

    # now get conversion data
    # date is now created date in new site
    # product_name is now title in new site
    # total_amount is not gone from new site. Filled with zero
    # commission is now amount in new site
    # status remains the smae. No change

    post_dict = {'number': [], 'date': [], 'product_name': [], 'total_amount': [],
                 'commission': [], 'status': []}

    has_next = True
    while has_next:
        rows = driver.find_element_by_xpath('//table[@id="affiliate-transactions-history"]/tbody').find_elements_by_tag_name('tr')
        for i in range(len(rows)):
            row = rows[i].find_elements_by_tag_name('td')
            for j in range(len(row)):
                number = row[0].get_attribute('textContent')
                product_name = row[1].get_attribute('textContent')
                total_amount = '$0'
                commission = row[2].get_attribute('textContent')
                status = row[3].get_attribute('textContent')
                date = row[4].get_attribute('textContent')
                date = parse(date)

            post_dict['number'].append(number)
            post_dict['date'].append(date)
            post_dict['product_name'].append(product_name)
            post_dict['total_amount'].append(total_amount)
            post_dict['commission'].append(commission)
            post_dict['status'].append(status)
        try:
            driver.find_element_by_xpath('//a[@title="Next"]').click()

        except:
            has_next=False

    return post_dict


def lookup_traffics(driver, sd, ed):
    driver.find_element_by_link_text("Traffics").click()
    # now get traffics data
    post_dict = {'traffic_source': [], 'clicks': [], 'uniuqe_clicks': [], 'store_view': [],
                 'landing_page': []}

    total_items = driver.find_element_by_class_name("amount").text.strip().split(' ')[-2]
    print(total_items)

    # 10 per page
    total_pages = int(int(total_items) / 10) + 1
    for p in range(1, int(total_pages) + 1):
        if p == 1:
            pass
        else:
            try:
                driver.find_element_by_link_text(str(p)).click()
            except:
                pass

        rows = driver.find_element_by_xpath('//table[@id="referer_grid"]').find_elements_by_tag_name('tr')
        for i in range(len(rows)):
            # print(rows[i].text)
            cells = rows[i].text.strip().split(' ')
            if len(cells) >= 5 and 'Source' not in cells:
                # meta =rows[i].find_element_by_xpath('.//*[@data-toggle="table"]').get_attribute('data-original-title')
                # print(meta)
                print(cells)
                # post_dict['reason'].append(meta)
                traffic_source = cells[0]
                post_dict['traffic_source'].append(traffic_source)
                clicks = cells[1]
                post_dict['clicks'].append(clicks)
                u_clicks = cells[2]
                post_dict['uniuqe_clicks'].append(u_clicks)
                land_page = cells[-1]
                post_dict['landing_page'].append(land_page)
                cells.remove(traffic_source)
                cells.remove(clicks)
                cells.remove(u_clicks)
                cells.remove(land_page)
                print('cells', cells)

                post_dict['store_view'].append(' '.join(cells))

    return post_dict


def process_df(post_dict):
    if 'commission' in post_dict:
        post_dict['date'] = (post_dict.date.apply(lambda x: pd.to_datetime(x)))

        post_dict['total_amount'] = (post_dict.total_amount.str.replace('$', ''))
        post_dict['commission'] = (post_dict.commission.str.replace('$', ''))

        post_dict['total_amount'] = (post_dict.total_amount.str.replace(',', ''))
        post_dict['commission'] = (post_dict.commission.str.replace(',', ''))

        post_dict['total_amount'] = post_dict['total_amount'].astype(float)
        post_dict['commission'] = post_dict['commission'].astype(float)

        #post_dict['number'] = (post_dict.number.str.replace('#', ''))

    return post_dict


if __name__ == '__main__':
    driver = init_driver()
    ed = (dt.datetime.now() - dt.timedelta(days=1))
    sd = (ed - dt.timedelta(days=65)).strftime('%Y-%m-%d')
    ed = ed.strftime('%Y-%m-%d')

    print('sd', sd)
    print('ed', ed)
    comm_data = lookup_commissions(driver, sd, ed)
    comm_data['site'] = 'thesleepjudge.com'
    print(comm_data)


    comm_data = pd.DataFrame.from_dict(comm_data)
    comm_data = process_df(comm_data)
    sorted_comm = comm_data.sort_values('date', ascending=False)

    comm_data.to_csv('commission.csv')

    driver.close()