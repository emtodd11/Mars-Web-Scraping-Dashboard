#dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
import datetime as dt


def mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:

        result = soup.body.find('div', class_='features')
        news_title = result.find('div', class_='content_title').text
        news_p = result.find('div', class_='rollover_description_inner').text

    except AttributeError:

        return None, None

    return news_title, news_p


def mars_image(browser):

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    relative_image_url = soup.find('a', class_='button fancybox')['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + relative_image_url
    return featured_image_url


def twitter_weather(browser):

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    return mars_weather


def mars_facts(browser):
    try:
        url = 'https://space-facts.com/mars/'
        df = pd.read_html(url)[0]
        df.columns=['description', 'value']
        df.set_index('description', inplace=True)
    except BaseException:
        return None
    return df.to_html(classes="table table-striped")


def mars_hemispheres(browser):
    hemisphere_image_urls = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    browser.click_link_by_partial_text('Cerberus')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h2', class_='title').text
    img_url = "https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src']
    hemi_dict = {'title': title,
             'img_url': img_url}
    hemisphere_image_urls.append(hemi_dict)
    browser.click_link_by_partial_text('Back')

    browser.click_link_by_partial_text('Schiaparelli')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h2', class_='title').text
    img_url = "https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src']
    hemi_dict = {'title': title,
                'img_url': img_url}
    hemisphere_image_urls.append(hemi_dict)
    browser.click_link_by_partial_text('Back')

    browser.click_link_by_partial_text('Syrtis')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h2', class_='title').text
    img_url = "https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src']
    hemi_dict = {'title': title,
                'img_url': img_url}
    hemisphere_image_urls.append(hemi_dict)
    browser.click_link_by_partial_text('Back')

    browser.click_link_by_partial_text('Valles')
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h2', class_='title').text
    img_url = "https://astrogeology.usgs.gov" + soup.find('img', class_='wide-image')['src']
    hemi_dict = {'title': title,
                'img_url': img_url}
    hemisphere_image_urls.append(hemi_dict)
    browser.click_link_by_partial_text('Back')

    return hemisphere_image_urls


def scrape_all():
    executable_path = {'executable_path': './chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    featured_image_url = mars_image(browser)
    mars_weather = twitter_weather(browser)
    hemisphere_image_urls = mars_hemispheres(browser)
    facts = mars_facts(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "hemispheres": hemisphere_image_urls,
        "weather": mars_weather,
        "facts": facts,
        "last_modified": timestamp
    }
    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape_all())