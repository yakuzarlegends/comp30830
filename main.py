#!/usr/bin/env python3

from flask import Flask

from scraping.scraper import herewego

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

 
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=80)
