#
from bs4 import BeautifulSoup
import pymongo
from flask_pymongo import PyMongo
from splinter import Browser
import requests
import time
import pandas as pd

from splinter import browser
from selenium import webdriver

def scrape():


    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless = False)


    url = "https://mars.nasa.gov/news/"
    browser.visit(url)


    news_html = browser.html
    soup = BeautifulSoup(news_html, "html.parser")


    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text



    #image

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)


    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    browser.click_link_by_partial_text('more info')


    image_html = browser.html
    soup = BeautifulSoup(image_html, "html.parser")


    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path




    # Mars Weather


    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)

    weather_html = browser.html
    soup = BeautifulSoup(weather_html, 'html.parser')

    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    #Facts---- cannot figure out how to do without requests sorry!


    mars_facts = requests.get("https://space-facts.com/mars/")
    space_table = pd.read_html(mars_facts.text)

    df = space_table[0]
    mars_data = df.to_html()
    new_mars_data= mars_data.replace('\n', '')

    new_mars_data


    #Hemisphere Images
    
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    hemisphere_image_urls = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

                
        #Dictionary for Mongo

        mars_dict = {
            "id": 1,
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "mars_weather": mars_weather,
            "new_mars_data": new_mars_data,
            "hemisphere_i": hemisphere_image_urls
            }
    return mar_dict