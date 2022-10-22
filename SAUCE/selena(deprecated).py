from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


textsearch = "Courting Étranger"


PATH = "C:\\Program Files (x86)\\chromedriver.exe"


option = webdriver.ChromeOptions()
option.add_argument('headless')
prefs = {"profile.managed_default_content_settings.images": 2}
option.add_experimental_option("prefs", prefs) # disable the images for faster loading time

s=Service(PATH)
driver = webdriver.Chrome(service=s, options = option)
driver.get("https://www.fakku.net")

print(driver.title)
# search = driver.find_element(By.XPATH, "//*[@id=\"suggest-content\"]")
search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"suggest-content\"]")))#faster
search.send_keys(textsearch)
search.send_keys(Keys.RETURN)

try:    # im waiting until the first doujin link is loaded unto the page
    content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@title=\"'+textsearch+'\"]')))
    # content = driver.find_element(By.XPATH, '//a[@title=\"'+textsearch+'\"]')
    print(f'Found {textsearch}')
    print('Exporting html')
    content.send_keys(Keys.RETURN)
except:
    print(f'Could not find {textsearch}')
    driver.close()






