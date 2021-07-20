import json 

class FileManager:

    @staticmethod
    def read_json(json_file_name: str):
        # Opening JSON file
        f = open(json_file_name,)
        
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        
        # Iterating through the json
        # list
        for i in data:
            print(i)
        
        # Closing file
        f.close()
        return data

    @staticmethod
    def write_json(data : dict, json_file_name : str) -> None:                         
        jsonString = json.dumps(data, default=str, indent=4)
        # print(jsonString)
        jsonFile = open(json_file_name, "w")
        jsonFile.write(jsonString)
        jsonFile.close()

# s = source()
# s.load_source()
