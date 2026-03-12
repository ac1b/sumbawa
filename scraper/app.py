"""
Scrapling HTTP API — sidecar for sumbawa-agent.
Endpoints:
  POST /fetch   — fetch URL with optional JS rendering
  POST /search  — fetch Meta Ad Library API
  GET  /health  — liveness check
"""

import os
import json
import asyncio
import ipaddress
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse

# Lazy imports — heavy libs loaded on first use
_fetcher = None
_stealthy = None


def get_fetcher():
    global _fetcher
    if _fetcher is None:
        from scrapling.fetchers import Fetcher
        _fetcher = Fetcher
    return _fetcher


def get_stealthy():
    global _stealthy
    if _stealthy is None:
        from scrapling.fetchers import StealthyFetcher
        _stealthy = StealthyFetcher
    return _stealthy


BLOCKED_NETS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),   # link-local / cloud metadata
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]
# Allow scraper→scraper (localhost) is fine, but block external requests to private nets
ALLOWED_INTERNAL = {"scraper", "localhost", "127.0.0.1"}


def is_url_safe(url: str) -> bool:
    """Block SSRF: no private IPs, no cloud metadata, no internal services."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""

        # Allow Meta Graph API regardless
        if "facebook.com" in host or "graph.facebook.com" in host:
            return True

        # Resolve hostname to IP
        try:
            addr = socket.getaddrinfo(host, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
            ips = {ipaddress.ip_address(a[4][0]) for a in addr}
        except socket.gaierror:
            return True  # unresolvable = let it fail naturally

        for ip in ips:
            for net in BLOCKED_NETS:
                if ip in net:
                    return False
        return True
    except Exception:
        return False


class ScraperHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._json_response({"status": "ok"})
        else:
            self._json_response({"error": "not found"}, 404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length else {}

        if self.path == "/fetch":
            self._handle_fetch(body)
        elif self.path == "/search":
            self._handle_meta_search(body)
        else:
            self._json_response({"error": "not found"}, 404)

    def _handle_fetch(self, body):
        """Fetch a URL. Use stealth=true for JS-heavy/protected pages."""
        url = body.get("url")
        if not url:
            self._json_response({"error": "url required"}, 400)
            return

        if not is_url_safe(url):
            self._json_response({"error": "blocked: private/internal URL"}, 403)
            return

        stealth = body.get("stealth", False)
        selector = body.get("selector")  # CSS selector to extract
        timeout = body.get("timeout", 30000)

        try:
            if stealth:
                Stealth = get_stealthy()
                page = Stealth.fetch(
                    url,
                    headless=True,
                    network_idle=True,
                    timeout=timeout,
                    block_images=True,
                )
            else:
                F = get_fetcher()
                page = F.get(url, stealthy_headers=True, timeout=timeout // 1000)

            result = {"url": url, "status": page.status}

            if selector:
                elements = page.css(selector)
                result["elements"] = [
                    {
                        "text": el.text or "",
                        "html": str(el) if el is not None else "",
                        "attribs": dict(el.attrib) if hasattr(el, "attrib") else {},
                    }
                    for el in elements[:100]  # cap at 100
                ]
                result["count"] = len(elements)
            else:
                text = page.get_all_text(ignore_tags=("script", "style", "noscript"))
                # Truncate to 50K chars
                result["text"] = text[:50000] if text else ""

            self._json_response(result)

        except Exception as e:
            self._json_response({"error": str(e), "type": type(e).__name__}, 500)

    def _handle_meta_search(self, body):
        """Search Meta Ad Library API (official, no browser needed)."""
        access_token = body.get("access_token") or os.environ.get("META_ADS_ACCESS_TOKEN", "")
        if not access_token:
            self._json_response({"error": "access_token required (body or META_ADS_ACCESS_TOKEN env)"}, 400)
            return

        search_terms = body.get("search_terms", "")
        ad_type = body.get("ad_type", "ALL")
        country = body.get("country", "ID")  # Indonesia
        limit = body.get("limit", 50)
        fields = body.get("fields", "id,ad_creation_time,ad_delivery_start_time,ad_delivery_stop_time,ad_creative_bodies,ad_creative_link_titles,ad_creative_link_descriptions,ad_snapshot_url,page_id,page_name,publisher_platforms,estimated_audience_size,impressions,spend,currency")

        params = {
            "access_token": access_token,
            "search_terms": search_terms,
            "ad_type": ad_type,
            "ad_reached_countries": f'["{country}"]',
            "ad_active_status": body.get("status", "ALL"),
            "limit": limit,
            "fields": fields,
        }

        # Optional filters
        if body.get("page_id"):
            params["search_page_ids"] = body["page_id"]
        if body.get("category"):
            params["ad_delivery_date_min"] = body.get("date_min", "")
            params["ad_delivery_date_max"] = body.get("date_max", "")

        url = f"https://graph.facebook.com/v21.0/ads_archive?{urlencode(params)}"

        try:
            F = get_fetcher()
            page = F.get(url, stealthy_headers=False, timeout=30)
            data = page.json()
            self._json_response(data)
        except Exception as e:
            self._json_response({"error": str(e), "type": type(e).__name__}, 500)

    def _json_response(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Quiet logs
        pass


if __name__ == "__main__":
    port = int(os.environ.get("SCRAPER_PORT", "8100"))
    server = HTTPServer(("0.0.0.0", port), ScraperHandler)
    print(f"Scrapling API listening on :{port}")
    server.serve_forever()
