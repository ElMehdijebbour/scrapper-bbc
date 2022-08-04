from re import A
import scrapy
import pandas as pd

from scrapperBBC.items import ScrapperbbcItem
from dateutil import parser
from shutil import which
from scrapy_selenium import SeleniumRequest
from dateutil import parser
import datetime
import pytz


#Starting Scrapper

class BBCSpider(scrapy.Spider):
    name = "bbc"
    def __init__(self, name=None, **kwargs):
        self.is_around_bbc_scraped=False


    def start_requests(self):
        urls = [
            'https://www.bbc.com/news',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        article_item=ScrapperbbcItem()
        categories=response.css('.nw-c-nav__wide-menuitem-container')
        for category in categories :
            #crawling to categories to scrappe
            selected_category_url=response.urljoin(category.css('a ::attr(href)').get())
            #selected_category_name=category.css('a span ::text').get()
            article_item['menu']=category.css('a span ::text').get()

            request=scrapy.Request(
                url=selected_category_url, callback=self.parse_category, dont_filter=True,meta=article_item)
            yield request


    def parse_category(self,response):
        article_item=response.meta
        sub_categories=response.css('.nw-c-nav__wide-secondary__title')
        sub_categories.extend(response.css('.nw-c-nav__secondary-menuitem-container'))
        if  sub_categories:
             #main sub exists
            for sub_category in sub_categories:
                    #selected_sub_category_name= sub_category.css('a span ::text').get()
                    selected_sub_category_url=response.urljoin(sub_category.css('a ::attr(href)').get())
                    #article_item["submenu"]=sub_category.css('a span ::text').get()
                    request=scrapy.Request(
                        url=selected_sub_category_url, callback=self.parse_sub_category,
                         dont_filter=True,meta=article_item)
                    yield request

        else: 
           
            #no sub category then category name is sub category name
            selected_sub_category_url=response.request.url
            #article_item["submenu"]=article_item["menu"]
            request=scrapy.Request(
                        url=selected_sub_category_url, callback=self.parse_sub_category,
                         dont_filter=True,meta=article_item)

            yield request
        
    def parse_sub_category(self, response):
        article_item=response.meta
        # around_bbc_section=response.css('.nw-c-around-the-bbc')
        # around_bbc_articles=around_bbc_section.css('.gs-c-promo')
        # for around_bbc_article in around_bbc_articles:
        #             article_url=response.urljoin(around_bbc_article.css('.gs-c-promo-heading ::attr(href)').get())
        #             #article_menu=article_menu
        #             #article_subtitle=around_bbc_article.css('.gs-c-promo-summary::text').get(),
        #             article_item["title"]=around_bbc_article.css('.gs-c-promo-heading h3::text').get(),
        #             request=SeleniumRequest(
        #                     url=article_url,
        #                     callback=self.parse_article,
        #                     dont_filter=True,meta=article_item,)
        #             yield request      
        
        # if not self.is_around_bbc_scraped:
        #     body_articles_section=response.xpath('//*[@id="index-page"]')
        #     body_articles_articles=body_articles_section.css('.gs-c-promo')
        #     for body_article in body_articles_articles:
        #                 article_url=response.urljoin(body_article.css('.gs-c-promo-heading ::attr(href)').get())
        #                 article_menu=article_menu
        #                 article_subtitle=body_article.css('.gs-c-promo-summary::text').get(),
        #                 article_title=body_article.css('.gs-c-promo-heading h3::text').get(),
        #                 request=scrapy.Request(article_url, callback=self.parse_article, dont_filter=True,
        #                 cb_kwargs=dict(article_url=article_url,article_menu=article_menu,article_title=article_title,article_subtitle=article_subtitle,article_submenu=article_submenu))
        #                 self.is_around_bbc_scraped=True
        #                 yield request
        for i in range(0,2):
            latest_articles_section=response.xpath('//*[@id="lx-stream"]/div[1]/ol')
            latest_articles_articles=latest_articles_section.css('.qa-post')              
            for latest_article in latest_articles_articles:
                        article_url=response.urljoin(latest_article.css('.qa-story-cta-link ::attr(href)').get())
                        #article_menu=article_menu
                        #article_subtitle=latest_article.css('.lx-stream-related-story--summary::text').get(),
                        #article_title=latest_article.css('.lx-stream-post__header-text ::text').get(),
                        #article_item["subtitle"]=latest_article.css('.lx-stream-related-story--summary::text').get(),
                        article_item["title"]=latest_article.css('.lx-stream-post__header-text ::text').get(),
                        #article_item["url"]=article_url
                        request=SeleniumRequest(
                            url=article_url,
                            callback=self.parse_article,
                            dont_filter=True,meta=article_item,)
                        yield request    
            
        #     response.request.meta['driver'].getElementsByClassName("lx-pagination__btn")[2].click()

            
        # for article in articles:
        #             #we extract what we can get from principal page
        #             article_url=response.urljoin(article.css('.gs-c-promo-heading ::attr(href)').get())
        #             article_menu=article_menu
        #             article_subtitle=article.css('.gs-c-promo-summary::text').get(),
        #             article_title=article.css('.gs-c-promo-heading h3::text').get(),
        #             request=scrapy.Request(article_url, callback=self.parse_article, dont_filter=True,
        #             cb_kwargs=dict(article_url=article_url,article_menu=article_menu,article_title=article_title,article_subtitle=article_subtitle,article_submenu=article_submenu))
        #             yield request    


    def parse_article(self,response):
        #article_item=ScrapperbbcItem()
        article_item=response.meta
        # text=[]
        # if response.css('.ssrcss-hmf8ql-BoldText::text').get() is not None:
        #     text.append(response.css('.ssrcss-hmf8ql-BoldText::text').get())
        # text.append(response.css('.ssrcss-7uxr49-RichTextContainer p::text').getall())
        # #second type of articles
        # if text is None:
        #     text=response.css(response.css('.article__intro ::text').get())
        #     text.extend(response.css('.body-text-card__text div ::text').getall())
            
        #items we can got from home page
        #article_item["text"]=text
        #article_item["url"]=article_url
        #article_item["menu"]=article_menu
        #article_item["subtitle"]=article_subtitle
        #article_item["title"]=article_title 
        #article_item["submenu"]=article_submenu
        #items we can get from article page
        #article_item["topic"]=list(set(response.css('.ssrcss-d7aixc-ClusterItems li a ::text').getall())),
        #article_item["images"]=response.css('.ssrcss-ab5fd8-StyledFigureContainer span img').xpath("@src").extract()

        #there is 2 types of articles

        #article_item["authors"]=response.css('.ssrcss-ugte5s-Contributor span strong ::text').get()
        # if article_item["authors"] is None:
        #     #check second type of articles
        #     article_item["authors"]=response.css('.author-unit__container a ::text').get()
        
        #geting data in ISO8061 format
        article_item["date"]=parser.parse(response.css('.ssrcss-1if1g9v-MetadataText time ::attr(datetime)').get())
        if article_item["date"] is None:
            if response.css('.author-unit__container span ::text').get() is not None:
                article_item["date"]=parser.parse(response.css('.author-unit__container span ::text').get())

        
        diffretiation = pytz.utc.localize(datetime.datetime.now()) -article_item["date"]


        if abs(diffretiation.days)<90:
             yield article_item

        