from bs4 import BeautifulSoup
import requests
import re

url = "https://www.fakku.net/hentai/after-school-thrills-english"

doc = requests.get(url)

parsed = BeautifulSoup(doc.text, "html.parser") #spits out html

pattern = [r'/artists/*']

search_1 = parsed.find('a', href= re.compile(pattern[0]) )

#reference: <meta property="og:description" content=" A lovely girl's secret side... ❤">
search_2 = parsed.find('meta', property='og:title')
print(search_2)

search_3 = parsed.find_all('a', href = re.compile("/tags/*"))
for i in search_3:
    print(i.text)

# for artist in search_1:
#     print(f'Artist {search_1.index(artist)}: {artist}')

print(search_1.text.strip()) # template for the author
print(search_2['content'].strip()) # template for the description, title, url