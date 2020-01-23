from selenium import webdriver

def get_driver():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    driver = webdriver.Firefox(executable_path=r'/opt/geckodriver', firefox_options=fireFoxOptions)
    return driver


def get_url(url):
    driver = get_driver()
    driver.get(url)
    return driver

def get_currencies_info(url):
    driver = get_url(url)
    currency_table = driver.find_element_by_xpath('//table/tbody')
    rows = currency_table.find_elements_by_tag_name('tr')
    if not rows:
        log_error("Couldn't find any currency")
    else:
        for row in rows:
            name = row.find_element_by_xpath('.//td//span')
            change = row.find_element_by_xpath('.//td[2]//span')
            value = row.find_element_by_xpath('.//td[3]//span').get_attribute('title')
            print(value)
    driver.quit()


def log_error(e):
    print(e)