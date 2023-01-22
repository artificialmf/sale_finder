from flask import Flask, render_template, url_for, request, redirect
import requests
from bs4 import BeautifulSoup
        

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        search = request.form['request']
        print(search)
        return redirect('/')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)