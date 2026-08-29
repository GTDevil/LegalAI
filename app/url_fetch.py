"""Fetch a public CSV/text list of leads from an https URL (bulk import)."""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse

import httpx

MAX_BYTES = 1_000_000


def normalize_sheet_url(url: str) -> str:
    text = url.strip()
    marker = "/spreadsheets/d/"
    if "docs.google.com" in text and marker in text:
        rest = text.split(marker, 1)[1]
        sheet_id = rest.split("/")[0].split("?")[0]
        gid = "0"
        if "gid=" in text:
            gid = text.split("gid=", 1)[1].split("&")[0].split("#")[0]
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
    return text


def _host_is_public(hostname: str) -> bool:
    if not hostname or hostname.lower() in {"localhost", "127.0.0.1", "::1"}:
        return False
    try:
        infos = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return False
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved:
            return False
    return True


def fetch_public_text(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Only https links are allowed")
    host = parsed.hostname or ""
    if not _host_is_public(host):
        raise ValueError("That link is not allowed")
    with httpx.Client(timeout=20.0, follow_redirects=True) as client:
        response = client.get(url, headers={"User-Agent": "LegalAI-calling-desk/1.0"})
        response.raise_for_status()
        content = response.content[: MAX_BYTES + 1]
    if len(content) > MAX_BYTES:
        raise ValueError("The file is too large (max 1 MB)")
    return content.decode("utf-8-sig", errors="replace")
