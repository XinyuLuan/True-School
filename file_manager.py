import os
import re
import pandas as pd

class FileManager: 

    @staticmethod
    def save_visited_result(visited_page_set : set) -> None:
        file_name = '/visited/pages.csv'
        visited_pd = pd.DataFrame(list(visited_page_set), columns=['visited_url'])
        visited_pd.to_csv(file_name, index=False)
        # for vp in visited_page_set:
        #     visited_pd.add

