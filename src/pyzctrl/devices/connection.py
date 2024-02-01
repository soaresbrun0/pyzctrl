"""Support for connecting to ZControl® devices."""

import logging
import urllib
from abc import abstractmethod
from typing import Optional, Protocol

import requests
from requests.exceptions import RequestException, Timeout

_LOGGER = logging.getLogger(__name__)


class ZControlDeviceConnection(Protocol):
    """Defines an abstract device connection."""

    @abstractmethod
    def fetch_resource(self, path: str) -> str:
        """Fetches a resource with the given path."""
        raise NotImplementedError
    
    class ConnectionError(Exception):
        """Raised when unable to connect to a device."""

        def __init__(self, url: str, reason: Optional[str] = None) -> None:
            message = f"Failed to connect to {url}"
            if reason is not None:
                message += f"; {message}"
            super().__init__(message)

    class ConnectionTimeoutError(Exception):
        """Raised when an attempt to connect to a device times out."""

        def __init__(self, url: str) -> None:
            super().__init__(url, 'Connection timed out')


class ZControlDeviceHTTPConnection(ZControlDeviceConnection):
    """Defines an HTTP-based device connection."""

    base_url: str
    """The base URL for connecting to the device."""

    timeout: int
    """The timeout in seconds to use when connecting to the device."""

    DEFAULT_TIMEOUT = 10
    """The default timeout in seconds to use when connecting to the device."""

    def __init__(self, base_url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def fetch_resource(self, path: str) -> str:
        try:
            url = urllib.parse.urljoin(self.base_url, path)
            _LOGGER.debug("Fetching %s", url)

            response = requests.get(url, timeout = self.timeout)
            response.raise_for_status()

            _LOGGER.debug("Successfully fetched %s: %s", url, response.text)
            return response.text

        except Timeout as ex:
            _LOGGER.error("Timed out while fetching %s", url)
            raise self.ConnectionTimeoutError(url) from ex

        except RequestException as ex:
            _LOGGER.error("Failed to fetch resource %s; %s", url, ex)
            raise self.ConnectionError(url, str(ex)) from ex
