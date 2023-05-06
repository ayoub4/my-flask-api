import socket
import time
from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

app = Flask(__name__)

firefox_options = Options()
firefox_options.headless = True  # run in headless mode so no browser window is opened
firefox_options.add_argument("--no-sandbox")

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

    # Create the Firefox driver instance
    c = 0

    while True:
        try:
            ua = UserAgent()
            profile = webdriver.FirefoxProfile()
            profile.set_preference("general.useragent.override", ua.random)
            driver = webdriver.Firefox(firefox_profile=profile, options=firefox_options)

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
                c = c+1
                time.sleep(5) # Wait for 5 seconds before retrying
            else:
                # Close the Firefox driver instance
                driver.quit()
                return {
                    'images': images,
                    'title': title
                }
        except Exception as e:
            print(e)
            driver.quit()
            continue

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
