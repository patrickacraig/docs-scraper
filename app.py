from firecrawl import FirecrawlApp
import os
import time
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()

base_url = os.getenv('BASE_URL')

def map_website(url):
    # Initialize the Firecrawl application with the API key
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

    # Use the /map endpoint to get all URLs from the website
    map_status = app.map_url(url)

    # Check if the mapping was successful
    if isinstance(map_status, list):
        return map_status
    else:
        print("Failed to map the website:", map_status)
        return []

def scrape_url(url):
    # Initialize the Firecrawl application with the API key
    app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

    # Use the /scrape endpoint to scrape the URL
    scrape_status = app.scrape_url(url)

    # Print the scrape_status to understand its structure
    print(f"Scrape status for {url}: {scrape_status}")

    # Check if the scraping was successful
    if 'markdown' in scrape_status:
        return scrape_status['markdown']
    else:
        print(f"Failed to scrape {url}: {scrape_status}")
        return ""

def scrape_all_urls(base_url):
    # Map the URLs
    urls = map_website(base_url)

    # Parse the base URL to get the domain without 'www' and scheme
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc.replace("www.", "")

    # Create the directory if it doesn't exist
    os.makedirs('scraped_documentation', exist_ok=True)
    
    # Generate the output file name and save location
    output_file = os.path.join('scraped_documentation', f"{domain}.md")

    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as md_file:
        # Iterate over the URLs
        for i, url in enumerate(urls):
            # Print the URL being scraped
            print(f"Scraping {url} ({i+1}/{len(urls)})")

            # Scrape the URL
            markdown_content = scrape_url(url)

            # Write the scraped content to the file
            md_file.write(f"# {url}\n\n")
            md_file.write(markdown_content)
            md_file.write("\n\n---\n\n")

            # Rate limiting: 10 scrapes per minute
            if os.getenv('LIMIT_RATE') == 'True':
                if (i + 1) % 10 == 0:
                    print("Rate limit reached, waiting for 60 seconds...")
                    time.sleep(60)

if __name__ == "__main__":
    
    scrape_all_urls(base_url)