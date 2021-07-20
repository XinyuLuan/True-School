from flask import Flask, redirect, url_for, render_template
import json

app = Flask(__name__)


@app.route("/")
def hello():
    # filename = os.path.join(app.static_folder, 'file://people.json')
    f = open('./json_files/uc_data.json')
    text = json.load(f)  # 将json格式的字符转换为dict，从文件中读取
    print(text)
    print(type(text))
    f.close()
    # return render_template('hello.html', json_text = json.dumps(text))
    return render_template('index.html', json_text=text)
    # return render_template('index.html')


@app.route("/CA")
def CA():
    f = open('./json_files/output.json')
    text = json.load(f)  # 将json格式的字符转换为dict，从文件中读取
    print(text)
    print(type(text))
    return render_template('CA.html', jsont=text)
    f.close()
    # return render_template('index.html')


@app.route("/CalTech")
def CalTech():
    f = open('./json_files/output.json')
    text = json.load(f)  # 将json格式的字符转换为dict，从文件中读取
    print(text)
    print(type(text))
    f.close()
    return render_template('caltech.html', jsont=text)


@app.route("/UCLA")
def UCLA():
    f = open('./json_files/output.json')
    text = json.load(f)  # 将json格式的字符转换为dict，从文件中读取
    print(text)
    print(type(text))
    f.close()
    return render_template('UCLA.html', jsont=text)


@app.route("/v1")
def v1():
    f = open('./json_files/output.json')
    text = json.load(f)
    print(text)
    print(type(text))
    f.close()
    return render_template('v1.html', jsonv=text)


if __name__ == "__main__":
    app.run(debug=True)
