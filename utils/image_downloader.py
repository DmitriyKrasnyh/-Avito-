"""Simple helper for downloading images."""

from pathlib import Path
from typing import Optional

import requests


def download_image(url: str, dest: Path, *, timeout: int = 10) -> Optional[Path]:
    """Download an image from ``url`` and save it to ``dest``.

    Returns the destination path on success or ``None`` on error.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        return None

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(response.content)
    return dest
