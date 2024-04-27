#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install faker


# In[50]:


pip install amazoncaptcha


# In[88]:





# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
from faker import Faker
import selenium
from selenium import webdriver
import pandas as pd
import json
#from fuzzywuzzy import process
from selenium.webdriver.common.by import By
from tqdm import tqdm
index=10
import time
from bs4 import BeautifulSoup
from itertools import cycle
from fake_useragent import UserAgent
from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading 
import queue
import json
import requests


# In[ ]:


q = queue.Queue()
valid_proxies = []

with open(r"C:\Users\Thinpad\Desktop\proxy.txt", "r") as f:
    proxies = f.read().split("\n")
    for p in proxies:
        q.put(p)


def check_proxies():
    global q
    global valid_proxies
    while not q.empty():
        proxy = q.get()
        try:
            res = requests.get("https://ipinfo.io/json",
                               proxies={"http": proxy,
                                        "https": proxy})
            
        except:
            continue
        if res.status_code == 200:
            valid_proxies.append(proxy)
            print(proxy)

# Create and start threads
threads = []
for _ in range(10):
    t = threading.Thread(target=check_proxies)
    threads.append(t)
    t.start()

# Wait for all threads to finish
for t in threads:
    t.join()

# Write valid proxies to a text file
with open(r"C:\Users\Thinpad\Desktop\valid_proxies.txt", "w") as file:
    for proxy in valid_proxies:
        file.write(proxy + "\n")

driver.get("https://www.amazon.com/errors/validateCaptcha")
link = driver.find_element(By.XPATH, "//*[@class='a-row a-text-center']//img").get_attribute('src')
#print(img)
captcha = AmazonCaptcha.fromlink(link)
captcha_val = AmazonCaptcha.solve(captcha)

#print(captcha_val)
input_field = driver.find_element(By.ID , "captchacharacters").send_keys(captcha_val)
button = driver.find_element(By.CLASS_NAME , "a-button-text")
button.click()

# In[106]:


#html_content


# ##### CODE 

# In[2]:


def bypass_captcha(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='a-row a-text-center']//img")))
    
    captcha_img = driver.find_element(By.XPATH, "//*[@class='a-row a-text-center']//img")
    captcha_src = captcha_img.get_attribute('src')
    captcha = AmazonCaptcha.fromlink(captcha_src)
    captcha_val = AmazonCaptcha.solve(captcha)
    
    input_field = driver.find_element(By.ID, "captchacharacters")
    input_field.send_keys(captcha_val)
    button = driver.find_element(By.CLASS_NAME, "a-button-text")
    button.click()
    
    WebDriverWait(driver, 10).until_not(EC.url_contains("captcha"))  
    return driver.page_source  


# In[3]:


def get_soup_retry(url, proxy):
    driver.get(url)
    
    if 'captcha' in driver.page_source:
        html_content = bypass_captcha(driver)
        return BeautifulSoup(html_content, 'html.parser')  
    else:
        return BeautifulSoup(driver.page_source, 'html.parser') 

# Open the proxy file and get the proxy
with open(r"C:\Users\Thinpad\Desktop\valid_proxies.txt", "r") as f:
    proxy = f.readline().strip()


# In[29]:


#f = open(r"C:\Users\Thinpad\Desktop\links1.txt", "r")
#print(f.read())


# In[57]:


def get_data(driver, links):
    products = []
    for url in links:
        driver.get(url)
        time.sleep(5)
        
        product = {}
        product['URL'] = url 

        try:
            # Name    
            product_title_element = driver.find_element(By.CSS_SELECTOR, '#productTitle')
            product['title'] = product_title_element.text.strip()

            # ASIN
            try:
                asin_element = driver.find_element(By.CSS_SELECTOR, '#detailBullets_feature_div > ul > li:nth-child(8) > span > span:nth-child(2)')
                product['asin'] = asin_element.text.strip()
            except NoSuchElementException:
                product['asin'] = '0'

            # Ratings
            try:
                rate_element = driver.find_element(By.CSS_SELECTOR, '#acrPopover > span.a-declarative > a > span')
                product['ratings'] = rate_element.text.strip()
            except NoSuchElementException:
                product['ratings'] = '0'

            # Price 
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, '#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole')
                product['price'] = price_element.text.strip()
            except NoSuchElementException:
                product['price'] = '0'

            # Gender
            try:
                a_element = driver.find_element(By.CSS_SELECTOR, '#wayfinding-breadcrumbs_feature_div > ul > li:nth-child(3) > span > a')
                product['gender'] = a_element.text.strip()
            except NoSuchElementException:
                product['gender'] = '0'

            # Category
            try:
                b_element = driver.find_element(By.CSS_SELECTOR, '#wayfinding-breadcrumbs_feature_div > ul > li:nth-child(5) > span > a')
                product['category'] = b_element.text.strip()
            except NoSuchElementException:
                product['category'] = '0'

            # Sub-category
            try:
                c_element = driver.find_element(By.CSS_SELECTOR, '#wayfinding-breadcrumbs_feature_div > ul > li:nth-child(7) > span > a')
                product['sub_category'] = c_element.text.strip()
            except NoSuchElementException:
                product['sub_category'] = '0'

            # Brand name
            try:
                d_element = driver.find_element(By.CSS_SELECTOR, '#detailBullets_feature_div > ul > li:nth-child(5) > span > span:nth-child(2)')
                product['brand_name'] = d_element.text.strip()
            except NoSuchElementException:
                product['brand_name'] = '0'

           
            # Color links
            color_links = {}
            li_elements = driver.find_elements(By.CLASS_NAME, 'swatchAvailable')
            for li in li_elements:
                color = li.get_attribute('title').replace("Click to select ", "")
                link = li.find_element(By.TAG_NAME, 'img').get_attribute('src')
                color_links[color] = link
            product['color_links'] = color_links

            # Description 
            try:
                product_description_div = driver.find_element(By.ID, 'productDescription')
                product['description'] = product_description_div.text.strip()
            except NoSuchElementException:
                product['description'] = '0'

            # Initialize reviews list
            product['reviews'] = []

            # Reviews
            try:
                # Find all review elements
                review_elements = driver.find_elements(By.CSS_SELECTOR, 'span.review-text')

                # Loop through each review element and append the review text to the product's reviews list
                for review_elem in review_elements:
                    review_text = review_elem.text.strip()
                    product['reviews'].append(review_text)

            except NoSuchElementException:
                product['reviews'] = '0'

            products.append(product)
            file_path = r'C:\Users\Thinpad\Desktop\products10.json'
            with open(file_path, 'w') as json_file:
                json.dump(products, json_file, indent=4)

            time.sleep(5)

        except Exception as e:
            print(f"Error occurred while scraping data from {url}: {e}")

    return products


# In[58]:


def urls(selected_url, driver):
    link1 = []

    for i in range(1,35):  # Scraping from the first three pages
        current_page_url = driver.current_url
        #print("Current Page URL:", current_page_url)

        time.sleep(10)
        # Find all anchor tags containing the links
        anchor_tags = driver.find_elements(By.CSS_SELECTOR, 'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')
        for tag in anchor_tags:
            link_url = tag.get_attribute('href')
            if link_url:  
                link1.append(link_url)

        # Click the next page button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.s-pagination-next'))
        )
        next_button.click()

        time.sleep(5)

    file_path = r'C:\Users\Thinpad\Desktop\links4.txt'
    with open(file_path, 'w') as file:
        for l in links:
            file.write(l +'\n')

    # Convert link1 to a set to remove duplicates, then back to a list before returning
    
    link1 = list(set(link1))

    return link1


# In[59]:



url = "https://www.amazon.com/errors/validateCaptcha"
driver = webdriver.Edge()
driver.get(url)

driver.get("https://www.amazon.com/ref=nav_logo")
time.sleep(5)

# Change the URL to a new one
selected_url = 'https://www.amazon.com/s?i=fashion-mens-intl-ship&bbn=16225019011&rh=n%3A7141123011%2Cn%3A16225019011%2Cn%3A6358539011&page=12&qid=1710241182&ref=sr_pg_50'
#selected_url='https://www.amazon.com/s?i=specialty-aps&bbn=16225018011&rh=n%3A7141123011%2Cn%3A16225018011%2Cn%3A15743631&ref=nav_em__nav_desktop_sa_intl_handbags_0_2_12_6'
driver.get(selected_url)

# Wait for a few seconds to allow the new page to load
time.sleep(5)



soup_selected = get_soup_retry(selected_url, proxy)
links = urls(selected_url , driver)
products  = get_data(driver, links)


# In[53]:


#products  = get_data(driver, links)


# In[56]:


len(links)

file_path = r'C:\Users\Thinpad\Desktop\links2.txt'
with open(file_path, 'w') as file:
    for l in links:
        file.write(l +'\n')
# In[16]:


len(links)


# In[ ]:





# In[12]:


json_string = json.dumps(products, indent=4)  
#print(json_string)


# In[13]:


file_path = r'C:\Users\Thinpad\Desktop\products_hani.json'
with open(file_path, 'w') as json_file:
    json.dump(products, json_file, indent=4)

print(f"Products data saved to {file_path}")


# In[102]:


len(links)


# In[ ]:




