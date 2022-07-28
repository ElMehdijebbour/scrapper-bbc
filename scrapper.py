from email import header
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


# Create a new Firefox browser object
browser = webdriver.Chrome(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-popup-blocking")
browser.maximize_window()
print("Current session is {}".format(browser.session_id))

#Starting Scrapper

try:
    # Go to a website, click the button to show sub menu and wait 2 secs
    browser.get('https://www.bbc.com/news')
    html = browser.page_source
    report1 = browser.find_element("xpath", '/html/body/div[8]/header/div[2]/div/div[1]/nav/ul/li[15]/span/button').click()
    time.sleep(2)

    # Create BeautifulSoup object from page source.
    soup = BeautifulSoup(html, 'html.parser')
    page = bs(browser.page_source, 'html.parser')

    #Finding the categories 

    menu= soup.find('ul', { 'class': 'gs-o-list-ui--top-no-border nw-c-nav__wide-sections'})
    menu_subcategories=soup.find('div', { 'class':   'nw-c-nav__wide-overflow-list gel-layout'})
    categories = menu.find_all('li')
    sub_categories=menu_subcategories.find_all('li')

    print(menu_subcategories)
    #print(page)
    for category in categories:
        name = category.find('span')
        print(name.text)
        link = category.find('a')
        if link:
            print(link['href'])
    for sub_category in sub_categories:
        name = sub_category.find('span')
        print(name.text)
        link = sub_category.find('a')
        if link:
            print(link['href'])    
except Exception as e:
    print(e)
finally:
    browser.quit()
