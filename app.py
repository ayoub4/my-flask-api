from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

chrome_options = Options()
chrome_options.add_argument("--headless")  # run in headless mode so no browser window is opened
chrome_options.add_argument("--no-sandbox")

# Get the path to the ChromeDriver executable based on the operating system
if os.name == 'nt':  # For Windows
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
else:  # For Linux
    chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')

@app.route('/scrape')
def scrape():
    url = request.args.get('url')

    # Create the Chrome driver instance and specify the path to the ChromeDriver executable
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

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

    # Close the Chrome driver instance
    print(title)
    print(images)
    driver.quit()

    return {
        'title': title,
        'images': images
    }


if __name__ == '__main__':
    app.run(debug=True)
