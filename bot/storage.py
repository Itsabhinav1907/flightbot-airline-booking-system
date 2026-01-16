# bot/storage.py

import json
import os

BOOKINGS_FILE = "data/bookings.json"


def load_bookings():
    if not os.path.exists(BOOKINGS_FILE):
        return {}
    try:
        with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # fallback for corrupted JSON
        return {}


def save_bookings(bookings):
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookings, f, indent=2)

