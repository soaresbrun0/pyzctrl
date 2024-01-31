"""Utilities to support testing."""

import os
from pathlib import Path
from src.pyzctrl.devices.connection import ZControlDeviceConnection


DEFAULT_BASE_DIR = Path(os.path.dirname(__file__))


def read_file(
        path: Path, 
        base_dir = DEFAULT_BASE_DIR,
        encoding: str = "UTF-8",
    ) -> str:
    """Reads the content of the given file."""
    path = (base_dir / path).resolve(strict = False)
    with open(path, 'r', encoding = encoding) as f:
        return f.read()


class MockDeviceConnection(ZControlDeviceConnection):
    """Defines a mock device connection backed by a static map of resources."""

    def __init__(self, resources: dict[str, str]) -> None:
        self.resources = resources

    def fetch_resource(self, path: str) -> str:
        try:
            return self.resources[path]
        except Exception as ex:
            raise self.ConnectionError(path) from ex