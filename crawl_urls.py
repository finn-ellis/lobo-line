import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils import save_pickle, clean_text
import json

async def fetch(session, url):
    """
    Fetches the content of a URL asynchronously.
    """
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return ""

async def crawl_subdomain(session, base_url):
    """
    Crawls a subdomain and returns a set of all found URLs.
    """
    urls = set()
    to_visit = set([base_url])
    visited = set()

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        visited.add(current_url)
        html = await fetch(session, current_url)
        if not html:
            continue
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc.endswith(urlparse(base_url).netloc):
                cleaned_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
                urls.add(cleaned_url)
                if cleaned_url not in visited:
                    to_visit.add(cleaned_url)
    return urls

async def main():
    # Read subdomains from file
    with open('site_titles_urls.json', 'r') as f:
        subdomains_data = json.load(f)
    subdomains = [entry['url'] for entry in subdomains_data]

    all_urls = set()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for subdomain in subdomains:
            tasks.append(crawl_subdomain(session, subdomain))
        
        results = await asyncio.gather(*tasks)
        for url_set in results:
            all_urls.update(url_set)

    with open('urls.txt', 'w') as f:
        for url in all_urls:
            f.write(f"{url}\n")
    
    print(f"Crawled URLs from {len(subdomains)} subdomains. Total URLs found: {len(all_urls)}.")

if __name__ == "__main__":
    asyncio.run(main()) 