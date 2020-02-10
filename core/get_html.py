from selenium import webdriver
import requests
from django.utils.text import slugify
from currencies.models import Currency
import json

API_ENDPOINT = 'http://localhost:8000/currencies/'

def get_driver():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    driver = webdriver.Firefox(executable_path='./geckodriver', firefox_options=fireFoxOptions)
    return driver


def get_url(url):
    driver = get_driver()
    driver.get(url)
    return driver

def get_currencies_info(url):
    driver = get_url(url)
    currency_table = driver.find_element_by_xpath('//table/tbody')
    rows = currency_table.find_elements_by_tag_name('tr')
    currencies = []
    if not rows:
        driver.quit()
        raise Exception("Couldn't find any currency")
    else:
        for row in rows:
            name = row.find_element_by_xpath('.//td//span').text
            change = row.find_element_by_xpath('.//td[2]//span').text
            chaos_value = float(row.find_element_by_xpath('.//td[3]//span').get_attribute('title'))
            currency_value = float(row.find_element_by_xpath('.//td[4]//span').get_attribute('title'))
            slug = slugify(name)
            value = chaos_value/currency_value
            currency = {
                "name" : name,
                "change" : change,
                "value" : value,
                "slug" : slug
            }
            currencies.append(currency)
        driver.quit()
    return currencies

def post_currencies(url):   
    currencies = get_currencies_info(url)
    return requests.post(API_ENDPOINT, json = currencies, headers={'Authorization': 'Bearer 3a18e524eb40f14c23b987a410e3d39cbebee964'})

def update_currencies(url):
    currencies = get_currencies_info(url)
    r = requests.put(API_ENDPOINT + 'bulk_update/', json = currencies, headers={'Authorization': 'Bearer 3a18e524eb40f14c23b987a410e3d39cbebee964'})


def log_error(e):
    print(e)
    