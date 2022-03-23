#!/usr/bin/env python
# coding: utf-8

# ### Modules ###

# In[1]:


import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


# ### Setting Chrome Path ###

# In[2]:

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


    # ### The URLs ###

    # In[3]:


    # the Websites to scrap
    news_url = 'https://redplanetscience.com/'
    image_url = 'https://spaceimages-mars.com/'
    galaxy_fact_url = 'https://galaxyfacts-mars.com/'
    mars_hemi_pics_url = 'https://marshemispheres.com/'


    # ### News! ###
    # In[4]:
    # URL to be scraped
    browser.visit(news_url)
    # new HTML object
    html = browser.html
    soup = bs(html, "html.parser")
    # In[5]:
    headline = soup.find("div", class_="content_title").get_text(strip=True)
    # In[6]:
    teaser = soup.find("div", class_="article_teaser_body").get_text(strip=True)
    
    # ### Mars Featured Image ###
    # In[7]:
    # URL to be scraped
    browser.visit(image_url)
    # new HTML object
    html = browser.html
    soup = bs(html, "html.parser")
    # Loop through images using Beautiful Soup and set feature_image_url
    featured_image_url = image_url + [img.get("src") for img in soup.find_all("img", class_="headerimage fade-in")][0]

    # ### Mars Facts / Galaxy Facts ###
    # In[8]:
    # URL to be scraped
    galaxy_facts_table = pd.read_html(galaxy_fact_url)
    # In[9]:
    mars_earth_com_df = galaxy_facts_table[0]
    mars_earth_com_df.columns = ['Description','Mars','Earth']
    mars_earth_com_table = mars_earth_com_df.to_html(classes="table table-striped", index = False)
    mars_earth_com_table
    
    # In[10]:
    mars_prof_df = galaxy_facts_table[1]
    mars_prof_df.columns = ['Description','Values']
    mars_prof_table = mars_prof_df.to_html(classes="table table-striped", index= False)
    mars_prof_table
    


    # ### Mars Hemisphere Images ###
    # In[11]:
    # URL to be scraped
    browser.visit(mars_hemi_pics_url)
    mars_images_urls = []
    for i in range(4):
            html = browser.html
            soup = bs(html, "html.parser")
            
            title = soup.find_all("h3")[i].get_text()
            browser.find_by_tag('h3')[i].click()
            
            html = browser.html
            soup = bs(html, "html.parser")
        
            img_url = soup.find("img", class_="wide-image")["src"]
        
            mars_images_urls.append({
                "title": title,
                "img_url": mars_hemi_pics_url + img_url})
            print 
            browser.back()
    #close browser
    browser.quit()  

    # ### Setting the HTML List ###
    # In[14]:
    # Set the List
    info_mars = []
    info_mars = {
        'headline': headline,
        'teaser': teaser,
        'featured_image': featured_image_url,
        'mars_earth_com_table': mars_earth_com_table,
        'mars_prof_table': mars_prof_table,
        'mars_images_urls':mars_images_urls
    }
    #printing the HTML List
    return info_mars





