import os
import time
import asyncio
from dotenv import load_dotenv
from urllib.parse import urlparse
from firecrawl import FirecrawlApp
import gradio as gr

load_dotenv()

def get_firecrawl_app(api_key):
    return FirecrawlApp(api_key=api_key)

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

async def scrape_all_urls(base_url, api_key, limit_rate, progress=gr.Progress(), cancel_event=None):
    app = get_firecrawl_app(api_key)
    urls = map_website(app, base_url)
    if not urls:
        return "No URLs found. Please check if the base URL is correct.", None

    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc.replace("www.", "")
    os.makedirs('scraped_documentation', exist_ok=True)
    output_file = os.path.join('scraped_documentation', f"{domain}.md")

    with open(output_file, 'w', encoding='utf-8') as md_file:
        for i, url in enumerate(progress.tqdm(urls)):
            if cancel_event and cancel_event.is_set():
                return "Scraping cancelled.", None
            progress(i / len(urls), f"Scraping {url}")
            markdown_content = await async_scrape_url(app, url)
            md_file.write(f"# {url}\n\n")
            md_file.write(markdown_content)
            md_file.write("\n\n---\n\n")
            if limit_rate and (i + 1) % 10 == 0:
                time.sleep(60)

    return f"Scraping completed. Output saved to {output_file}", output_file

def count_urls(base_url, api_key):
    if not api_key:
        return "Please enter your Firecrawl API key first."
    app = get_firecrawl_app(api_key)
    urls = map_website(app, base_url)
    if urls:
        return f"{len(urls)} URLs found. Do you want to proceed with scraping?"
    else:
        return "No URLs found. Please check the base URL or API key."

async def gradio_scrape(base_url, api_key, limit_rate, progress=gr.Progress()):
    if not api_key:
        return "Please enter your Firecrawl API key.", None
    if not base_url:
        return "Please enter a base URL to scrape.", None
    cancel_event = asyncio.Event()
    result, file_path = await scrape_all_urls(base_url, api_key, limit_rate, progress, cancel_event)
    return result, file_path

def cancel_scrape():
    # This function will be called when the cancel button is clicked
    global cancel_event
    if cancel_event:
        cancel_event.set()
    return "Cancelling scrape operation..."

with gr.Blocks() as iface:
    gr.Markdown("# Docs Scraper")
    gr.Markdown("""
    ## Map and Scrape Website URLs with Firecrawl API
    Enter a base URL, your Firecrawl API key, and choose whether to limit the scraping rate.
    Scraped content will be saved as a markdown file named after the domain.
    """)
    gr.HTML('Don\'t have an API key? <a href="https://firecrawl.dev/" target="_blank" rel="noopener noreferrer">Get one from Firecrawl</a>')
    
    with gr.Row():
        base_url = gr.Textbox(label="Base URL", placeholder="Enter the base URL to scrape")
        api_key = gr.Textbox(label="Firecrawl API Key", type="password")
        limit_rate = gr.Checkbox(
            label="Limit Rate", 
            value=True, 
            info="Enable to limit scraping to 10 URLs per minute. This adheres to Firecrawl API's free tier rate limit."
        )
    
    gr.Markdown("After entering your API key, click 'Count URLs' to determine the number of URLs to be scraped. Then, click 'Scrape URLs' to begin the process.")
    
    with gr.Row():
        with gr.Column(scale=1):
            count_button = gr.Button("Count URLs")
        with gr.Column(scale=1):
            url_count = gr.Textbox(label="URL Count")

    with gr.Row():
        with gr.Column(scale=1):
            scrape_button = gr.Button("Scrape URLs")
            cancel_button = gr.Button("Cancel Scrape")
        with gr.Column(scale=1):
            output = gr.Textbox(label="Output", elem_id="output_textbox")
    
    file_output = gr.File(label="Download Scraped Content")
    
    gr.Markdown("""
    #### Note: 
    The free tier of the Firecrawl API allows for 500 credits per month. 
    If you need to scrape more, consider upgrading to a paid plan.
    """)
    
    count_button.click(count_urls, inputs=[base_url, api_key], outputs=[url_count])
    scrape_button.click(gradio_scrape, inputs=[base_url, api_key, limit_rate], outputs=[output, file_output])
    cancel_button.click(cancel_scrape, outputs=[output])

if __name__ == "__main__":
    global cancel_event
    cancel_event = asyncio.Event()
    iface.launch()