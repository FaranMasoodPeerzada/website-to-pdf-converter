import requests
from bs4 import BeautifulSoup
import pdfkit
from urllib.parse import urljoin, urlparse
import time

# Function to fetch and clean the website's content
def get_website_content(url, base_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove external links
    for link in soup.find_all('a', href=True):
        full_link = urljoin(base_url, link['href'])
        if not full_link.startswith(base_url):
            link.decompose()

    return soup

# Function to find all internal links
def get_internal_links(soup, base_url):
    links = set()
    for link in soup.find_all('a', href=True):
        full_link = urljoin(base_url, link['href'])
        if full_link.startswith(base_url):
            links.add(full_link)
    return links

# Function to convert HTML content to PDF
def convert_html_to_pdf(html_content, output_file):
    # Provide the path to the wkhtmltopdf executable
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    
    # Convert the HTML content to PDF
    pdfkit.from_string(html_content, output_file, configuration=config)

# Main function to scrape all internal links and generate a PDF
def scrape_website_to_pdf(base_url, output_pdf):
    visited_links = set()
    content = ""

    # Start with the base URL
    to_visit = {base_url}

    while to_visit:
        url = to_visit.pop()
        if url not in visited_links:
            print(f"Scraping {url}...")
            soup = get_website_content(url, base_url)
            visited_links.add(url)
            content += str(soup)

            # Get new internal links
            internal_links = get_internal_links(soup, base_url)
            to_visit.update(internal_links - visited_links)

            # Respect web server (add delay to avoid overloading)
            time.sleep(1)

    # Convert all the collected content to PDF
    convert_html_to_pdf(content, output_pdf)
    print(f"Website content and its pages have been saved to {output_pdf}")

# Entry point
if __name__ == "__main__":
    base_url = "https://help.optmyzr.com/en/"
    
    # Define the output PDF file name
    output_pdf = "optmyzr_help_site_all_pages.pdf"
    
    # Scrape website and convert to PDF
    scrape_website_to_pdf(base_url, output_pdf)
