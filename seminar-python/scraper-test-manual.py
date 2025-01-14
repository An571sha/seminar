import unittest
from mock import patch, MagicMock

class TestWebScraper(unittest.TestCase):
    def setUp(self):
        """Set up a WebScraper instance and mock data."""
        from scraper import WebScraper
        self.url = "https://example.com"
        self.scraper = WebScraper(self.url)
        self.mock_html = """
        <html>
            <body>
                <h1>Test Title</h1>
                <div class="article-title">Article 1</div>
                <div class="article-title">Article 2</div>
                <div class="article-title">Article 3</div>
            </body>
        </html>
        """

    @patch('requests.get')
    def test_fetch_html(self, mock_get):
        """Test the fetch_html method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.mock_html
        mock_get.return_value = mock_response

        html = self.scraper.fetch_html()
        self.assertEqual(html, self.mock_html)
        mock_get.assert_called_once_with(self.url)

    def test_parse_titles(self):
        """Test the parse_titles method."""
        titles = self.scraper.parse_titles(self.mock_html, ".article-title")
        self.assertEqual(titles, ["Article 1", "Article 2", "Article 3"])

if __name__ == '__main__':
    unittest.main()
