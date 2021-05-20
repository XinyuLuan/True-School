import os
import webbrowser
import json

path = os.path.abspath('hello.html')
url = 'file://' + path

# with open(path, 'w') as f:
#     f.write(html)
f = open('people.json')
text = json.load(f)
print(text)

hello = open("hello.html", "r").read().format(json_text = text)
webbrowser.open(url)

f.close()