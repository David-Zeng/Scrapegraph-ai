"""
Module for managing SSL certificate configuration for web scraping
"""
import os
import ssl
from pathlib import Path
import certifi  # Add import for certifi
import urllib.request  # Add import for urllib

class SSLConfiguration:
    """
    Handles SSL/TLS configuration for web scrapers
    """
    def __init__(self, ca_bundle_path: str = None):
        """
        Initialize SSL configuration

        Args:
            ca_bundle_path: Path to CA bundle file. Defaults to system certs.
        """
        self.ca_bundle_path = ca_bundle_path or self._get_default_ca_bundle()
        self.ssl_context = self.create_ssl_context()

    def _get_default_ca_bundle(self) -> str:
        """Get default CA bundle path"""
        # Prefer environment variable if set, else use system defaults
        return os.environ.get('SSL_CA_BUNDLE') or ssl.get_default_verify_paths().cafile or certifi.where()

    def create_ssl_context(self) -> ssl.SSLContext:
        """Create SSL context with custom CA bundle"""
        context = ssl.create_default_context()

        if self.ca_bundle_path and Path(self.ca_bundle_path).exists():
            context.load_verify_locations(cafile=self.ca_bundle_path)
        else:
            raise FileNotFoundError(f"CA bundle not found at {self.ca_bundle_path}")

        return context

    def verify_url(self, url: str) -> bool:
        """Verify if SSL certificate is valid for a given URL"""
        try:
            with urllib.request.urlopen(url, context=self.ssl_context) as response:
                return response.status == 200
        except ssl.SSLError:
            return False

# Global SSL configuration instance
ssl_config = SSLConfiguration()