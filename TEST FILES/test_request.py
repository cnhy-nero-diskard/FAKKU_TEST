import requests
import test_hardcode as txtfilter
from bs4 import BeautifulSoup as bs


title = "Sore Loser, Shunko!! ~Perfect Game~"
filtered = txtfilter.bruteSearch(title)+'sex'
# url = "https://www.fakku.net//"+filtered
url = "https://www.fakku.net//sore-loser-shunko-perfect-game-englishsex"

birb = requests.get(url)
b_parse = bs(birb.text,'html.parser')
print(dir(bs))