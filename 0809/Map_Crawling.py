from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import quote
import csv

# Initialize a Selenium WebDriver

# 실행하고 원하는 검색어 입력(띄어쓰기 없이) ex)"부산대맛집"  

input_text = input()
url_text = quote(input_text)
url = "https://map.naver.com/v5/search/"+ url_text+"?c=10,0,0,0,dh"
driver = webdriver.Chrome()  # You need to have ChromeDriver installed and its path set

# Number of times to run the code
num_runs = 3

for _ in range(num_runs):
    # Load the webpage using Selenium
    driver.get(url)

    # Switch to the iframe context
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)

    # Wait for the iframe content to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'place_bluelink')))

    # Get the page source after giving some time for JavaScript content to load
    page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")

    # Find all elements with the specified class
    restaurant_elements = soup.find_all("span", class_="place_bluelink TYaxT")

    # Extract the names of the first 10 restaurants
    restaurant_names = [restaurant.get_text() for restaurant in restaurant_elements[:10]]

    # Close the iframe context
    driver.switch_to.default_content()

    # Save the restaurant names in a CSV file with a dynamic filename
    csv_filename = f"restaurant_names.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([input_text])  # Write header
        writer.writerows([[name] for name in restaurant_names])  # Write restaurant names

    print(f"First 10 restaurant names saved in '{csv_filename}'")
    # Increment the file counter

# Close the Selenium WebDriver
driver.quit()

