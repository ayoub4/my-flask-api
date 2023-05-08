import sys
import platform

import requests
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time

app = Flask(__name__)

chrome_options = Options()

chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage") # add this line

if platform.system() == 'Windows':
    chromedriver_path = 'chromedriver.exe'
else:
    chromedriver_path = 'chromedriver'

service = Service(chromedriver_path)

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/scrape")
def scrape():
    url = request.args.get("url")
    escaped_url = quote(url, safe=':/?&=')

    # create a session object
    session = requests.Session()
    session.headers.update({'ali_apache_track': 'mt=1|ms=|mid=fr927446943znpae'})

    # make the request with the session object
    response = session.get(escaped_url)

    # parse the response using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")
    product_title = soup.find("h1", class_="product-title-text")
    title = product_title.text.strip() if product_title else ""
    images_view_wrap = soup.find("div", class_="images-view-wrap")
    images = []
    if images_view_wrap:
        for img in images_view_wrap.find_all("img"):
            src = img.get("src")
            if "jpg_50x50" in src:
                src = src.replace("jpg_50x50", "jpg")
                images.append(src)

    return jsonify({"Title": title, "Images": images})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
