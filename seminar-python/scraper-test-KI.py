import unittest
from scraper import WebScraper
from mock import patch, MagicMock

class TestWebScraper(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_fetch_html_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '<html></html>'
        mock_get.return_value = mock_response

        scraper = WebScraper('https://example.com')
        html = scraper.fetch_html()
        self.assertEqual(html, '<html></html>')

    
    def test_parse_titles(self):
        html = '''
        <html>
            <head><title>Test Page</title></head>
            <body>
                <h1 class="title">Title 1</h1>
                <h1 class="title">Title 2</h1>
            </body>
        </html>
        '''
        scraper = WebScraper('https://example.com')
        titles = scraper.parse_titles(html, 'h1.title')
        self.assertEqual(titles, ['Title 1', 'Title 2'])
        

    @patch('scraper.requests.get')
    def test_fetch_html_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        scraper = WebScraper('localhost')
        with self.assertRaises(Exception):
            scraper.fetch_html()



if __name__ == '__main__':
    unittest.main()