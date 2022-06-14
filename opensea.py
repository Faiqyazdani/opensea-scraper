import scrapy
import json
import csv
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


headers_csv = ['token','url', 'name', 'description', 'wallet', 'twitter', 'instagram', 'website_url']
csvfile = open('opensea.csv', 'w', newline='', encoding='utf-8')
writer = csv.DictWriter(csvfile, fieldnames=headers_csv)
writer.writeheader()
csvfile.flush()

token = open("opensea-wallets - Sheet1.csv","r")
tokens = token.read().split("\n")

options = Options()
options.add_argument("start-maximized")
options.add_argument("--incognito")
# options.add_argument("--headless")
driver =webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

for tok in tokens:
    driver.get("http://opensea.io/{}".format(tok))
    time.sleep(6)
    response = scrapy.Selector(text=driver.page_source)
    data = json.loads([v for v in response.css("script::text").getall() if "window.__wired_" in v][0].split("window.__wired__")[-1][1:])
    item = dict()
    item['token'] = tok
    item['url'] = driver.current_url
    item['name'] = response.css("h1::text").get()
    item['description'] = [v for v in list(data['records'].values()) if "AccountType" in v['__typename']][0]['bio']
    try:
        item['wallet'] = [v for v in list(data['records'].values()) if "Name" in v['__typename']][0]['name']
    except:
        item['wallet'] = ''
    if item['description'] is None:
        item['description'] = ''
    try:
        item['twitter'] = "https://twitter.com/" + [v for v in list(data['records'].values()) if '=:metadata' in v['__id']][0]['twitterUsername']
    except:
        item['twitter'] = ''
    try:
        item['instagram'] = "https://instagram.com/" + [v for v in list(data['records'].values()) if '=:metadata' in v['__id']][0]['instagramUsername']
    except:
        item['instagram'] = ''
    try:
        item['website_url'] = [v for v in list(data['records'].values()) if '=:metadata' in v['__id']][0]['websiteUrl']
    except:
        item['website_url'] = ''
    writer.writerow(item)
    csvfile.flush()
driver.quit()
