from typing import ItemsView
from noise_remove import Noise_remover
from classes.deadline import Deadline
import requests as req
from urllib.request import urlopen
import json
import re
from FileManager import FileManager
from bs4 import BeautifulSoup
from collegedunia_helper import Collegedunia


class retriever:
    DEADLINE_PATTERN = '(?P<date>(May|March|June)\s[0-9]{1,2})\s([^.]*)[Dd]eadline\s(?P<deadline_title>[^.]+)\.'
    SEMESTER_PATTERN = '(?P<semester>(Fall|Spring|Summer|Winter)\s20[0-9]{1,2})'

    class Profile:
        def __init__(self, items, values) -> None:
            self.items = items
            self.values = values

        def __str__(self) -> str:
            return '{} : {}'.format(self.items, self.values)

        def __repr__(self) -> str:
            return '{} : {}'.format(self.items, self.values)

    def __init__(self) -> None:
        self.data = {}

    def retrieve(self) -> None:
        self.data = FileManager.read_json('./json_files/source_data.json')
        main_contents = self.get_clear_content()
        for name, main_content in main_contents.items():
            self.retrieve_data(name, main_content)
        FileManager.write_json(self.data, "./json_files/output.json")

    def get_clear_content(self) -> dict:
        main_contents = {}
        nr = Noise_remover()
        for d in self.data.values():
            name = d['name']
            urls = d['urls']
            for url in urls:
                main_content = nr.noise_remove(url)
                main_contents[name] = main_content
        return main_contents

    def retrieve_data(self, name: str, cleaned_texts: str):
        pattern = re.compile(self.DEADLINE_PATTERN)
        found_university = self.find_data_by_name(name)
        if not found_university:
            raise TypeError(name + 'university is Null')

        for match in pattern.finditer(cleaned_texts):
            # print('\n', match.group())
            # print(match.group('deadline_title'))
            # print(match.group('date'))
            deadline = Deadline(match.group(
                'deadline_title'), match.group('date'))
            if 'deadlines' not in found_university.keys():
                found_university['deadlines'] = []
            found_university['deadlines'].append(deadline)

        pattern = re.compile(self.SEMESTER_PATTERN)
        matches = re.search(self.SEMESTER_PATTERN, cleaned_texts)
        if matches:
            found_university['semester'] = matches.group('semester')

    def find_data_by_name(self, name: str) -> dict:
        for university_data in self.data:
            if university_data["name"] == name:
                return university_data
        return None

    def retrieve_table(self, name: str):
        self.data = FileManager.read_json('./json_files/source_data.json')
        c = Collegedunia()

        replace_list = ['\r', '\t', '\n']
        for college in self.data:
            college_url = self.data[college]["urls"][0]
            # print(college_url)
            # caltech_data = self.data["Cal Tech"]["urls"][0]
            tablelist = c.get_table_components(
                college_url)    # a list of table

            # print("----- table title ----\n", tablelist)
            for j in range(len(tablelist)):
                # get the title of tables
                titleoftables = tablelist[j][0].get_text()
                descriptionOfTable = tablelist[j][1].get_text()

                # if titleoftables not in self.data:
                #     self.data[titleoftables] = []

                # the index of 2 is the highlight table
                table = tablelist[j][2]

                tabledata = []  # store one table's data in a 2d array

                while table.find('tr'):
                    row = table.find('tr')
                    tabledata.append([])
                    tag = ""
                    if row.find('td'):
                        tag = 'td'
                    elif row.find('th'):
                        tag = 'th'

                    if tag == "":
                        continue

                    for i in range(len(row.select(tag))):
                        value = row.select(tag)[i].get_text()
                        for replacedstr in replace_list:
                            value = value.replace(replacedstr, "")
                        tabledata[-1].append(value)

                    curr_row = table.find('tr')
                    curr_row.extract()

                if "tables" not in self.data[college]:
                    self.data[college]["tables"] = []
                    # if titleoftables not in self.data["Cal Tech"]["tables"]:
                    #     self.data["Cal Tech"][titleoftables] = []
                # self.data["Cal Tech"]["tables"].append({titleoftables:tabledata})
                self.data[college]["tables"].append({"title": titleoftables,
                                                     # "description" : descriptionOfTable,
                                                     "data": tabledata})  # [titleoftables].append(tabledata)
                # print(self.data)

        FileManager.write_json(self.data, "./json_files/output.json")


seed = "https://collegedunia.com/usa/college/1813-california-institute-of-technology-pasadena/admission"
r = retriever()
table2 = r.retrieve_table(seed)
