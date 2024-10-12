import requests
from bs4 import BeautifulSoup
import pdfkit

# Function to fetch and clean the website's content
def get_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove external links
    for link in soup.find_all('a', href=True):
        if not link['href'].startswith(url):
            link.decompose()

    # You can also clean other elements like ads, footers, etc.
    
    return str(soup)

# Function to convert HTML to PDF
def convert_html_to_pdf(html_content, output_file):
    # Provide the path to the wkhtmltopdf executable
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
    
    # Convert the HTML content to PDF
    pdfkit.from_string(html_content, output_file, configuration=config)

# Main function
if __name__ == "__main__":
    base_url = "https://help.optmyzr.com/en/"
    
    # Get the website content
    html_content = get_website_content(base_url)
    
    # Save the content as PDF
    output_pdf = "optmyzr_help_site.pdf"
    convert_html_to_pdf(html_content, output_pdf)

    print(f"Website content has been saved to {output_pdf}")
