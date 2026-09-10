#!/usr/bin/env python3
"""Validate official source URLs referenced by data/events.json."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "events.json"
USER_AGENT = "Mozilla/5.0 (compatible; ChinaCalendarBot/1.0; +https://github.com/charles0506/china-political-calendar)"


def check_url(url: str) -> tuple[bool, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = getattr(response, "status", 200)
            return 200 <= status < 400, f"HTTP {status}"
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit with status 1 when any source URL fails",
    )
    args = parser.parse_args()

    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    events = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    urls = sorted({event.get("source") for event in events if event.get("source")})

    failed = 0
    for url in urls:
        ok, detail = check_url(url)
        marker = "OK" if ok else "FAIL"
        print(f"[{marker}] {detail} {url}")
        if not ok:
            failed += 1
            if in_actions:
                print(f"::warning title=Source URL check failed::{detail} {url}")

    if failed:
        print(f"\n{failed} of {len(urls)} source URL(s) failed validation.", file=sys.stderr)
        # Official Chinese sites often block or break TLS for overseas runners,
        # so failures are warnings unless --strict is given.
        return 1 if args.strict else 0

    print(f"\nValidated {len(urls)} unique source URL(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
