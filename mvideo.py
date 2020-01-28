import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
from pymongo import MongoClient
import warnings
warnings.filterwarnings('ignore')


button_xpath = "//div[@data-init= 'ajax-category-carousel'][1]//div[@class= 'carousel-paging']//a"
driver = webdriver.Chrome('/Users/paruyr1/PycharmProjects/Lesson_7/chromedriver')
driver.get('https://www.mvideo.ru/')

a = "//div[@data-init= 'ajax-category-carousel'][1]//li[@class= 'gallery-list-item']//a[@class= 'sel-product-tile-title']"

WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
buttons = driver.find_elements_by_xpath(button_xpath)

name_list = []
price_list = []
link_list = []

client = MongoClient('localhost', 27017)
mvideo_db = client['mvideo_db']
mvideo = mvideo_db.mvideo

for i in range(len(buttons)):

    buttons[i].click()
    time.sleep(2)
    links = driver.find_elements_by_xpath(a)

    for j in links:

        if j.get_attribute('href') in link_list:
            continue
        link_list.append(j.get_attribute('href'))

for link in link_list:

    driver.get(link)
    time.sleep(3)
    name = driver.find_element_by_tag_name("h1")
    photos = driver.find_elements_by_xpath("//a[@data-src]")
    for i in photos:
        if i.get_attribute('data-src').startswith('//img'):
            photos[photos.index(i)] = 'https:'+i.get_attribute('data-src')

        else:
            photos[photos.index(i)] = i.get_attribute('data-src')[2:]

    price = driver.find_element_by_xpath("//div[@class= 'c-pdp-price__current sel-product-tile-price']")
    price = price.text.replace('¤', '₽')
    _id = driver.find_element_by_xpath("//p[@class='c-product-code']")

    temp_dict = {'Название': name.text,
                 'Фото': photos,
                 '_id': _id.text,
                 'Цена': price}

    mvideo.update({'_id': temp_dict['_id']}, {'$set': temp_dict}, upsert=True)


for i in mvideo.find():
    pprint(i)

time.sleep(5)
driver.close()
