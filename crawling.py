from typing import List
from urllib import request
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests as req
import re   # regular expression
import random
import pandas as pd

# from crawler.file_manager import FileManager

'''
TODO:
1. 把爬虫分为缩小到本网站内
2. 更深层爬虫
3. NLP
'''
class WebCrawler:
    to_be_visited_pages_queue = []
    to_be_visited_set = set()
    visited_page = set()
    page_limit = 5

    def __init__(self, seed_url, language = 'en') -> None:
        self.seed_path = self.split_seed_path(seed_url)
        self.to_be_visited_pages_queue = [seed_url]
        self.lang = language

    def crawl_new_page(self) -> None:
        while self.to_be_visited_pages_queue and len(self.visited_page) < self.page_limit:
            # try:
                # page_url = random.choices(self.to_be_visited_pages_queue)[0] # Pick a random page from the queue
                page_url = self.to_be_visited_pages_queue[0]
                print(page_url)
                self.to_be_visited_pages_queue.remove(page_url) # remove visited page from to be visited
                self.visited_page.add(page_url)
                # crawl all next level outlinks
                outlinks = self.crawl_outlinks(page_url)
                if not outlinks:
                    continue
                for outlink in outlinks:
                    if outlink in self.visited_page or not self.check_same_host(page_url, outlink) or outlink in self.to_be_visited_set:
                        continue
                    self.to_be_visited_set.add(outlink)
                    self.to_be_visited_pages_queue.append(outlink)
                print("Done to crawl: ", page_url)
                for idx, outlink in enumerate(self.to_be_visited_pages_queue):
                    print(idx, ":", outlink)
                    
            # except Exception as e:
            #     print(page_url, " get EXCEPTION", str(e))
            #     print(type(e))
        self.save_visited_result(self.visited_page)
        self.save_to_be_visit_result(self.to_be_visited_set)

    def crawl_outlinks(self, page_url: str) -> List:
        outlinks = None
        try:
            if page_url.endswith('.html'):
                html = req.get(page_url).content.decode('utf-8') # Parse html file (e.g., https://www.test.com/main.html)
            else: 
                html = urlopen(page_url).read().decode('utf-8') # Parse regular URL (e.g., https://www.techcruntch.com)

            # print("---- crawling down url -----")
            outlinks = self.collect_outlinks(page_url, html)
            outlinks = list(outlinks)
            for idx, outlink in enumerate(outlinks):
                outlinks[idx] = self.generate_outlinks_url(outlink)
            # print(idx, ":", outlinks[idx])
            
        except:
            pass

        return outlinks
        

    def collect_outlinks(self, page_url : str, html : str) -> set:
        if html is None:
            return None
        soup = BeautifulSoup(html, features='html.parser')
        all_a_tags = soup.find_all('a')
        all_a_tags = filter(lambda tag: tag.get('href') is not None, all_a_tags)
        all_href = {tag['href'] for tag in all_a_tags}
        all_href = {page_url + href if href.startswith('/') else href for href in all_href} # Append the link to current URL if it is a relative path
        return all_href

    def split_seed_path(self, page_url : str) -> List:
        return page_url.split('/')

    def generate_outlinks_url(self, outlink : str) -> str:
        previous_path = '../'
        num_of_previous_path = 2    # start with 2 because there are always 'https' and ''(empty string)
        while outlink.startswith(previous_path):
            num_of_previous_path += 1
            outlink = outlink[len(previous_path):]
            # print(outlink)
        
        new_outlink = ""
        if num_of_previous_path > 2:
            for i in range(num_of_previous_path):
                if self.seed_path[i] == 'how-to-apply':
                    continue
                new_outlink += self.seed_path[i] + '/'
        new_outlink += outlink

        # print('new outlink:', new_outlink)
        return new_outlink

    def extract_host_name(self, page_url: str) -> str:
        url_pattern = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
        return re.search(url_pattern, page_url).group('host')
    
    def check_same_host(self, page_url_one: str, page_url_two: str) -> bool:
        return self.extract_host_name(page_url_one) == self.extract_host_name(page_url_two)

    # @staticmethod
    def save_visited_result(self, visited_page_set : set) -> None:
        file_name = 'visited/pages.csv'
        visited_pd = pd.DataFrame(list(visited_page_set), columns=['visited_url'])
        visited_pd.to_csv(file_name, index=False)

    def save_to_be_visit_result(self, outlinks : set) -> None:
        file_name = 'tobevisited/pages.csv'
        visited_pd = pd.DataFrame(list(outlinks), columns=['to_be_visited_url'])
        visited_pd.to_csv(file_name)
    
# seed = "https://admission.universityofcalifornia.edu/how-to-apply/applying-as-a-freshman/"
# seed = "https://admission.universityofcalifornia.edu/how-to-apply/"
# seed = "https://www.admissions.caltech.edu/apply/first-year-freshman-applicants/application-requirements"
# seed = "https://admission.universityofcalifornia.edu/campuses-majors/berkeley/freshman-admit-data.html"
seed = "https://collegedunia.com/usa/college/1042-university-of-washington-bothell-campus-bothell"
webCrawler = WebCrawler(seed)
webCrawler.crawl_new_page() 

def generate_outlink_url_tester():
    seed = "https://admission.universityofcalifornia.edu/how-to-apply/applying-as-a-freshman/"
    webCrawler = WebCrawler(seed)
    print("seed path:", webCrawler.seed_path)
    webCrawler.crawl_new_page() 
    outlink = "../../admission-requirements/transfer-requirements/transfer-pathways/index.html"
    webCrawler.generate_outlinks_url(outlink)

    outlink2 = "../applying-as-a-transfer/dates-and-deadlines.html"
    webCrawler.generate_outlinks_url(outlink2)

    outlink3 = "http://admissions.berkeley.edu/transferstudents"
    print(webCrawler.generate_outlinks_url(outlink3))

# generate_outlink_url_tester()









# seed = "https://baike.baidu.com/item/%E4%BA%9A%E6%9C%B5%E9%85%92%E5%BA%97/9000409"
# seed = "https://morvanzhou.github.io/static/scraping/basic-structure.html"
# origin = "https://baike.baidu.com"
# seed = origin + "/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB/5162711"


#if has Chinese, apply decode()
# html = urlopen(seed).read().decode('utf-8')
# print(html)

# print('body --------- ')
# soup = BeautifulSoup(html, features='lxml')
# # print(soup.a)

# print('a --------- ')
# soup = BeautifulSoup(html, features='lxml')
# # a tag 表示 里面可能会有link, href=True排除所有没有href的 a tag
# all_tag_a = soup.find_all('a', {"target": "_blank", "href": re.compile("/item/(%.{2})+$")})
# # print(all_tag_a)
# # 要拿到真正的link 我们需要从<a href="link"> 拿到 href的属性
# # soup.a.attrs 读取里面会是一个dict

# all_href = []
# for l in all_tag_a:
#     # if not l['href'] or re.search(r"^http:", l['href']) is None :
#     #     continue;
#     all_href.append(origin + l['href'])

# print('\nall href')
# print(all_href)





# url_pattern = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'
# x = re.search(url_pattern, seed).group('host')
# print(x)
