from noise_remove import Noise_remover
from typing import List, Pattern
from bs4 import BeautifulSoup
from urllib import request
import requests as req
from urllib.request import urlopen
import nltk
import re
from noise_remove import Noise_remover
from FileManager import FileManager


class Collegedunia():
    prefix_tags = [0]

    def __init__(self) -> None:
        self.noise_remove = Noise_remover()
        # self.retrieve = retriever()
        pass

    def admission_noise_remove(self):
        admission_url = self.get_admission_url(url)

        main_content = self.noise_remove.noise_remove(admission_url)
        # print("----- main content ----", main_content)

    def get_body(self, url: str):
        if url.endswith('.html'):
            # Parse html file (e.g., https://www.test.com/main.html)
            html = req.get(url).content.decode('utf-8')
        else:
            # Parse regular URL (e.g., https://www.techcruntch.com)
            html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        body = soup.find("body")
        return body

    def get_admission_url(self, url: str):
        body = self.get_body(url)
        if body is not None:
            nav = body.find_all("nav")
            # This returns the <a> element
            for n in nav:
                a_tag = n.find(
                    'a',
                    text=re.compile(".*ADMISSION.*")
                )
                href = a_tag['href']
                href = 'https://' + self.extract_host_name(url) + href
        return href

    def get_table_components(self, url: str):
        body = self.get_body(url)

        main_contains = body.find_all(
            'div', attrs={'class': re.compile('cdcms_.*')})
        tablelist = []
        for i in range(len(main_contains)):
            while main_contains[i].find('table'):
                h2 = main_contains[i].find('h2')
                h3 = main_contains[i].find('h3')

                if h2:
                    title = h2
                elif h3:
                    title = h3

                p = main_contains[i].find('p')
                # print(h2)
                # print(p)
                # table = main_contains[i].find(lambda tag:tag.name == 'table')
                table = main_contains[i].find('table')
                tablelist.append([title, p, table])
                p.extract()
                table.extract()
            # div.extract()
        return tablelist
        # tables = main_contains[0].find_all('table')
        # print(tables)

    def extract_host_name(self, page_url: str) -> str:
        url_pattern = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
        return re.search(url_pattern, page_url).group('host')


url = "https://collegedunia.com/usa/college/2074-stanford-university-stanford/admission"
c = Collegedunia()
# c.admission_noise_remove()
c.get_table_components(url)
# print(admission_url)
