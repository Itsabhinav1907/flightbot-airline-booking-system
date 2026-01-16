# bot/utils.py

import re
import random
import string
import calendar
from datetime import datetime, date


def gen_pnr():
    chars = string.ascii_uppercase + string.digits
    while True:
        p = ''.join(random.choice(chars) for _ in range(6))
        if any(c.isdigit() for c in p):
            return p


CITY_ALIASES = {
    "ben": "Bengaluru", "blr": "Bengaluru", "bangalore": "Bengaluru",
    "del": "Delhi", "delhi": "Delhi",
    "mum": "Mumbai", "mumbai": "Mumbai",
    "hyd": "Hyderabad", "hyderabad": "Hyderabad",
    "chen": "Chennai", "chennai": "Chennai",
    "kol": "Kolkata", "kolkata": "Kolkata",
}


def normalize_city(text):
    t = text.lower().strip()
    if t in CITY_ALIASES:
        return CITY_ALIASES[t]
    return " ".join(w.capitalize() for w in text.split())


def safe_int(text):
    try:
        return int(re.search(r"\d+", str(text)).group())
    except:
        return None


def parse_date_flexible(text):
    if not text:
        return None

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d %b %Y",
        "%d %B %Y"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            pass

    m = re.match(r"(\d{1,2})\s+([A-Za-z]+)", text.strip())
    if m:
        day = int(m.group(1))
        month = m.group(2)[:3].title()
        month_map = {calendar.month_abbr[i]: i for i in range(1, 13)}
        if month in month_map:
            year = date.today().year
            d = date(year, month_map[month], day)
            if d < date.today():
                d = date(year + 1, month_map[month], day)
            return d

    return None


def date_to_display(d):
    return d.strftime("%Y-%m-%d")
