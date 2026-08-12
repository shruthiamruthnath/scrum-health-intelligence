import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from scrum_health.server import Handler


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()

    def test_health_endpoint(self):
        with urlopen(f"http://127.0.0.1:{self.server.server_port}/api/health") as response:
            self.assertEqual(200, response.status)
            self.assertEqual("ok", json.load(response)["status"])

    def test_dashboard_is_served(self):
        with urlopen(f"http://127.0.0.1:{self.server.server_port}/") as response:
            self.assertIn(b"Scrum Health Intelligence", response.read())


if __name__ == "__main__": unittest.main()

