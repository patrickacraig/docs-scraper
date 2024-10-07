from firecrawl import FirecrawlApp
import os
import time
import asyncio
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

base_url = os.getenv('BASE_URL')
api_key = os.getenv('FIRECRAWL_API_KEY')
limit_rate = os.getenv('LIMIT_RATE', 'False').lower() == 'true'

# Get Firecrawl App instance
def get_firecrawl_app(api_key):
    return FirecrawlApp(api_key=api_key)

# Asynchronous scrape URL
async def async_scrape_url(app, url):
    try:
        scrape_status = app.scrape_url(url)
        print(f"Scrape status for {url}: {scrape_status}")
        if 'markdown' in scrape_status:
            return scrape_status['markdown']
        else:
            print(f"Failed to scrape {url}: {scrape_status}")
            return ""
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

# Synchronously map website URLs
def map_website(app, url):
    try:
        map_status = app.map_url(url)
        if isinstance(map_status, list):
            return map_status
        else:
            print("Failed to map the website:", map_status)
            return []
    except Exception as e:
        print(f"Error mapping website {url}: {e}")
        return []

# Asynchronously scrape all URLs
def scrape_all_urls(base_url, api_key, limit_rate):
    async def scrape_process():
        app = get_firecrawl_app(api_key)
        urls = map_website(app, base_url)
        if not urls:
            print("No URLs found. Please check if the base URL is correct.")
            return

        parsed_url = urlparse(base_url)
        domain = parsed_url.netloc.replace("www.", "")
        os.makedirs('scraped_documentation', exist_ok=True)
        output_file = os.path.join('scraped_documentation', f"{domain}.md")

        with open(output_file, 'w', encoding='utf-8') as md_file:
            for i, url in enumerate(urls):
                print(f"Scraping {url} ({i+1}/{len(urls)})")
                markdown_content = await async_scrape_url(app, url)
                md_file.write(f"# {url}\n\n")
                md_file.write(markdown_content)
                md_file.write("\n\n---\n\n")
                
                # Rate limiting: 10 scrapes per minute
                if limit_rate and (i + 1) % 10 == 0:
                    print("Rate limit reached, waiting for 60 seconds...")
                    time.sleep(60)

        print(f"Scraping completed. Output saved to {output_file}")

    asyncio.run(scrape_process())

if __name__ == "__main__":
    if not base_url:
        print("Error: BASE_URL not specified in environment variables.")
    elif not api_key:
        print("Error: FIRECRAWL_API_KEY not specified in environment variables.")
    else:
        scrape_all_urls(base_url, api_key, limit_rate)