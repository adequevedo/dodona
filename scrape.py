# user xpath //*[@id="txtAccessOfCode"]
# password xpath //*[@id="txtAccessOfPassword"]

# login button xpath //*[@id="form1"]/input[3]

# football xpath //*[@id="divSportMenu"]/div[3]/div[2]

# NFL xpath //*[@id="divSportMenu"]/div[3]/div[3]/div[3]

import os
from urllib import request

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# Navigate to the website
driver.get("https://betus44.com/Logins/007/sites/betus44/index.aspx")

# Wait for the page to load
time.sleep(2)

# Find the username, password fields and login button by their XPath
username_field = driver.find_element(By.XPATH, '//*[@id="txtAccessOfCode"]')
password_field = driver.find_element(By.XPATH, '//*[@id="txtAccessOfPassword"]')
login_button = driver.find_element(By.XPATH, '//*[@id="form1"]/input[3]')

# Input username and password
username_field.send_keys("P85908")
password_field.send_keys("AG08")

# Click the login button
login_button.click()

# Wait for the next page to load
time.sleep(2)

# Perform further interactions here...
football_button = driver.find_element(By.XPATH, '//*[@id="divSportMenu"]/div[3]/div[2]')
football_button.click()

time.sleep(2)

nfl_button = driver.find_element(By.XPATH, '//*[@id="divSportMenu"]/div[3]/div[3]/div[3]')
nfl_button.click()


time.sleep(10)




# Close the browser
driver.quit()
