from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

# Set up the Selenium driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
url = "https://www.shiksha.com/college/k-j-somaiya-college-of-engineering-vidya-vihar-mumbai-37903/reviews"

# Fetch the page
driver.get(url)
time.sleep(5)  # Wait for the page to load

soup = BeautifulSoup(driver.page_source, 'html.parser')
review_data = []

# Locate all review sections
review_sections = soup.find_all('section', class_='review-card')

for section in review_sections:
    try:
        review_text = section.find('div', class_='rvw-content').get_text(separator=' ', strip=True)
        rating = section.find('span', class_='rating-block rvw-lyr').get_text(strip=True).split()[0]
        date = section.find('div', class_='rvw-date').get_text(strip=True).replace('Reviewed on ', '')
        review_data.append([review_text, rating, date, url])
    except AttributeError:
        continue  # Skip sections with missing data

driver.quit()  # Close the driver

# Save reviews to CSV
if review_data:
    with open('shiksha_reviews.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Review', 'Rating', 'Date', 'Source URL'])
        writer.writerows(review_data)
    print(f"Reviews saved to shiksha_reviews.csv")
else:
    print("No reviews found.")
