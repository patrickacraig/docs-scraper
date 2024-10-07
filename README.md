<p align="center">
  <img src="images/docs-scraper.webp" alt="Docs Scraper" style="max-width: 300px;">
</p>

# Docs Scraper

This project offers a Python script designed to map and scrape all URLs from a specified website using the Firecrawl API. The scraped content is saved into markdown files, which can then be provided to AI systems to offer context. This is particularly beneficial for AI code editors that need to gather comprehensive information from various websites. By analyzing the scraped content, the AI can better understand the structure and details of the information, thereby enhancing its ability to provide accurate code suggestions and improvements.

Types of sites that would be useful to scrape include:
- Documentation websites
- API reference sites
- Technical blogs
- Tutorials and guides
- Knowledge bases

The scraped content is saved into a markdown file named after the domain of the base URL, making it easy to reference and utilize.

## Prerequisites

- Python 3.x
- <a href="https://firecrawl.dev/" target="_blank" rel="noopener noreferrer">Firecrawl API key</a>
- Virtual environment (recommended)

## Setup

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/patrickacraig/docs-scraper.git
   cd docs-scraper
   ```

2. **Create a Virtual Environment**

   Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Rename the `.env.example` file to `.env` and enter your own variables:

   ```plaintext
   FIRECRAWL_API_KEY=your_actual_api_key  # Your unique API key for accessing the Firecrawl API. Obtain it from your Firecrawl account settings.

   BASE_URL="https://docs.example.com/"  # The starting point URL of the website you want to scrape. Replace with your target URL.

   LIMIT_RATE=True  # Set to "True" to enable rate limiting (10 scrapes per minute), or "False" to disable it.
   ```

## Rate Limiting
The script is designed to adhere to a rate limit of 10 scrapes per minute in adherence with the Firecrawl API free tier. To disable it, set the `LIMIT_RATE` environment variable to `False` in your `.env` file.

## Usage

1. **Run the Script**

   Execute the script to start mapping and scraping the URLs:

   ```bash
   python app.py
   ```

2. **Output**

   The script will generate a markdown file named after the domain of the base URL (e.g., `example.com.md`) containing the scraped content.

## Alternative Usage: Web UI



1.   **Run the Script**

      Alternatively, you can execute the script to run the web-based interface using Gradio:

      ```bash
      python web_ui.py
      ```

      This will launch a web interface in your default browser where you can enter the base URL, your Firecrawl API key, and choose whether to enable rate limiting. The output will be displayed directly in the browser.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## Contact

For any questions or issues, please open an issue in the repository.

