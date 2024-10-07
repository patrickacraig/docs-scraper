import os
import time
from dotenv import load_dotenv
from urllib.parse import urlparse
from firecrawl import FirecrawlApp
import gradio as gr

load_dotenv()

def map_website(url, api_key):
    app = FirecrawlApp(api_key=api_key)
    map_status = app.map_url(url)
    if isinstance(map_status, list):
        return map_status
    else:
        print("Failed to map the website:", map_status)
        return []

def scrape_url(url, api_key):
    app = FirecrawlApp(api_key=api_key)
    scrape_status = app.scrape_url(url)
    print(f"Scrape status for {url}: {scrape_status}")
    if 'markdown' in scrape_status:
        return scrape_status['markdown']
    else:
        print(f"Failed to scrape {url}: {scrape_status}")
        return ""

def scrape_all_urls(base_url, api_key, limit_rate, progress=gr.Progress()):
    urls = map_website(base_url, api_key)
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc.replace("www.", "")
    os.makedirs('scraped_documentation', exist_ok=True)
    output_file = os.path.join('scraped_documentation', f"{domain}.md")
    
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for i, url in enumerate(progress.tqdm(urls)):
            progress(i / len(urls), f"Scraping {url}")
            markdown_content = scrape_url(url, api_key)
            md_file.write(f"# {url}\n\n")
            md_file.write(markdown_content)
            md_file.write("\n\n---\n\n")
            if limit_rate:
                if (i + 1) % 10 == 0:
                    time.sleep(60)
    
    return f"Scraping completed. Output saved to {output_file}"

def count_urls(base_url, api_key):
    if not api_key:
        return "Please enter your Firecrawl API key first."
    urls = map_website(base_url, api_key)
    return f"{len(urls)} URLs found. Do you want to proceed with scraping?"

def gradio_scrape(base_url, api_key, limit_rate):
    if not api_key:
        return "Please enter your Firecrawl API key."
    if not base_url:
        return "Please enter a base URL to scrape."
    return scrape_all_urls(base_url, api_key, limit_rate)

with gr.Blocks() as iface:
    gr.Markdown("# Docs Scraper")
    gr.Markdown("## To map and scrape all URLs from a given website using the Firecrawl API, enter a base URL to scrape, your Firecrawl API key, and choose whether to limit the rate of scraping.")
    gr.Markdown("Scraped content is saved into a markdown file named after the domain of the base URL, making it easy to reference and utilize. This can be particularly useful for AI code editors that need to gather context from various types of websites. By scraping the content, the AI can analyze and understand the structure and information provided, which can enhance its ability to offer accurate code suggestions and improvements.")
    gr.HTML('Don\'t have an API key? <a href="https://firecrawl.dev/" target="_blank" rel="noopener noreferrer">Get one from Firecrawl</a>')
    
    with gr.Row():
        base_url = gr.Textbox(label="Base URL", placeholder="Enter the base URL to scrape")
        api_key = gr.Textbox(label="Firecrawl API Key", type="password")
        limit_rate = gr.Checkbox(
            label="Limit Rate", 
            value=True, 
            info="Enable to limit scraping to 10 URLs per minute. This adheres to Firecrawl API's free tier rate limit."
        )
    
    gr.Markdown("After entering your API key, click 'Count URLs' to determine the number of URLs to be scraped. Then, click 'Scrape URLs' to begin the process. The progress and file location will be displayed in the textbox labeled 'Output'.") 
    with gr.Row():
        count_button = gr.Button("Count URLs")
        url_count = gr.Textbox(label="URL Count")

    with gr.Row():
        scrape_button = gr.Button("Scrape URLs")
        output = gr.Textbox(label="Output", elem_id="output_textbox")
    
    gr.Markdown("#### Note: The free tier of the Firecrawl API allows for 500 credits per month. If you need to scrape more, you can upgrade to a paid plan. The 'Count URLs' button may not work as expected if the base URL is not correctly specified or if the API key is invalid. Always ensure the base URL is correct and the API key is valid before proceeding.")

    
    count_button.click(count_urls, inputs=[base_url, api_key], outputs=[url_count])
    scrape_button.click(gradio_scrape, inputs=[base_url, api_key, limit_rate], outputs=[output])

if __name__ == "__main__":
    iface.launch()