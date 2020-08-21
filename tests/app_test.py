import os
import unittest
import fakeredis
import app

from bs4 import BeautifulSoup


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()
        app.redis = fakeredis.FakeStrictRedis()
        app.redis.set('hits', 1)

    def test_page_counter(self):
        response = self.app.get('/test', follow_redirects=True)
        data = response.data.decode('utf-8')
        self.assertIn(data, "Flask Web Server is Up!")

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_counter(self):
        app.redis.get('hits')
        current_counter = app.redis.get('hits')
        response = self.app.get('/', follow_redirects=True)
        soup = BeautifulSoup(response.data, "html.parser")
        return_counter = soup.find(id="counter").text
        self.assertEqual(int(current_counter) + 1, int(return_counter))


if __name__ == "__main__":
    unittest.main()