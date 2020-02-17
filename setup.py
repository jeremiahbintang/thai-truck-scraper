# To initialise browser
from selenium import webdriver
# To search using parameters
from selenium.webdriver.common.by import By
# To wait for a page to eload
from selenium.webdriver.support.ui import WebDriverWait
# To spceify what to look when a page is loaded
from selenium.webdriver.support import expected_conditions as EC
# To handle timeout situation
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException

import json
import time

def start_browser():
    # create incognito
    option = webdriver.ChromeOptions()
    option.add_argument(" - incognito")

    browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=option)
    browser.get("https://www.thaitruckcenter.com/tdsc/2Product/CompanyV_4")

    # Wait 20 seconds for page to load
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='col-12 px-1 bg__white content-block p-2']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    return browser

def get_page_url(browser):
    # find_elements_by_xpath returns an array of selenium objects.
    urls_element = browser.find_elements_by_xpath("//td[@class='tdLeft']/a")
    # use list comprehension to get the actual repo titles and not the selenium objects.
    urls = [x.get_attribute("href") for x in urls_element]

    return urls
    
browser = start_browser()
# 'กรุงเทพมหานคร', 'ระยอง', 'ชลบุรี', 'สมุทรปราการ'  
provinces = ['พระนครศรีอยุธยา']


for province in provinces:
    urls = set([])

    browser.find_element_by_xpath(f"//select[@name='ddlProvince']/option[text()='{province}']").click()
    browser.find_element_by_xpath("//a[@id='BtnSearch']").click()
    time.sleep(1)
    while True:
        urls.update(get_page_url(browser))
        print(len(urls))

        with open(f'{province}/urls.json', 'w') as file:
            file.write(json.dumps(str(urls)))

        try:
            button = browser.find_element_by_xpath("//a[@id='GridViewCompany_btnNext']").click()
            time.sleep(3)
        except NoSuchElementException:
            break
