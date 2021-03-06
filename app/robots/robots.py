

from urllib.request import Request, urlopen

import time
import requests
import urllib.request
from app.admin import config
import lxml.html as html
from app.admin import db
import json



class PageContent():

    '''
    This is a Class for read Page Html Content for access Page with Xpath to extaract data with it 
    Here we have a Staticmethod
    This function have url argument and with request object we can get page Html content and decode 
    And Finaly returns a Html content

    '''
    @staticmethod
    def reading_Html(url):
        reformated_url = url.replace('%3A', ':')
        headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"}
        try:
            req = Request(reformated_url, headers=headers)
            fp = urllib.request.urlopen(req)
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            return mystr
        except Exception as e:  # This is the correct syntax
            print(f"Error ---> {e}")



class news_from_tejaratnews():
    '''
    Class for tejaratNews 

    we have a page link and pass it to staticmethod to return url link content 
    After we got content we can access to tags with xpath 

    Xpath returns a list object with the news content such as Title, News link, And Body of news 

    '''
    def __init__(self):
      url = "https://tejaratnews.com/category/%d8%a7%d9%82%d8%aa%d8%b5%d8%a7%d8%af-%d8%ac%d9%87%d8%a7%d9%86"
      self.content = PageContent()
      self.root = html.fromstring(self.content.reading_Html(url))


    '''
    news_title returns news Titles with Xpath 

    Xpath returns a list of Titles in the site 
    
    '''

    def news_title(self):
        title_lst = []
        title_lst = self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//div[contains(@class, 'news-media__title')]//a/text()")
        return title_lst

    '''
    news_link returns news Link with Xpath 

    Xpath returns a list of news links in the site 
    
    '''

    def news_link(self):
        link_news = []
        link_news = self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//div[contains(@class, 'news-media__title')]//a/@href")
        return link_news


    def news_content_and_image(self,links):
        news_image_lst = []
        news_content = []
        modifed_text = ""
        content = PageContent()
        for link in links:
            root = html.fromstring(content.reading_Html(link))
            image_lnk = root.xpath("//div[contains(@class,'gds-container')]//img/@data-src")
            news_image_lst.append(image_lnk[0])
            for text in root.xpath("//div[contains(@class, 'single-post-content')]/p[position() < last()]//text()"):
                modifed_text = modifed_text + str(text)
            modifed_text = modifed_text.lstrip()
            news_content.append(modifed_text[20:])
            modifed_text = ""
        return news_content ,news_image_lst



    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        news_content , news_image = self.news_content_and_image(self.news_link())
        data= {
            'news_image_link': news_image,
            'news_title': self.news_title(),
            'news_content': news_content,
            'news_link':self.news_link()
        }
        posts=[]
        data_len = self.news_title()
        for post in range(len(data_len)):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts
        



class news_from_tasnimnews():

    '''
    Class for tasnimnews 

    we have a page link and pass it to staticmethod to return url link content 
    After we got content we can access to tags with xpath 

    Xpath returns a list object with the news content such as Title, News link, And Body of news 

    '''


    '''
    
    Url for news section on tasnimnews 
    root is the return value of the staticmethod in PageContent
    
    '''

    def __init__(self):
      url = "https://www.tasnimnews.com/fa/service/85/%D8%A7%D9%82%D8%AA%D8%B5%D8%A7%D8%AF-%D8%AC%D9%87%D8%A7%D9%86"
      self.content = PageContent()
      self.root = html.fromstring(self.content.reading_Html(url))


    '''
    news_title returns news Titles with Xpath 

    Xpath returns a list of Titles in the site 
    
    '''

    def news_title(self):
        title_lst = []
        title_lst = self.root.xpath("//article[contains(@class, 'list-item')]//div[contains(@class,'col-md-8 col-xs-8 text-container vcenter')]//h2[contains(@class,'title')]/text()")
        return title_lst

    def news_content_and_image(self,links):
        news_image_lst = []
        news_content = []
        modifed_text = ""
        content = PageContent()
        for link in links:
            root = html.fromstring(content.reading_Html(link))
            image_lnk = root.xpath("//div//img[contains(@class,'img-responsive center_position ')][1]/@src")
            news_image_lst.append(image_lnk[0])
            for text in root.xpath("//article[contains(@class, 'single-news')]//p[position() < last()]//text()"):
                modifed_text = modifed_text + str(text)
            modifed_text = modifed_text.lstrip()
            news_content.append(modifed_text[23:])
            modifed_text = ""
        return news_content, news_image_lst


    '''
    news_link returns news Link with Xpath 

    Xpath returns a list of news links in the site 

    Because of Xpath returns a Incomplete link we need to add it with link_add string to links work properly

    '''

    def news_link(self):
        link_news = []
        link_news = self.root.xpath("//article[contains(@class, 'list-item')]/a/@href")
        modified_link = []
        link_add = "https://www.tasnimnews.com"
        for lnk in link_news:
            modified_link.append(str(link_add)+ str(lnk))
        return modified_link

    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        time.sleep(2)
        news_content, news_image = self.news_content_and_image(self.news_link())
        data= {
            'news_image_link': news_image,
            'news_title': self.news_title(),
            'news_content': news_content,
            'news_link':self.news_link()
        }
        posts=[]
        for post in range(len(self.news_title())):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts



class news_from_arzdigital():

    '''
    Class for arzdigital 

    we have a page link and pass it to staticmethod to return url link content 
    After we got content we can access to tags with xpath 

    Xpath returns a list object with the news content such as Title, News link, And Body of news 

    '''

    '''

    Url for news section on arzdigital 
    root is the return value of the staticmethod in PageContent
    
    '''
    def __init__(self):
      url = "https://arzdigital.com/category/news/world-news/"
      self.content = PageContent()
      self.root = html.fromstring(self.content.reading_Html(url))




    '''
    news_title returns news Titles with Xpath 

    Xpath returns a list of Titles in the site 
    
    '''
    def news_title(self):
        title_lst = []
        title_lst = self.root.xpath("//div[contains(@class, 'arz-row-sb arz-posts')]//h3[contains(@class,'arz-last-post-title')]/text()")
        return title_lst


        
    def news_content_and_image(self,links):
        news_image_lst = []
        news_content = []
        modifed_text = ""
        content = PageContent()
        for link in links:
            root = html.fromstring(content.reading_Html(link))
            image_lnk = root.xpath("//div[contains(@class,'arz-post-image')]/img/@src")
            news_image_lst.append(image_lnk[0])
            for text in root.xpath("//article//p[position() < last()]//text()"):
                modifed_text = modifed_text + str(text)
            news_content.append(modifed_text)
            modifed_text = ""
        return news_content, news_image_lst

    '''
    news_link returns news Link with Xpath 

    Xpath returns a list of news links in the site 
    
    '''

    def news_link(self):
        link_news = []
        link_news = self.root.xpath("//div[contains(@class, 'arz-row-sb arz-posts')]/a/@href")
        return link_news

    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        news_content, news_image = self.news_content_and_image(self.news_link())
        data= {
            'news_image_link': news_image,
            'news_title': self.news_title(),
            'news_content': news_content,
            'news_link':self.news_link()
        }
        posts=[]
        for post in range(len(self.news_title())):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts




class news_from_mehrnews():

    def __init__(self):
      url = "https://www.mehrnews.com/tag/%D9%88%DB%8C%D8%B1%D9%88%D8%B3+%DA%A9%D8%B1%D9%88%D9%86%D8%A7"
      self.news_link_url = "https://www.mehrnews.com"
      self.content = PageContent()
      self.root = html.fromstring(self.content.reading_Html(url))

    def news_title(self):
        news_title = []
        news_title = self.root.xpath("//section[contains(@class,'box list list-bordered list-thumbs thumbs-lg highlights no-header  _types')]/div/ul//li//h3/a/text()")
        return news_title

        
    def news_content_and_image(self,links):
        image_lnk_lst = []
        news_content = []
        modifed_text = ""
        content = PageContent()
        for link in links:
            root = html.fromstring(content.reading_Html(link))
            image_lnk = root.xpath("//figure[contains(@class,'item-img')]//img/@src")
            if image_lnk == []:
                image_lnk_lst.append("به لینک منبع مراجعه کنید!")
            else:
                image_lnk_lst.append(image_lnk[0])
            for text in root.xpath("//div[contains(@class,'item-body')]//p/text()"):
                modifed_text = modifed_text + str(text)
            modifed_text = modifed_text.lstrip()
            news_content.append(modifed_text[10:])
            modifed_text = ""
        return news_content, image_lnk_lst


    def news_link(self):
        news_link = []
        news_link = self.root.xpath("//section[contains(@class,'box list list-bordered list-thumbs thumbs-lg highlights no-header  _types')]/div/ul//li//h3/a/@href")
        modified_link = []
        for lnk in news_link:
            modified_link.append(str(self.news_link_url)+ str(lnk))
        return modified_link



    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        news_content, news_img = self.news_content_and_image(self.news_link())
        data= {
            'news_image_link': news_img,
            'news_title': self.news_title(),
            'news_content': news_content,
            'news_link':self.news_link()
        }
        posts=[]
        for post in range(len(self.news_title())):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts



class Bors_news():

    def __init__(self):
      url = "https://tejaratnews.com/category/%d8%a8%d8%a7%d8%b2%d8%a7%d8%b1/%d8%a8%d9%88%d8%b1%d8%b3?all=true"
      self.content = PageContent()
      self.root = html.fromstring(self.content.reading_Html(url))




    def news_title(self):
        news_title = []
        news_title = self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//div[contains(@class, 'news-media__title')]//a/text()")
        return news_title

    def news_content_and_image(self,links):
        image_lnk_lst = []
        news_content = []
        modifed_text = ""
        content = PageContent()
        for link in links:
            root = html.fromstring(content.reading_Html(link))
            image_lnk = root.xpath("//div[contains(@class,'gds-container')]//img/@data-src")
            image_lnk_lst.append(image_lnk[0])
            for text in root.xpath("//div[contains(@class, 'single-post-content')]/p[position() < last()]//text()"):
                modifed_text = modifed_text + str(text)
            modifed_text = modifed_text.lstrip()
            news_content.append(modifed_text[19:].replace("،",""))
            modifed_text = ""
        return news_content, image_lnk_lst



    def news_link(self):
        link_news = []
        link_news = self.root.xpath("//article[contains(@class, 'news-media media news-media__row news-media__l')]//div[contains(@class, 'news-media__title')]//a/@href")
        return link_news



    '''
    returning a dictionary data for store in dataBase

    '''
    def getData(self):
        news_content , news_img = self.news_content_and_image(self.news_link())
        data= {
            'news_image_link':news_img,
            'news_title': self.news_title(),
            'news_content': news_content,
            'news_link':self.news_link()
        }
        posts=[]
        for post in range(len(self.news_title())):
            posts.append({"news_img_link":data['news_image_link'][post],"title":data['news_title'][post],"content":data['news_content'][post],"link":data['news_link'][post]})
        return posts




def get_all_data():
    tejarat_news = news_from_tejaratnews()
    data_tejart = tejarat_news.getData()  

    tasnim_news = news_from_tasnimnews()
    data_tasnim = tasnim_news.getData()  

    arzdigital_news = news_from_arzdigital()
    data_arzdigi = arzdigital_news.getData()  

    mehr_news = news_from_mehrnews()
    data_corona = mehr_news.getData() 

    Bors_news_data = Bors_news()
    data_bors = Bors_news_data.getData() 

    return data_tejart, data_tasnim, data_arzdigi, data_corona, data_bors  