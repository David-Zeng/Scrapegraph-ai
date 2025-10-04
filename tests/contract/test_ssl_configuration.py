"""
Test SSL certificate verification with trusted public certificates
"""
import unittest
import requests
from scrapegraphai.models.ssl_configuration import SSLConfiguration

class TestSSLConfiguration(unittest.TestCase):
    """Test SSL configuration"""

    def test_ssl_cert_verification(self):
        """Test that SSL certificate verification works with public certificates"""
        # Create SSL config with system default certificates
        ssl_config = SSLConfiguration()

        # Test a public HTTPS endpoint
        url = "https://www.duckduckgo.com"
        try:
            response = requests.get(url,
                                 timeout=10,
                                 verify=ssl_config.ca_bundle_path)
            response.raise_for_status()
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.SSLError as e:
            self.fail(f"SSL certificate verification failed: {str(e)}")