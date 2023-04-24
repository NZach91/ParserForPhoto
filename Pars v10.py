import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from selenium import webdriver
import pandas as pd

data = []
url_data = []
l_and_w = []

for p in range(50): # Website have 50 pages
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=options) # Use Selenium for take data from website, because site use JS to generate pages
    browser.get(f"https://www.esahubble.org/images/page/{p+1}/")
    generated_html = browser.page_source
    browser.quit()
    sleep(randint(2,5)) # delay 
    soup = BeautifulSoup(generated_html, "lxml")
    stars = soup.find('div', class_='image-list image-list-300').findAll('div', class_='picrow') # Get list of pages
    for star in stars:
        list_h_w =[]
        star_url = "https://esahubble.org" + star.find('a', class_="item").get('href')
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(star_url)
        star_html = browser.page_source #page of photo
        browser.quit()
        star_soup = BeautifulSoup(star_html, "lxml")
        star_size = star_soup.find('div', class_='container').find('div', class_='col-md-3 right-column').find('div', class_='object-info').find('div').find('td', class_='title', string='Size:').next_sibling # Take information about photo's page
        star_url_download ="https://esahubble.org" + star_soup.find('div', id='content').find('div', class_='container').find('div', class_='row page').find('div', class_='col-md-3 right-column').find('h3', class_='archivegrouptitle').next_sibling.find('a', string='Fullsize Original').get('href') # Get info about photo
        list_h_w = star_size.text[:star_size.text.find('p')-1].split('x') # Grab 2 numbers in list, heihgt and weight
        if (int(list_h_w[0]))>15000 and (int(list_h_w[1]))>15000: 
            data.append([star_url_download, star_size]) # pick up only large files
        sleep(randint(1,3)) #another delay
header = ([star_url_download, star_size])
sw = pd.DataFrame(data, columns=header)
sw.to_csv('/Users/kkrug/Desktop/Python/Parser 10', sep=';', encoding='utf8') # I used sibling because from page to page website have some difference in location of information.
