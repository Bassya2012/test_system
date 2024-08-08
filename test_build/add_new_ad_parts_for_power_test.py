import os
import sys
import time
from time import sleep
from datetime import datetime

from selenium.webdriver import ActionChains

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../functions')))

from data1 import data1
from selenium import webdriver
from selenium.webdriver.common.by import By
from playdb import convert_seconds, insert_result_data, insert_mistake, end_work, work, add_start_end

global execution_time
global result
global start_time
global end_time
global mistake
global start_formatted
global end_formatted
name = 'add_new_ad_parts_for_power_test.py'
try:
    data1()

    work(name)

    start_time = time.time()
    start_object = datetime.fromtimestamp(start_time)
    start_formatted = start_object.strftime('%Y-%m-%d %H:%M:%S')

    op = webdriver.ChromeOptions()
    op.add_argument("window-size=1920,1080")
    op.add_argument('disable-gpu')
    op.add_argument("headless")
    driver = webdriver.Chrome(options=op)
    # driver = webdriver.Chrome()

    work(name)

    driver.get("https://japancar.ru/")
    # пока авторизация в начале
    login = driver.find_element(By.NAME, "login")
    login.send_keys("zlataang+testing@gmail.com")
    password = driver.find_element(By.NAME, "pass")
    password.send_keys("+7953216@")
    submit = driver.find_element(By.CLASS_NAME, "js-btnAuthOn")
    submit.click()
    sleep(5)

    work(name)

    driver.find_element(By.XPATH,"//div[@class='col pl-10 text-right']/a[@href='/add/']").click()
    driver.find_element(By.XPATH,"//li/a[@href='/add/powerparts/']").click()
    h1 = driver.find_element(By.TAG_NAME,"h1").text
    if h1 == "Разместить объявление о продаже запчасти на коммерческий транспорт, грузовик":
        print('правильный раздел запчасть на ком.транспорт')
    else:
        print('неправильный раздел запчасть на ком.транспорт')

    name1 = driver.find_element(By.ID, "f_name_text")
    name1.click()
    name1.send_keys('руль')

    work(name)

    driver.find_element(By.ID, "f_year").click()
    driver.find_element(By.XPATH, "//*[@id='f_year']/option[5]").click()

    driver.find_element(By.ID,"f_firm").click()
    driver.find_element(By.XPATH,"//*[@id='f_firm']/option[8]").click()
    sleep(3)

    model = driver.find_element(By.ID, "f_model")
    model.click()
    model.send_keys('лучшая модель на свете')

    work(name)

    driver.find_element(By.XPATH, "//*[@id='add']/div[10]/div/div[1]/label[2]").click()

    driver.find_element(By.XPATH, "//*[@id='add']/div[11]/div/div[1]/label[3]").click()

    price = driver.find_element(By.ID,"f_price")
    price.click()
    price.send_keys('777')

    work(name)

    town = driver.find_element(By.CLASS_NAME, "js-name")
    town.click()
    sleep(1)
    town1 = driver.find_element(By.CLASS_NAME, "js-town-123")
    sleep(1)
    if town == town1:
        town.click()
    else:
        town1.click()

    driver.find_element(By.CLASS_NAME, "js-btnAddAdv").click()

    sleep(5)

    h1 = driver.find_element(By.LINK_TEXT, "Удалить")
    if h1:
        print('Объявление успешно добавлено!!!')
    else:
        print('где-то ошибка')

    work(name)

    h1.click()
    p = driver.find_element(By.TAG_NAME, "h1")
    p = p.text
    if p == 'Объявление удалено!':
        print('Объявление успешно удалено')
    else:
        print('где-то ошибка')

    result = 'passed'
    sleep(3)

except Exception as e:
    result = 'failed'
    mistake = e
    print('BAN', e)
finally:
    end_time = time.time()
    end_object = datetime.fromtimestamp(end_time)
    end_formatted = end_object.strftime('%Y-%m-%d %H:%M:%S')
    execution_time = convert_seconds(int(end_time - start_time))
    print('execution_time', execution_time)
    if result == 'passed':
        insert_result_data(name, execution_time, result)
    else:
        insert_mistake(name, execution_time, result, mistake)
    end_work(name)
    add_start_end(start_formatted, end_formatted, name)
    driver.quit()