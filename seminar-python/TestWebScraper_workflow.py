import unittest
from unittest.mock import patch, Mock
from web_scraper import WebScraper  # Replace with the actual file name containing the WebScraper class


class TestWebScraper(unittest.TestCase):

    # -------- Test __init__ method -------- #
    def test_init_with_valid_url(self):
        # Test if the URL is correctly stored during initialization
        scraper = WebScraper("https://example.com")
        self.assertEqual(scraper.url, "https://example.com")

    def test_init_with_empty_url(self):
        # Test initialization with an empty string
        with self.assertRaises(ValueError):  # Assuming you add a ValueError check in your implementation
            WebScraper("")

    def test_init_with_malformed_url(self):
        # Test initialization with a malformed URL
        scraper = WebScraper("http:/example")
        self.assertEqual(scraper.url, "http:/example")  # No validation currently; ensures it's stored as provided

    # -------- Test fetch_html method -------- #
    @patch("web_scraper.requests.get")  # Mocking requests.get
    def test_fetch_html_success(self, mock_get):
        # Mock a successful HTTP GET response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test</body></html>"
        mock_get.return_value = mock_response

        scraper = WebScraper("https://example.com")
        html = scraper.fetch_html()
        self.assertEqual(html, "<html><body>Test</body></html>")  # Verify returned HTML

    @patch("web_scraper.requests.get")
    def test_fetch_html_http_error(self, mock_get):
        # Mock an HTTP error (e.g., 404)
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        scraper = WebScraper("https://example.com")
        with self.assertRaises(Exception):  # Test if the correct exception is raised
            scraper.fetch_html()

    @patch("web_scraper.requests.get")
    def test_fetch_html_non_html_response(self, mock_get):
        # Mock a non-HTML response (e.g., JSON)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '{"key": "value"}'
        mock_get.return_value = mock_response

        scraper = WebScraper("https://example.com")
        html = scraper.fetch_html()
        self.assertEqual(html, '{"key": "value"}')  # Ensure non-HTML content is still returned correctly

    @patch("web_scraper.requests.get")
    def test_fetch_html_timeout(self, mock_get):
        # Mock a timeout error
        mock_get.side_effect = Exception("Timeout error")

        scraper = WebScraper("https://example.com")
        with self.assertRaises(Exception):  # Ensure the timeout exception is raised
            scraper.fetch_html()

    # -------- Test parse_titles method -------- #
    def test_parse_titles_valid_html(self):
        # Test parsing valid HTML for titles
        html = """
        <html>
            <body>
                <h1>Title 1</h1>
                <h1>Title 2</h1>
            </body>
        </html>
        """
        scraper = WebScraper("https://example.com")
        titles = scraper.parse_titles(html, "h1")
        self.assertEqual(titles, ["Title 1", "Title 2"])  # Verify parsed titles

    def test_parse_titles_no_matching_elements(self):
        # Test parsing HTML with no matches for the CSS selector
        html = """
        <html>
            <body>
                <div>No titles here</div>
            </body>
        </html>
        """
        scraper = WebScraper("https://example.com")
        titles = scraper.parse_titles(html, "h1")
        self.assertEqual(titles, [])  # Should return an empty list if no matches

    def test_parse_titles_empty_html(self):
        # Test parsing an empty HTML string
        html = ""
        scraper = WebScraper("https://example.com")
        titles = scraper.parse_titles(html, "h1")
        self.assertEqual(titles, [])  # Should return an empty list for empty HTML

    def test_parse_titles_invalid_html(self):
        # Test parsing malformed HTML
        html = "<html><div>"
        scraper = WebScraper("https://example.com")
        titles = scraper.parse_titles(html, "div")
        self.assertEqual(titles, [])  # BeautifulSoup handles malformed HTML; should return no matches

    def test_parse_titles_with_special_characters(self):
        # Test parsing elements with special characters in text
        html = """
        <html>
            <body>
                <h1>Title &amp; 1</h1>
                <h1>😀 Title 2</h1>
            </body>
        </html>
        """
        scraper = WebScraper("https://example.com")
        titles = scraper.parse_titles(html, "h1")
        self.assertEqual(titles, ["Title & 1", "😀 Title 2"])  # Verify special characters and emoji are preserved

    def test_parse_titles_whitespace_handling(self):
        # Test parsing elements containing extra whitespace
        html = """
        <html>
            <body>
                <h1>   Title 1   </h1>
                <h1>Title 2</h1>
            </body>
        </html>
        """
        scraper = WebScraper("https://example.com")
        titles = scraper.parse_titles(html, "h1")
        self.assertEqual(titles, ["Title 1", "Title 2"])  # Verify leading/trailing whitespace is stripped

    # -------- Test Full Workflow -------- #
    @patch("web_scraper.requests.get")
    def test_full_workflow_success(self, mock_get):
        # Mock a successful GET request and test full workflow
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <h1>Title 1</h1>
                <h1>Title 2</h1>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        scraper = WebScraper("https://example.com")
        html = scraper.fetch_html()  # Fetch the HTML
        titles = scraper.parse_titles(html, "h1")  # Parse titles
        self.assertEqual(titles, ["Title 1", "Title 2"])  # Verify the full workflow outputs correct titles


if __name__ == "__main__":
    unittest.main()