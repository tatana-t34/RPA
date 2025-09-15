# Б - Mozilla Firefox
# А - standard_user / secret_sauce
# В - Сортировка по цене (low to high)
# Г - Добавить самый дорогой товар (обратите внимание на сортировку!).
# Б - Добавить товар в корзину, перейти в корзину и удалить его оттуда.

import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

GECKODRIVER_PATH = r"C:/Program Files/geckodriver.exe"
service = Service(GECKODRIVER_PATH)
driver = webdriver.Firefox(service=service)

driver.get("https://www.saucedemo.com/")
time.sleep(2)

username = "standard_user"
password = "secret_sauce"

driver.find_element(By.ID, "user-name").send_keys(username)
driver.find_element(By.ID, "password").send_keys(password)
time.sleep(2)

driver.find_element(By.ID, "login-button").click()
time.sleep(2)

#Проверка locked_out_user
try:
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    if "locked out" in error.text.lower():
        print("Этот аккаунт заблокирован. Пробуем с другим пользователем...")
        driver.find_element(By.ID, "user-name").clear()
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "user-name").send_keys("problem_user")
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(2)
except NoSuchElementException:
    pass

#Сортировка товаров (low to high)
sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
sort_dropdown.select_by_value("lohi")  # low to high
time.sleep(2)

#Выбор самого дорогого товара
names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
add_buttons = driver.find_elements(By.CSS_SELECTOR, ".inventory_item button")

most_expensive_index = len(prices) - 1
product_name = names[most_expensive_index].text
product_price = prices[most_expensive_index].text

add_buttons[most_expensive_index].click()
time.sleep(2)

#Переход в корзину
driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
time.sleep(2)

#Удаление товара из корзины
cart_item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
cart_item_price = driver.find_element(By.CLASS_NAME, "inventory_item_price").text

driver.find_element(By.CSS_SELECTOR, ".cart_item button").click()
time.sleep(2)

driver.quit()
