from typing import List, Pattern
from bs4 import BeautifulSoup
from urllib import request
import requests as req
from urllib.request import urlopen
import nltk

class Noise_remover:
    prefix_tags = [0]

    def __init__(self) -> None:
        # self.pages = []
        # self.uc_data = {'name' : 'University of California', 'deadlines' : []}
        pass
    
    def noise_remove(self, url : str) -> str:
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
            for b in body.select("img"):
                b.extract()
            for b in body.select("image"):
                b.extract()
            for b in body.select("input"):
                b.extract()
            for b in body.select("a"):
                b.extract()
            for b in body.select("footer"):
                b.extract()
            for b in body.select("style"):
                b.extract()
            for b in body.find_all("div", {"class" : "uw-footer"}):
                b.extract()
            
        
        # print("body: ", body)   # body type:  <class 'bs4.element.Tag'>

        body_string_quotes_cleaned = self.clean_quotes(str(body))
        # Error: TypeError: expected string or bytes-like object
        # The problem is that you have None (NA)
        # body.dropna(inplace=True)
        body_tokens = nltk.tokenize.word_tokenize(body_string_quotes_cleaned)
        # print('----------------- body token: ----------------', body_tokens)

        body_tokens_clean = self.customize_tokenizer(body_tokens)
        body_tokens_clean = self.clean_useless_tag(body_tokens_clean)
        # print('***************** body token clean: ****************', body_tokens_clean)

        self.prefix_tags = self.prefix_sum_tags(body_tokens_clean)
        # print(self.prefix_tags)

        i, j = self.noise_remove_for_one(body_tokens_clean)
        # print("i: " + str(i))
        # print("j: " + str(j))
        # print(body_tokens_clean[i : j + 1])
        
        main_contents_list = body_tokens_clean[i : j + 1]
        joined = " "
        main_contents = joined.join(main_contents_list)
        return main_contents

    def clean_useless_tag(self, tokens) -> List: # new
        new_tokens = []
        for token in tokens:
            if "span" in token and '<' in token:
                continue
            if "li" in token and '<' in token:
                continue
            if "ul" in token and '<' in token:
                continue
            if "strong" in token and '<' in token:
                continue
            if "polygon" in token and '<' in token:
                continue
            if "path" in token and '<' in token:
                continue
            if "rect" in token and '<' in token:
                continue
            new_tokens.append(token)
        return new_tokens

    def prefix_sum_tags(self, tokens) -> List:  # 1
        prefix_tags = [0]
        for token in tokens:
            if '<' in token:
                prefix_tags.append(prefix_tags[-1] + 1)
            else:
                prefix_tags.append(prefix_tags[-1])
        return prefix_tags
        # self.prefix_tags = prefix_tags

    def  noise_remove_for_one(self, tokens):    # 2
        prefix_tags = self.prefix_tags
        # print('prefix_tags: ', prefix_tags)
        maxi = maxj = -1
        max = 0

        for i in range(len(tokens) - 1):
            for j in range(i + 1, len(tokens)):
                # print(prefix_tags[i])
                # print((j - i + 1) - (prefix_tags[j + 1] - prefix_tags[i]))
                # print(prefix_tags[-1] - prefix_tags[j + 1])
                sum = prefix_tags[i] + ((j - i + 1) - (prefix_tags[j + 1] - prefix_tags[i])) + (prefix_tags[-1] - prefix_tags[j + 1])
                
                if sum > max:
                    maxi = i
                    maxj = j
                    max = sum
        return (maxi, maxj)
    
    def customize_tokenizer(self, tokens):
        new_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if tokens[i] == '<':
                i += 1
                while tokens[i] != '>':
                    token += ' ' + tokens[i]
                    i += 1
                token += '>'
            i += 1
            new_tokens.append(token)
        return new_tokens
    
    def clean_quotes(self, text):
        left_single_quote = "‘"
        right_single_quote = "’"
        left_double_quote = "“"
        right_double_quote = "”"
        text = text.replace(left_single_quote, "'")
        text = text.replace(right_single_quote, "'")
        text = text.replace(left_double_quote, "((")
        text = text.replace(right_double_quote, "))")

        return text
    
    def get_url_from_file(self, file_path) -> List:
        with open(file_path, "r") as csv_file:
            data = csv_file.read()
            # print(data)
            # print(type(data))
            return data.split('\n')[1:-1]

    def stem_texts(self, old_texts : List) -> List:
        ps = nltk.PorterStemmer()
        stems = []
        for token in old_texts:
            if '<' in token and '>' in token:
                stems.append(token)
            else:
                stems.append(ps.stem(token))
            
        return stems


    
    # def find_a_keyword_and_retrieve_relative(self, keyword : str, tokens : List) -> str:
    #     start = -1
        
    #     while keyword in tokens[start + 1:]:
    #         index  = tokens[start + 1:].index(keyword)
    #         tag_index = -1
    #         for i in range(index,-1,-1):
    #             if '<' in tokens[i] and '>' in tokens[i]:
    #                 tag_index = i
    #                 break
    #         if tag_index == -1:
    #             raise Exception("No tags before " + tokens[index])
    #         # whole_sentense_with_tags = self.get_full_sentence_with_tags(tokens, tag_index)
    #         print(" tag_index", tag_index, " tag", tokens[tag_index], "keyword:", keyword)
    #         start = tag_index

    def extract_text(self, tokens : List) -> List:      # 3
        texts = []
        for token in tokens:
            if '<' in token and '>' in token:
                continue
            texts.append(token)
        return texts
'''
    def retrieve_data(self, cleaned_texts : str):       # 4
        pattern = re.compile(self.DEADLINE_PATTERN)
        
        for match in pattern.finditer(cleaned_texts):
            # print('\n', match.group())
            # print(match.group('deadline_title'))
            # print(match.group('date'))
            deadline = self.Deadline(match.group('deadline_title'), match.group('date'))
            self.uc_data['deadlines'].append(deadline)

        pattern = re.compile(self.SEMESTER_PATTERN)
        matches = re.search(self.SEMESTER_PATTERN, cleaned_texts)
        print('\nsemester:', matches.group())
        if matches:
            self.uc_data['semester'] = matches.group('semester')
        
        return self.uc_data
    
    def convert_to_json(self):                          # 5
        jsonString = json.dumps(self.uc_data, default=str, indent=4)
        print(jsonString)
        jsonFile = open("uc_data.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()
'''
    # def retri_semester(self, cleaned_str: str):
    #     semesters=[]
    #     pattern='(?P<season>[Ss]pring|[Ff]all|[Ss]ummer)\s(?P<year>202[0-9])'
    #     re_pattern = re.compile(pattern)
    #     l1=[]
    #     set1=set()
    #     for match in re_pattern.finditer(cleaned_str):
    #         # semesters.append(match)
    #         # print(match.group('season'))
    #         # print(match.group('year'))
    #         # semester=self.Semester(match.group('season'), match.group('year'))
    #         l1.append([match.group('season'), match.group('year')])
    #         print(l1)
    #     for i in range(len(l1)):
    #         if l1[i][0].endswith("all"):
    #             l1[i][0]='Fall'
    #             t1=(l1[i][0],l1[i][1])
    #             set1.add(t1)
    #     l2=list(set1)
    #     for i in range(len(l2)):
    #         semester = self.Semester(l2[i][0], l2[i][1])
    #         self.uc_data['semesters'].append(semester)
    #         print(self.uc_data['semesters'])

    #         # self.uc_data['semesters'].append(semester)
    #     return semesters
        
'''
nr  = Noise_remover()
# nr.get_url_from_file('visited/pages.csv')
# nr.get_clear_content()

# test_seed = "https://admission.universityofcalifornia.edu/"
# test_seed = "https://grad.uw.edu/admission/find-a-program/program-detail/#!?progid=709"
# test_seed = "https://collegedunia.com/usa/college/1813-california-institute-of-technology-pasadena/admission"
test_seed = "https://www.admissions.caltech.edu/apply/first-year-freshman-applicants/application-requirements"
cleaned_tag_string = nr.noise_remove(test_seed)
# print(cleaned_tag_string)
# nr.find_a_keyword_and_retrieve_relative('Deadline', cleaned_tag_string)
texts = nr.extract_text(cleaned_tag_string)
# print(texts)
joined = " "
joined = joined.join(texts)
print(joined)

# '^[Dd]eadline.*[0-9]+$'
# '(May|March)\s[0-9]{1,2}\s([^,]+)\.'
# pattern = re.compile('^[Dd]eadline')

# https://superuser.com/questions/266732/matching-only-the-first-occurrence-in-a-line-with-regex
# matches = re.search('(May|March)\s[0-9]{1,2}\s([^.]*)Deadline(?P<name>[^.]+)\.', joined)
# print(matches)

# *
# print()
# data = nr.retrieve_data(joined)
# print(data)
# nr.convert_to_json()
'''

# semester = nr.retri_semester(joined)
# print(semester)
# pattern = re.compile(r'(?P<date>(May|March|June)\s[0-9]{1,2})\s([^.]*)Deadline\s(?P<name>[^.]+)\.')

# for match in pattern.finditer(joined):
#     print('\n', match.group())
#     print(match.group('name'))
#     print(match.group('date'))
# if matches.groups():

# else:
#     print("No deadline")


# nr.stem_texts(texts)
# print(texts)