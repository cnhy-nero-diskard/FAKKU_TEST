from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import difflib
import requests
import time


def bruteSearch(text, extension='english', url="https://www.fakku.net/hentai/"):
    # will attempt to hardcode the doujin separated by dash into the browser if fakku is trolling
    wspaceSplit = text.split()
    filSplit = []
    for unf in wspaceSplit:
        cleansed = ''.join(filter(str.isalnum, unf)).lower()
        filSplit.append(cleansed)
    filSplit.append(extension)

    return url+'-'.join(filSplit)

def htmlParse(textsearch, url="https://www.fakku.net"):
    """PROMISE TO SELF: I WILL OPTIMIZE THIS (I'M GONNA ASSUME) HORRIBLE SNIPPET OF CODE
        TILL THEN, BEAR WITH MY NOOBNESS
        WARNING: THIS ONLY WORKS WITH FAKKU.NET
        I'M TOO LAZY TO MAKE AN NHENTAI API WHEN SOMEONE ALREADY MADE ONE"""

    canParse = True
    PATH = "C:\\Program Files (x86)\\chromedriver.exe"

    option = webdriver.ChromeOptions()
    option.add_argument('headless')      #---->DEBUG FOR BROWSER-LESS POP UP
    prefs = {"profile.managed_default_content_settings.images": 2}
    option.add_experimental_option("prefs", prefs)  # disable the images for faster loading time

    s = Service(PATH)
    driver = webdriver.Chrome(service=s, options=option) # not deprecated version of creating an object in selenium

    ###########INITIALIZATION COMPLETE################
    driver.get(url)

    print(f'Accessing {driver.current_url}')   # ----> DEBUG

    search = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"suggest-content\"]")))  #

    # emulate human-like key presses because FAKKU tends to troll scripts or my internet is slow af
    search.send_keys(textsearch[:-1])
    search.send_keys(textsearch[-1])
    search.send_keys(Keys.BACK_SPACE)
    search.send_keys(textsearch[-1])

    # //*[@id="js-search-results"]/a[1] --> Rel XPATH for search bar 1st option
    print(f'Accessing {driver.current_url}')

    try:
        # search =
        search1 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "underline"))) # underline specifies most similar in popup
        print("CLICKING")           #----->DEBUG
        search1.click()

        # /html/body/div[1]/div[2]/div[2]/div/div[2]/h1 ---> XPATH for the title in blindfolded page

        verify = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/h1")
        seq = difflib.SequenceMatcher(a=verify.text.lower(), b=textsearch.lower())  # exception when title not same
        print(f'[{verify.text}] as blindfold webpage as ref wall [{textsearch}] with'
              f'similarity ratio {seq.ratio()}')
        print(f'Found [{textsearch}] in {driver.current_url} with no exception')
        htmlfile = driver.page_source
        url = driver.current_url

    except:
        print(f'[FAILED]Could not find {textsearch}')
        print("Attempting redirect through hardcoding")
        altURL = bruteSearch(textsearch)
        altHTML = requests.get(altURL)
        htmlfile = altHTML.text
        url = altURL
        print(url)

    return htmlfile, url  # ill assume this will return an object same as requests.get()
