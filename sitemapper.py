import json
import requests
from bs4 import BeautifulSoup, SoupStrainer
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from scripts.removebadsublinks import filter_sublinks
from config import OPENAI_API_KEY
from tqdm import tqdm

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def generate_embedding_manifest(sitemap, scrape_pages=False):
    api_key = os.getenv("OPENAI_API_KEY")
    embeddings_model = OpenAIEmbeddings(api_key=api_key)

    # Generate embeddings for titles
    # titles = [entry['text'] for entry in sitemap]
    # embeddings = embeddings_model.embed_documents(titles)

    # TODO: add compatbility for ../ links
    # TODO: Revise scraping and make sure it's relevant content (food.unm, events, etc.)
	# TODO: make sure there are no duplicate sublinks
    # TODO: remove duplicate content / boilerplate from pages (unm headers)
    if os.path.exists('links_pages.json') and not scrape_pages:
        with open('links_pages.json', 'r') as f:
            links_pages = json.load(f)
        links = [entry['link'] for entry in links_pages]
        pages = [entry['page'] for entry in links_pages]
    else:
        links = []
        for site in sitemap:
            links.append(site['url'])
            for sublink in site['sublinks']:
                links.append(f"{site['url']}/{sublink}")
        pages = []
        for link in tqdm(links, desc="Scraping links"):
            try:
                response = requests.get(link, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser', parse_only=SoupStrainer(
                    lambda tag, attrs: (
                        tag in ["p", "h1", "h2", "h3", "li", "span", "a"]
                    )
                ))
                page_content = soup.get_text(separator=' ', strip=True)
                pages.append(page_content)
            except Exception as e:
                print(f"Failed to retrieve {link}: {e}")
        # Save zip of links and pages to a json file
        links_pages = [{"link": link, "page": page} for link, page in zip(links, pages)]
        with open('links_pages.json', 'w') as f:
            json.dump(links_pages, f, indent=4)
    
    # vectors = embeddings_model.embed_documents(pages)

    # Write embeddings file
    # embedding_manifest = []
    # for link, vector in zip(links, vectors):
    #     embedding_manifest.append({
    #         "link": link,
    #         "vector": vector
    #     })
    
    # with open('embedding_manifest.json', 'w') as f:
    #     json.dump(embedding_manifest, f, indent=4)
    

def load_sitemap():
    with open('site_titles_urls.json', 'r') as f:
        sitemap = json.load(f)
    return sitemap

def write_sitemap():
    directory_url = "https://directory.unm.edu/departments/"
    load_dotenv()

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
    # sitemap = write_sitemap()
    sitemap = load_sitemap()
    generate_embedding_manifest(sitemap, True)
