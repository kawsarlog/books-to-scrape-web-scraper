import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Base URL of the website
base_url = 'https://books.toscrape.com/catalogue/page-{}.html'
book_base_url = 'https://books.toscrape.com/catalogue/'

# Create directories if they don't exist
os.makedirs('data_sheet', exist_ok=True)
os.makedirs('images', exist_ok=True)

# List to store book details
books = []

# Function to extract data from a single page
def extract_data_from_page(soup, page):
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        availability = book.find('p', class_='instock availability').text.strip()
        rating_text = book.p['class'][1]
        rating = convert_rating_to_number(rating_text)
        link = book_base_url + book.h3.a['href']
        thumbnail_url = 'https://books.toscrape.com/' + book.find('img', class_='thumbnail')['src']
        thumbnail_file_name = save_thumbnail_image(thumbnail_url, title)
        
        book_data = {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating,
            'Link': link,
            'Thumbnail URL': thumbnail_url,
            'Thumbnail File Name': thumbnail_file_name
        }
        
        books.append(book_data)
        
        # Print the extracted data to the console in a formatted way
        print(f"Page: {page}")
        print(f"Title: {title}")
        print(f"Price: {price}")
        print(f"Availability: {availability}")
        print(f"Rating: {rating}")
        print(f"Link: {link}")
        print(f"Thumbnail URL: {thumbnail_url}")
        print(f"Thumbnail File Name: {thumbnail_file_name}")
        print("="*50)

# Function to convert rating text to a number
def convert_rating_to_number(rating_text):
    rating_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return rating_dict.get(rating_text, 0)

# Function to save thumbnail image
def save_thumbnail_image(url, title):
    response = requests.get(url)
    sanitized_title = "".join([c if c.isalnum() else "_" for c in title])
    image_path = os.path.join('images', f"{sanitized_title}.jpg")
    with open(image_path, 'wb') as file:
        file.write(response.content)
    return image_path

# Loop through the first 10 pages
for page in range(1, 11):  # Scraping the first 10 pages
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    extract_data_from_page(soup, page)
    print(f"Extracted data from page {page}")

# Save the data to a CSV file
df = pd.DataFrame(books)
df.to_csv('data_sheet/books_data.csv', index=False)
print("Data saved to data_sheet/books_data.csv")
