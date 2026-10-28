"""Minimal client for Kalshi's public (no-login) market data API.

Two functions:
  get(path, params)            -> one request, with a polite delay and retries
  paginate(path, params, key)  -> follows the cursor and yields every item
"""

import logging
import time

import requests

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

# Kalshi's basic tier allows ~20 reads/sec. Sleeping 0.15s between calls keeps us
# around 6/sec, well under the limit, so we rarely hit a 429 in the first place.
DELAY_SECONDS = 0.15
# Under load (e.g., several downloads at once) 429s are normal, so be patient: 8 retries
# back off 1s, 2s, ... 128s, about 4 minutes in total, before giving up.
MAX_RETRIES = 8

log = logging.getLogger("kalshi_api")


def get(path, params=None):
    """GET BASE_URL + path and return the parsed JSON.

    Retries on 429 (rate limited) and 5xx (server errors) with exponential
    backoff: wait 1s, 2s, 4s, ... doubling up to MAX_RETRIES times, then give up.
    Kalshi doesn't send a Retry-After header, so backoff is the documented approach.
    """
    url = BASE_URL + path
    for attempt in range(MAX_RETRIES + 1):
        time.sleep(DELAY_SECONDS)
        try:
            response = requests.get(url, params=params, timeout=30)
        except requests.RequestException as error:
            # Network hiccup (timeout, dropped connection): treat it like a 5xx.
            status = f"network error: {error}"
        else:
            if response.status_code == 200:
                return response.json()
            if response.status_code != 429 and response.status_code < 500:
                # 400/404 etc. won't succeed on retry, so fail right away.
                response.raise_for_status()
            status = response.status_code

        if attempt == MAX_RETRIES:
            raise RuntimeError(f"Giving up on {url} after {MAX_RETRIES} retries ({status})")
        wait = 2 ** attempt
        log.warning("%s on %s, retrying in %ss", status, path, wait)
        time.sleep(wait)


def paginate(path, params, key):
    """Yield every item in response[key], following the cursor across pages."""
    params = dict(params)
    while True:
        page = get(path, params)
        yield from page.get(key, [])
        cursor = page.get("cursor")
        if not cursor:
            return
        params["cursor"] = cursor
