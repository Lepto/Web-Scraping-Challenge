import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit Red Planet Science website to scrape
    url='https://redplanetscience.com/'
    browser.visit(url)
    
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Collect latest Mars News
    news_title = soup.find('div', class_= 'content_title').text

    # Collect teaser text for Mars news
    news_p = soup.find('div', class_ = 'article_teaser_body').text

    # Visit Space Images-Mars website to scrape
    url='https://spaceimages-mars.com'
    browser.visit(url)

    time.sleep(1)

    # Scraping spaceimages-mars.com
    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    img_url = soup.find('img', class_ = 'headerimage')['src']
    featured_img_url = "https://spaceimages-mars.com/" + img_url
    
    # Visitng galaxyfacts-mars.com to scrape for Mars facts into a DataFrame
    MarsFacts_df = pd.read_html('https://galaxyfacts-mars.com')[1]
    MarsFacts_df.columns = ['Category', 'Mars']

    time.sleep(1)

    # Converting DataFrame into HTML table string
    MarsFacts_html = MarsFacts_df.to_html(classes = ["table", "table-striped"], index =False, justify = "left")
    MarsFacts = MarsFacts_html.replace('\n','')

    # Visit marshemispheres.com to scrape for hi-def images of Mars' hemispheres
    url='https://marshemispheres.com/'
    browser.visit(url)

    time.sleep(1)

    html_hemispheres = browser.html
    soup = bs(html_hemispheres , 'html.parser')

    #Create an empty list of links for the hemispheres
    hemisphere_img_urls=[]
    products=soup.find('div', class_='result-list')
    hemispheres=products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        ending_link = hemisphere.find("a")["href"]
        image_link = "https://marshemispheres.com/" + ending_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup = bs(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_= "downloads")
        image_url = downloads.find("a", string = "Sample") ["href"]
        hemisphere_img_urls.append({"title": title, "image_url": url+image_url})

    # mars_info dictionary
    mars_info = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_img_url" : featured_img_url,
        "MarsFacts" : MarsFacts,
        "hemisphere_img_urls" : hemisphere_img_urls
    }
       
    # Close the browser after scraping
    browser.quit()

    return mars_info