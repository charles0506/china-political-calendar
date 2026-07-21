#!/usr/bin/env python3
"""Build china-political-calendar.ics from data/events.json."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "events.json"
OUTPUT_FILE = ROOT / "china-political-calendar.ics"


def escape_ics(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\r\n", "\\n")
        .replace("\n", "\\n")
    )


def fold_line(line: str, limit: int = 73) -> list[str]:
    """Fold an iCalendar line without splitting UTF-8 code points."""
    encoded = line.encode("utf-8")
    chunks: list[str] = []
    first = True
    while encoded:
        size = limit if first else limit - 1
        cut = min(size, len(encoded))
        while cut > 0:
            try:
                part = encoded[:cut].decode("utf-8")
                break
            except UnicodeDecodeError:
                cut -= 1
        if cut == 0:
            raise ValueError("Unable to fold UTF-8 line")
        chunks.append(("" if first else " ") + part)
        encoded = encoded[cut:]
        first = False
    return chunks or [""]


def add(lines: list[str], line: str) -> None:
    lines.extend(fold_line(line))


def main() -> None:
    events = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    events.sort(key=lambda event: (event["start"], event["summary"]))

    now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines: list[str] = []
    for line in (
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//charles0506//China Political Calendar//ZH-TW",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:中國重要政治會議",
        "X-WR-CALDESC:中國重要例行政治會議、正式會期與待官宣觀察窗",
        "X-WR-TIMEZONE:Asia/Shanghai",
        "REFRESH-INTERVAL;VALUE=DURATION:P1D",
        "X-PUBLISHED-TTL:P1D",
    ):
        add(lines, line)

    for event in events:
        description = event["description"]
        source = event.get("source")
        if source:
            description = f"{description}\n來源：{source}"

        add(lines, "BEGIN:VEVENT")
        add(lines, f"UID:{escape_ics(event['uid'])}")
        add(lines, f"DTSTAMP:{now}")
        add(lines, f"DTSTART;VALUE=DATE:{event['start'].replace('-', '')}")
        add(lines, f"DTEND;VALUE=DATE:{event['end'].replace('-', '')}")
        add(lines, f"SUMMARY:{escape_ics(event['summary'])}")
        add(lines, f"DESCRIPTION:{escape_ics(description)}")
        add(lines, f"LOCATION:{escape_ics(event.get('location', '北京'))}")
        add(lines, f"STATUS:{event.get('status', 'TENTATIVE')}")
        add(lines, f"SEQUENCE:{int(event.get('sequence', 0))}")
        add(lines, "TRANSP:TRANSPARENT")
        if source:
            add(lines, f"URL:{source}")
        add(lines, "END:VEVENT")

    add(lines, "END:VCALENDAR")
    OUTPUT_FILE.write_text("\r\n".join(lines) + "\r\n", encoding="utf-8", newline="")
    print(f"Wrote {OUTPUT_FILE} with {len(events)} events")


if __name__ == "__main__":
    main()
