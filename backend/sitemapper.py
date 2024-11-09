import json
import requests
from bs4 import BeautifulSoup, SoupStrainer
import os
from backend.removebadsublinks import filter_sublinks
from config import OPENAI_API_KEY
from tqdm import tqdm
from urllib.parse import urljoin

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def scrape_page(link):
    """Scrape the content of a given webpage and return the text of the page as a string.

    Args:
        link (str): The URL of the webpage to scrape.

    Returns:
        str: The content of the webpage as a string, or None if the request fails.

    Raises:
        Exception: If the request fails or there is another error.
    """
    try:
        response = requests.get(link, timeout=5)
        response.raise_for_status()
        # soup = BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer(
        #     lambda tag, attrs: (
        #         tag in ["p", "h1", "h2", "h3", "li", "span", "a"]
        #     )
        # ))
        soup = BeautifulSoup(response.text, 'html.parser')
        # Remove any navigation divs that may have been parsed
        for nav in soup.find_all(["div", "a"], {"role": "navigation"}):
            nav.decompose()
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"Failed to retrieve {link}: {e}")
        return None

def scrape_pages(sitemap):
    """
    Scrape the content of a list of links and sublinks and save the results to a file.

    Args:
        sitemap (list): A list of dictionaries with 'text', 'url', and 'sublinks' keys.
        scrape_pages (bool, optional): Whether to scrape the pages. Defaults to False.

    Returns:
        None
    """

    # TODO: make sure there are no duplicate sublinks... do this here or in filter_sublinks?
    links = []
    for site in sitemap:
        base_url = site['url']
        links.append(base_url)
        for sublink in site['sublinks']:
            # Use urljoin to properly resolve relative URLs including ../
            full_url = urljoin(base_url + '/', sublink)
            links.append(full_url)
    pages = []
    for link in tqdm(links, desc="Scraping links"):
        page_content = scrape_page(link)
        if page_content:
            pages.append(page_content)
    # Save zip of links and pages to a json file
    links_pages = [{"link": link, "page": page} for link, page in zip(links, pages)]
    with open('links_pages.json', 'w') as f:
        json.dump(links_pages, f, indent=4)
    

def load_sitemap():
    """
    Load the sitemap from a JSON file and return it as a list of dictionaries.

    Returns:
        list: A list of dictionaries containing the sitemap data with 'text', 'url', and 'sublinks' keys.
    """
    with open('site_titles_urls.json', 'r') as f:
        sitemap = json.load(f)
    return sitemap

def write_sitemap():
    """
    Fetch and parse department information from the UNM directory webpage and save 
    the sitemap to a JSON file.

    This function sends a request to the UNM directory page, parses the HTML to find 
    department links, and extracts the main URL and sublinks for each department. 
    It filters and validates URLs before writing the sitemap data to 'site_titles_urls.json'.

    Returns:
        list: A list of dictionaries containing the department names, URLs, and sublinks.

    Raises:
        requests.RequestException: If there's an error during the HTTP request.
    """
    directory_url = "https://directory.unm.edu/departments/"

    try:
        response = requests.get(directory_url, timeout=5)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        department_list_div = soup.find('div', id='department_list')
        if not department_list_div:
            print("No department list found.")
            return
        
        items = department_list_div.find_all('li')
        sitemap = []  # Initialize the list to store titles and URLs
        total_items = len(items)

        for item in tqdm(items, desc="Finding links"):
            text = item.text.strip()
            phone_span = item.find('span', class_='department_table_phone')
            if not phone_span:
                total_items -= 1
                continue
            
            phone_href = phone_span.find('a', href=True)
            if not phone_href:
                total_items -= 1
                continue
            
            phone_href = phone_href['href']
            if not phone_href.strip().startswith("https://"):
                phone_href = "https://" + phone_href.lstrip("http://")
            
            # Check if the URL is valid and works
            try:
                response = requests.get(phone_href, timeout=5)
                if response.status_code == 200:
                    # find sublinks on the page
                    strainer = SoupStrainer('a', href=True)
                    soup = BeautifulSoup(response.content, 'lxml', parse_only=strainer)

                    # Extract and process links
                    sublinks = []
                    for link in soup.find_all('a', href=True):
                        href = link['href'].strip()
                        sublinks.append(href)
                    sublinks = filter_sublinks(sublinks)
                    siteInfo = {'text': text, 'url': phone_href, 'sublinks': sublinks}
                    sitemap.append(siteInfo)  # Add the title and URL to the list
            except requests.RequestException:
                print(f"Invalid or unreachable URL: {phone_href}")

        with open('site_titles_urls.json', 'w') as f:
            json.dump(sitemap, f, indent=4)
            
        print("Titles, URLs, and embeddings saved to site_titles_urls.json")
        return sitemap
    except requests.RequestException as e:
        print(f"Error fetching {directory_url}: {e}")



if __name__ == "__main__":
    # Use to generate sitemap
    # sitemap = write_sitemap()

    # Once sitemap is generated, it can be loaded:
    sitemap = load_sitemap()

    # Use to scrape pages
    scrape_pages(sitemap)

    # Testing scraping:
    # test_link = "https://food.unm.edu/locations/hours/fall-2024-hours.html"
    # print(scrape_page(test_link))