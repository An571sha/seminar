import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url

    def fetch_html(self):
        """Fetches HTML content of the webpage."""
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.text
        else:
            response.raise_for_status()

    def parse_titles(self, html, css_selector):
        """Parses the HTML to extract titles based on the provided CSS selector."""
        soup = BeautifulSoup(html, 'html.parser')
        titles = [element.get_text().strip() for element in soup.select(css_selector)]
        return titles
     