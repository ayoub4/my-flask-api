import random
import string
import socket
import time

from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")  # run in headless mode so no browser window is opened
chrome_options.add_argument("--no-sandbox")


@app.route('/')
def index():
    # Generate a random string of length 10
    random_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f"Random text: {random_text}"


@app.route('/scrape')
def scrape():
    url = request.args.get('url')

    # Set timeout to 6 minutes (360 seconds)
    socket.setdefaulttimeout(360)

    # Create the Chrome driver instance
    driver = webdriver.Chrome(options=chrome_options)

    # Clear cookies
    driver.delete_all_cookies()

    # Initialize variables
    title = ''
    images = []

    while not title and not images:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the product title
        product_title = soup.find("h1", class_="product-title-text")
        title = product_title.text.strip() if product_title else ""

        # Find all the images inside the "images-view-wrap" class
        images_view_wrap = soup.find("div", class_="images-view-wrap")
        if images_view_wrap:
            for img in images_view_wrap.find_all("img"):
                src = img.get("src")
                if "jpg_50x50" in src:
                    src = src.replace("jpg_50x50", "jpg")
                images.append(src)

        # Sleep for a random amount of time before trying again (between 1 and 5 seconds)
        time.sleep(random.uniform(1, 5))

    # Close the Chrome driver instance
    driver.quit()

    return {
        'images': images,
        'title': title
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
