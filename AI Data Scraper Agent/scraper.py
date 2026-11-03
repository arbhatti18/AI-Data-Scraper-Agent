
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def scrape_website(url):

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ["http", "https"] or not parsed_url.netloc:
        raise ValueError("Please enter a valid website URL.")

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DataScraper/1.0)"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()

    title = soup.title.get_text(strip=True) if soup.title else "No Title"

    headings = [
        heading.get_text(strip=True)
        for heading in soup.find_all(["h1", "h2", "h3"])
    ]

    paragraphs = [
        paragraph.get_text(strip=True)
        for paragraph in soup.find_all("p")
        if paragraph.get_text(strip=True)
    ]

    links = [
        link.get("href")
        for link in soup.find_all("a", href=True)
    ]

    return {
        "url": url,
        "title": title,
        "headings": headings,
        "paragraphs": paragraphs,
        "links": links
    }
