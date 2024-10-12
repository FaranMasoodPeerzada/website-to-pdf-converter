import requests
from bs4 import BeautifulSoup
import pdfkit
from urllib.parse import urljoin
import time
import os
from PyPDF2 import PdfMerger

# Function to fetch and clean the website's content
def get_website_content(url, base_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove external links
    for link in soup.find_all('a', href=True):
        full_link = urljoin(base_url, link['href'])
        if not full_link.startswith(base_url):
            link.decompose()

    return str(soup)

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

# Main function to scrape only the first 5 internal links and generate individual PDFs
def scrape_website_to_pdf(base_url):
    visited_links = set()
    pages_scraped = 0
    max_pages = 5  # Limit to scraping only 5 pages

    # Start with the base URL
    to_visit = {base_url}

    # Create a directory to store individual PDFs
    os.makedirs('individual_pdfs', exist_ok=True)

    while to_visit and pages_scraped < max_pages:
        url = to_visit.pop()
        if url not in visited_links:
            print(f"Scraping {url}...")
            html_content = get_website_content(url, base_url)
            visited_links.add(url)

            # Generate PDF for the current page
            pdf_filename = f'individual_pdfs/page_{pages_scraped + 1}.pdf'
            convert_html_to_pdf(html_content, pdf_filename)

            pages_scraped += 1

            # Get new internal links
            internal_links = get_internal_links(BeautifulSoup(html_content, "html.parser"), base_url)
            to_visit.update(internal_links - visited_links)

            # Respect web server (add delay to avoid overloading)
            time.sleep(1)

    return visited_links

# Function to merge individual PDFs into a single PDF
def merge_pdfs(pdf_list, output_file):
    merger = PdfMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(output_file)
    merger.close()

# Entry point
if __name__ == "__main__":
    base_url = "https://help.optmyzr.com/en/"
    
    # Scrape website and save individual PDFs
    visited_links = scrape_website_to_pdf(base_url)

    # List of PDF files to merge
    pdf_files = [f'individual_pdfs/page_{i + 1}.pdf' for i in range(len(visited_links))]

    # Define the output merged PDF file name
    output_pdf = "optmyzr_help_site_combined.pdf"
    
    # Merge individual PDFs into one
    merge_pdfs(pdf_files, output_pdf)

    print(f"All pages have been saved and combined into {output_pdf}")
