from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote
import time

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-dev-shm-usage") # add this line

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/scrape")
def scrape():
    url = request.args.get("url")
    escaped_url = quote(url, safe=':/?&=')
    print(escaped_url)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(escaped_url)
    time.sleep(2)  # add delay after getting URL
    soup = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(1)  # add delay after getting page source
    product_title = soup.find("h1", class_="product_title")
    title = product_title.text.strip() if product_title else ""
    images_view_wrap = soup.find("il", class_="swiper-slide-visible")
    images = []
    if images_view_wrap:
        for img in images_view_wrap.find_all("img"):
            src = img.get("src")
            if "jpg_50x50" in src:
                src = src.replace("jpg_50x50", "jpg")
                images.append(src)

    print(title, images)
    return jsonify({"Title": title,"Images": images})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
