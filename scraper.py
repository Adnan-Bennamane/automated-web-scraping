import csv
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def scrape_books():
    base_url = "http://books.toscrape.com/"
    # Start at the first catalog page
    current_page_url = urljoin(base_url, "catalogue/page-1.html")
    
    # Open a CSV file to save the scraped data
    with open("books.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write CSV Header
        writer.writerow(["Title", "Price", "Rating", "Availability", "Link"])
        
        page_number = 1
        while current_page_url:
            print(f"Scraping page {page_number}...")
            response = requests.get(current_page_url)
            
            if response.status_code != 200:
                print(f"Failed to retrieve page {page_number}. Status code: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article", class_="product_pod")
            
            for book in books:
                # 1. Title (getting the 'title' attribute ensures the full name is retrieved)
                title_el = book.find("h3").find("a")
                title = title_el.get("title") or title_el.text
                
                # 2. Price
                price = book.find("p", class_="price_color").text.strip()
                
                # 3. Rating (extracted from the 'class' attribute of the star-rating paragraph)
                rating_classes = book.find("p", class_="star-rating")["class"]
                rating = next((cls for cls in rating_classes if cls != "star-rating"), "No Rating")
                
                # 4. Availability
                availability = book.find("p", class_="instock availability").text.strip()
                
                # 5. Direct Link
                book_rel_link = title_el.get("href")
                book_link = urljoin(current_page_url, book_rel_link)
                
                # Write the row data to our CSV
                writer.writerow([title, price, rating, availability, book_link])
            
            # Find the link to the next page
            next_button = soup.find("li", class_="next")
            if next_button:
                next_rel_url = next_button.find("a").get("href")
                current_page_url = urljoin(current_page_url, next_rel_url)
                page_number += 1
            else:
                current_page_url = None  # No more pages to scrape

    print("Scraping completed successfully! Data saved to 'books.csv'.")

if __name__ == "__main__":
    scrape_books()
