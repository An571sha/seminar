import unittest

class TestWebScraperBad(unittest.TestCase):
    def test_fetch_and_parse(self):
        """Bad test that fetches live data and parses it."""
        from scraper import WebScraper 
        
        scraper = WebScraper("https://www.google.com")
        html = scraper.fetch_html()
        titles = scraper.parse_titles(html, "h1")
        
        
        self.assertIn("Example Domain", titles)
