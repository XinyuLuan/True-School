from flask import Flask, redirect, url_for, render_template
import json

app = Flask(__name__)

@app.route("/")
def hello():
    # filename = os.path.join(app.static_folder, 'file://people.json')
    f = open('/json_files/uc_data.json')
    text = json.load(f)
    print(text)
    print(type(text))
    f.close()
    # return render_template('hello.html', json_text = json.dumps(text))
    return render_template('index.html', json_text = text)
    # return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)