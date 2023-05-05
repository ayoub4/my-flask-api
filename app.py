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
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")  # set user agent


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
    c = 0
    proxies = []
    with open("proxies.txt", "r") as f:
        proxies = f.readlines()

    while True:
        # Rotate through all proxies from proxies.txt file
        proxy = proxies[c % len(proxies)].strip()
        proxy_options = {
            "proxy": {
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy,
                "noProxy": None,
                "proxyType": "MANUAL",
                "class": "org.openqa.selenium.Proxy",
                "autodetect": False
            }
        }
        chrome_options.add_experimental_option("proxy", proxy_options)

        driver = webdriver.Chrome(options=chrome_options)

        # Clear cookies
        driver.delete_all_cookies()
        # Try to scrape the page
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Find the product title
        product_title = soup.find("h1", class_="product-title-text")
        title = product_title.text.strip() if product_title else ""

        # Find all the images inside the "images-view-wrap" class
        images_view_wrap = soup.find("div", class_="images-view-wrap")
        images = []
        if images_view_wrap:
            for img in images_view_wrap.find_all("img"):
                src = img.get("src")
                if "jpg_50x50" in src:
                    src = src.replace("jpg_50x50", "jpg")
                images.append(src)

        # If the data is not found, wait for a few seconds and try again
        if not title and not images:
            print(c)
            c = c + 1
            time.sleep(5)  # Wait for 5 seconds before retrying
            driver.quit()  # Close the Chrome driver instance
        else:
            driver.quit()  # Close the Chrome driver instance
            return {
                'images': images,
                'title': title
            }

        # Increment the counter to rotate through proxies
        c = c + 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
