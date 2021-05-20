from flask import Flask, redirect, url_for, render_template
import os
import json

'''
send data to javascript in flask:
https://stackoverflow.com/questions/62906140/displaying-json-in-the-html-using-flask-and-local-json-file

html with template folder:
https://stackoverflow.com/questions/23327293/flask-raises-templatenotfound-error-even-though-template-file-exists

Kill port:
https://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use

'''

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello! this is the main page <h1>HELLO</h1>"

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/hello")
def hello():
    # filename = os.path.join(app.static_folder, 'file://people.json')
    f = open('people.json')
    text = json.load(f)
    print(text)
    print(type(text))
    f.close()
    # return render_template('hello.html', json_text = json.dumps(text))
    return render_template('hello.html', json_text = text)

@app.route("/admin")
def admin():
    return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run()