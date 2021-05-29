from noise_remove import Noise_remover
from classes.deadline import Deadline
import json
import re
from FileManager import FileManager

class retriever:
    DEADLINE_PATTERN = '(?P<date>(May|March|June)\s[0-9]{1,2})\s([^.]*)[Dd]eadline\s(?P<deadline_title>[^.]+)\.'
    SEMESTER_PATTERN = '(?P<semester>(Fall|Spring|Summer|Winter)\s20[0-9]{1,2})'

    def __init__(self) -> None:
        self.data = []
    
    def retrieve(self)-> None:
        self.data = FileManager.read_json('./json_files/source_data.json')
        main_contents = self.get_clear_content()
        for name, main_content in main_contents.items():
            self.retrieve_data(name, main_content)
        FileManager.write_json(self.data, "./json_files/output.json")

    def get_clear_content(self) -> dict:
        main_contents = {}
        nr = Noise_remover()
        for d in self.data:
            name = d['name']
            urls = d['urls']
            for url in urls:
                main_content = nr.noise_remove(url)
                main_contents[name] = main_content
        return main_contents

    def retrieve_data(self, name: str, cleaned_texts : str):      
        pattern = re.compile(self.DEADLINE_PATTERN)
        found_university = self.find_data_by_name(name)
        if not found_university:
            raise TypeError(name+ 'university is Null')
        
        for match in pattern.finditer(cleaned_texts):
            # print('\n', match.group())
            # print(match.group('deadline_title'))
            # print(match.group('date'))
            deadline = Deadline(match.group('deadline_title'), match.group('date'))
            if 'deadlines' not in found_university.keys():
                found_university['deadlines'] = []
            found_university['deadlines'].append(deadline)

        pattern = re.compile(self.SEMESTER_PATTERN)
        matches = re.search(self.SEMESTER_PATTERN, cleaned_texts)
        if matches:
            found_university['semester'] = matches.group('semester')
    
    def find_data_by_name(self, name : str) -> dict:
        for university_data in self.data:
            if university_data["name"] == name:
                return university_data
        return None

r = retriever()
r.retrieve()