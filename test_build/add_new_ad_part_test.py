import os
import sys
import time
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../functions')))

from data1 import data1
from playdb import convert_seconds, insert_result_data, work, end_work, insert_mistake, add_start_end

global execution_time
global result
global mistake
global start_time
global end_time
global start_formatted
global end_formatted
name = 'add_new_ad_part_test.py'
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
    driver.get("https://japancar.ru/")

    work(name)

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
    driver.find_element(By.XPATH,"//li/a[@href='/add/parts/']").click()

    h1 = driver.find_element(By.TAG_NAME,"h1").text
    if h1 == "Разместить объявление о продаже запчасти на автомобиль":
        print('правильный раздел запчасти на авто')
    else:
        print('неправильный раздел запчасти на авто')

    work(name)

    driver.find_element(By.XPATH, "//*[@id='partsState']/label[1]").click()

    driver.find_element(By.XPATH, "//*[@id='add']/div[2]/div[2]/div[1]/label[1]").click()

    oem = driver.find_element(By.XPATH, "//*[@id='cl_OEM']")
    oem.click()
    oem.send_keys("UDS-013")
    sleep(1)

    work(name)

    part = driver.find_element(By.XPATH, "//*[@id='cl_partCode-label']")
    part.click()
    part.send_keys("фара")
    sleep(1)

    driver.find_element(By.XPATH, "//div[2]/label[2]").click()
    sleep(3)

    work(name)

    driver.find_element(By.ID,"f_marka").click()
    driver.find_element(By.XPATH,"//*[@id='f_marka']/option[10]").click()

    driver.find_element(By.ID, "f_model").click()
    sleep(2)
    driver.find_element(By.XPATH, "//*[@id='f_model']/option[7]").click()
    sleep(1)
    price = driver.find_element(By.ID, "f_price")
    price.click()
    price.send_keys('1000000000')
    sleep(3)

    work(name)

    town = driver.find_element(By.CLASS_NAME, "js-name")
    town.click()
    town11 = town.text
    sleep(1)

    work(name)

    town1 = driver.find_element(By.CLASS_NAME, "js-town-123")
    town22 = town1.text
    sleep(3)
    if town11 == town22:
        town.click()
    else:
        town1.click()
    driver.find_element(By.CLASS_NAME, "js-btnAddAdv").click()

    work(name)

    sleep(10)

    h1 = driver.find_element(By.LINK_TEXT, "Удалить")
    if h1:
        print('Объявление успешно добавлено!!!')
    else:
        print('где-то ошибка')
    h1.click()
    p = driver.find_element(By.CLASS_NAME, "main")
    p = p.text

    work(name)

    if p == 'Объявление удалено из раздела "Запчасти".':
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

