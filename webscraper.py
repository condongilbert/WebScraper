from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Path to ChromeDriver
driver_path = "C:/Users/v-gcondon/Downloads/chromedriver-win64/chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode, optional
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create a Service object
service = Service(driver_path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the URL
    url = "https://www.berkshirehathaway.com/news/2024news.html"
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load content
    
    # Save and print HTML content
    page_source = driver.page_source
    with open("downloaded_page.html", "w", encoding="utf-8") as file:
        file.write(page_source)
    print("Page HTML content saved as 'downloaded_page.html'. Check this file for links.")
    
finally:
    driver.quit()