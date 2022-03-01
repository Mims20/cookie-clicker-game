from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_webdriver = "C:\chromedriver_win32\chromedriver"  # chrome driver location
driver = webdriver.Chrome(executable_path=chrome_webdriver)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# clickable cookie
cookie = driver.find_element(By.ID, "cookie")

check_price = time.time() + 5
timeout = time.time() + 60 * 5

# upgrade items and ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]
# item_ids = item_ids[7::-1]

while True:
    cookie.click()

    # check every 5secs
    if time.time() > check_price:
        # find prices of each id and convert to int for later comparison
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []
        for price in all_prices:
            if price.text != "":
                price = int((price.text.split("-")[1].strip().replace(",", "")))
                item_prices.append(price)

        # get your current money
        my_money = driver.find_element(By.ID, "money").text
        if "," in my_money:
            my_money = my_money.replace(",", "")

        # check highest item you can afford with my_money
        # then get index of the price, use that to get actual item id in item_ids
        # click element to buy

        affordable_items = []
        for price in item_prices:
            if int(my_money) > price:
                affordable_items.append(price)

        max_price = max(affordable_items)
        index = item_prices.index(max_price)
        upgrade_item = driver.find_element(By.ID, item_ids[index])
        upgrade_item.click()

        # increase time by 5secs so you can check for price
        check_price = time.time() + 5

    if time.time() > timeout:
        break

cookies_per_sec = driver.find_element(By.ID, "cps").text
print(cookies_per_sec)

driver.quit()
