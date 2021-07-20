from typing import List, Pattern
from bs4 import BeautifulSoup
from urllib import request
import requests as req
from urllib.request import urlopen
import nltk

class retriTable:
    prefix_tags = [0]

    def __init__(self) -> None:
        # self.pages = []
        # self.uc_data = {'name' : 'University of California', 'deadlines' : []}
        pass
    
    def retritable(self, url : str) -> str:
        if url.endswith('.html'):
            html = req.get(url).content.decode('utf-8') # Parse html file (e.g., https://www.test.com/main.html)
        else: 
            html = urlopen(url).read().decode('utf-8') # Parse regular URL (e.g., https://www.techcruntch.com)
        soup = BeautifulSoup(html, "html.parser")
        # soup = BeautifulSoup(html)
        # print(soup.prettify())
        body = soup.find("body")
        # print(body.get_text())

        if body is not None:
            # remove script
            for b in body.select("script"):
                b.extract()
            # remove image tags
            
                b.extract()
            for b in body.find_all("div", {"class" : "uw-footer"}):
                b.extract()
            
        tables = body.find_all("table")
        # print("******* table *******", tables)
        # print("body: ", body)   # body type:  <class 'bs4.element.Tag'>

        

        return main_contents
