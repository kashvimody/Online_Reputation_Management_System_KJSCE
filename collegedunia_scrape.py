import requests
from bs4 import BeautifulSoup
import csv

# URL of the reviews page
base_url = "https://collegedunia.com/college/13916-k-j-somaiya-college-of-engineering-kjsce-mumbai/reviews"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0'
}

# Function to fetch and parse the reviews page
def fetch_reviews(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve the page: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    review_data = []

    # Locate all review sections 
    review_sections = soup.find_all('section', class_=lambda x: x and 'clg-review' in x)

    for section in review_sections:
        try:
            # Extract the review text directly from the section
            review_text = section.get_text(separator=' ').strip()
        except AttributeError:
            review_text = "No review content found"

        try:
            # Extract the rating using a more specific selector
            rating = section.find('span', class_='jsx-3091098665 f-16 font-weight-semi text-dark-grey').get_text(strip=True)
        except AttributeError:
            rating = "No rating found"

        try:
            # Extract the date, looking for text containing "Reviewed on"
            date_element = section.find('span', class_='jsx-3091098665', string=lambda s: s and 'Reviewed on' in s)
            date = date_element.get_text(strip=True).replace('Reviewed on ', '') if date_element else "No date found"
        except AttributeError:
            date = "No date found"

        # Append each piece of extracted information as a new row
        review_data.append([review_text, rating, date, url])

    return review_data

# Function to save the reviews to a CSV file
def save_reviews_to_csv(reviews, filename='collegedunia_reviews.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Review', 'Rating', 'Date', 'Source URL'])
        writer.writerows(reviews)

    print(f"Reviews saved to {filename}")

# Main function to scrape and save the reviews
if __name__ == "__main__":
    all_reviews = []
    page = 1

    while True:
        url = f"{base_url}?page={page}"
        reviews = fetch_reviews(url)
        
        # Break if no reviews are found on the current page (end of pagination)
        if not reviews:
            break

        # Add the reviews of the current page to the list of all reviews
        all_reviews.extend(reviews)
        
        # Move to the next page
        page += 1

    # Save all collected reviews to a CSV file
    if all_reviews:
        save_reviews_to_csv(all_reviews)
    else:
        print("No reviews found.")
