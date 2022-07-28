import requests
from bs4 import BeautifulSoup as bs

class BBC:
    def __init__(self, url):
        article = requests.get(url)
        self.soup = bs(article.content, "html.parser")
        self.categories = self.get_categories()
    def get_categories(self) -> list:

        body = self.soup.find(property="articleBody")
        return [p.text for p in body.find_all("p")]