"""Custom exception classes."""
from __future__ import annotations

class ResourceFetchError(Exception):
    """Raised when unable to fetch a certain remote resource"""

    def __init__(
        self,
        host: str,
        resource: str | None = None,
        reason: str | None = None
    ) -> None:
        if resource == None:
            resource = 'resource'
        message = f"Error fetching {resource} from {host}"
        if reason != None:
            message += f"; {reason}"
        super().__init__(message)


class ResourceFetchTimeoutError(ResourceFetchError):
    """Raised when unable to fetch a certain remote resource due to a connection timeout"""

    def __init__(
        self,
        host: str,
        resource: str | None = None
    ) -> None:
        super().__init__(host, resource, 'Connection timeout')
