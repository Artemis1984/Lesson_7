import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pprint import pprint
from pymongo import MongoClient
from hashlib import sha1
import warnings
warnings.filterwarnings('ignore')
from selenium.webdriver.common.action_chains import ActionChains



driver = webdriver.Chrome('/Users/paruyr1/PycharmProjects/Lesson_7/chromedriver')
driver.get('https:/account.mail.ru')

WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, 'Login')))
username = driver.find_element_by_name('Login')
# username.send_keys('test.mail.2021')
username.send_keys('artak-minasyan-84')
username.send_keys(Keys.RETURN)


WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.NAME, 'Password')))
username = driver.find_element_by_name('Password')
# username.send_keys('12091988A')
username.send_keys('30031984a')
username.send_keys(Keys.RETURN)


WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@class= 'dataset dataset_select-mode_off']//a")))
mail_list = driver.find_elements_by_xpath("//div[@class= 'dataset dataset_select-mode_off']//a")

client = MongoClient('localhost', 27017)
mail_db = client['mail_db']
mail = mail_db.mail

if mail_list:

    for i in range(len(mail_list)):

        try:
            driver.get(mail_list[i].get_attribute('href'))
            time.sleep(2)

        except:
            break
        date = driver.find_element_by_class_name('letter__date')
        letter = driver.find_element_by_class_name('html-parser')
        theme = driver.find_element_by_tag_name('h2')
        contact = driver.find_element_by_xpath("//span[@class= 'letter__contact-item']")

        temp_dict = {'Тема': theme.text,
                     'От кого': contact.text,
                     'Дата': date.text,
                     'Текст': letter.text.replace('\n', ''),
                     'hash': sha1(letter.text.replace('\n', '').encode('utf-8')).hexdigest()}
        pprint(temp_dict)

        driver.back()
        time.sleep(2)
        mail_list = driver.find_elements_by_xpath("//div[@class= 'dataset dataset_select-mode_off']//a")
        mail.update({'hash': temp_dict['hash']}, {'$set': temp_dict}, upsert=True)

for i in mail.find():
    pprint(i)

driver.close()
