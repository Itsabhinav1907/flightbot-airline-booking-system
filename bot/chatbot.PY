# bot/chatbot.py

from datetime import date

from bot.constants import DISCOUNTS, STUDENT_MIN_AGE, FLIGHTS
from bot.utils import (
    gen_pnr,
    normalize_city,
    safe_int,
    parse_date_flexible,
    date_to_display
)
from bot.storage import load_bookings, save_bookings
from bot.states import State


class FlightBot:

    def __init__(self):
        self.bookings = load_bookings()
        self.reset()

    def reset(self):
        self.state = State.START
        self.mode = None
        self.origin = None
        self.dest = None
        self.travel_date = None
        self.adults = None
        self.seat_class = None

    def _reset_booking_data(self):
        self.origin = None
        self.dest = None
        self.travel_date = None
        self.adults = None
        self.seat_class = None

    # ---------------- REFUND LOGIC ----------------
    def _calculate_refund(self, booking):
        if booking.get("payment_status") != "PAID":
            return 0, 0

        travel_date_str = booking.get("travel_date") or booking.get("depart")
        if not travel_date_str:
            return 0, booking.get("total", 0)

        travel_date = date.fromisoformat(travel_date_str)
        today = date.today()
        days_left = (travel_date - today).days

        total = booking.get("total", 0)

        if days_left > 7:
            charge_pct = 0.10
        elif 2 <= days_left <= 7:
            charge_pct = 0.25
        elif days_left >= 0:
            charge_pct = 0.50
        else:
            charge_pct = 1.00

        charge = int(total * charge_pct)
        refund = total - charge
        return charge, refund

    # ---------------- SHOW BOOKINGS ----------------
    def _show_bookings(self, current_user):
        lines = ["📋 Your bookings:"]

        for pnr, b in self.bookings.items():
            if b.get("username") != current_user:
                continue

            travel_date = (
                b.get("travel_date")
                or b.get("depart")
                or "N/A"
            )

            lines.append(
                f"PNR: {pnr} | "
                f"{b.get('origin', 'N/A')} → {b.get('destination', 'N/A')} | "
                f"Date: {travel_date} | "
                f"Status: {b.get('status', 'UNKNOWN')}"
            )

        if len(lines) == 1:
            return "You have no bookings."

        lines.append("\nType the PNR to cancel a booking, or type BACK to return.")
        return "\n".join(lines)

    # ---------------- MAIN CHAT ----------------
    def respond(self, text, username=None):
        current_user = username
        text = text.strip().lower()

        if text in ("end", "exit", "quit"):
            return "Goodbye — safe travels!"

        # -------- START --------
        if self.state == State.START:
            if "book" in text:
                self.mode = "BOOK"
                self.state = State.ASK_TRIP_TYPE
                return "Do you want ONE-WAY or ROUND-TRIP?"

            if "cancel" in text:
                self.state = State.CANCEL_LIST
                return self._show_bookings(current_user)

        # -------- TRIP TYPE --------
        if self.mode == "BOOK" and self.state == State.ASK_TRIP_TYPE:
            if "one" in text:
                self.state = State.ASK_ROUTE
                return "Enter route (e.g., Bengaluru to Delhi)"
            return "Please choose ONE-WAY."

        # -------- ROUTE --------
        if self.state == State.ASK_ROUTE:
            parts = text.split("to")
            if len(parts) == 2:
                self.origin = normalize_city(parts[0])
                self.dest = normalize_city(parts[1])
                self.state = State.ASK_DATE
                return "Enter travel date (YYYY-MM-DD)"
            return "Invalid route format."

        # -------- DATE --------
        if self.state == State.ASK_DATE:
            d = parse_date_flexible(text)
            if not d or d < date.today():
                return "Enter a valid future date."
            self.travel_date = d
            self.state = State.ASK_ADULTS
            return "How many adults?"

        # -------- ADULTS --------
        if self.state == State.ASK_ADULTS:
            n = safe_int(text)
            if not n:
                return "Enter number of adults."
            self.adults = n
            self.state = State.ASK_SEAT
            return "Economy or Business?"

        # -------- SEAT + BOOK --------
        if self.state == State.ASK_SEAT:
            if "eco" in text:
                self.seat_class = "economy"
            elif "bus" in text:
                self.seat_class = "business"
            else:
                return "Please choose Economy or Business."

            pnr = gen_pnr()
            base = 4500 if self.seat_class == "economy" else 7200
            total = base * self.adults

            booking = {
                "pnr": pnr,
                "username": current_user,
                "origin": self.origin,
                "destination": self.dest,
                "travel_date": date_to_display(self.travel_date),
                "adults": self.adults,
                "seat_class": self.seat_class,
                "total": total,
                "payment_status": "PAID",
                "payment_mode": "SIMULATED",
                "payment_id": f"PAY{pnr}",
                "status": "CONFIRMED"
            }

            self.bookings[pnr] = booking
            save_bookings(self.bookings)

            response = (
                f"✅ Booking Confirmed!\n"
                f"PNR: {pnr}\n"
                f"Route: {self.origin} → {self.dest}\n"
                f"Date: {booking['travel_date']}\n"
                f"Passengers: {self.adults}\n"
                f"Class: {self.seat_class.title()}"
            )

            self._reset_booking_data()
            self.state = State.END
            return response

        # -------- CANCEL --------
        if self.state == State.CANCEL_LIST:
            if text == "back":
                self.reset()
                return "Do you want to BOOK a ticket or CANCEL a ticket?"

            pnr = text.upper()

            if pnr not in self.bookings:
                return "❌ Invalid PNR. Please enter a valid PNR or type BACK."

            booking = self.bookings[pnr]

            if booking.get("username") != current_user:
                return "❌ You are not authorized to cancel this booking."

            if booking.get("status") == "CANCELLED":
                return f"⚠️ Booking {pnr} is already cancelled."

            booking["status"] = "CANCELLED"
            charge, refund = self._calculate_refund(booking)

            booking["cancellation_charge"] = charge
            booking["refund_amount"] = refund
            save_bookings(self.bookings)

            self.state = State.END
            return (
                f"✅ Booking Cancelled Successfully\n"
                f"PNR: {pnr}\n"
                f"Route: {booking['origin']} → {booking['destination']}\n"
                f"Payment Status: {booking['payment_status']}\n"
                f"Cancellation Charge: ₹{charge}\n"
                f"Refund Amount: ₹{refund}"
            )

        # -------- END --------
        if self.state == State.END:
            if "book" in text:
                self.reset()
                self.mode = "BOOK"
                self.state = State.ASK_TRIP_TYPE
                return "Do you want ONE-WAY or ROUND-TRIP?"

            if "cancel" in text:
                self.reset()
                self.state = State.CANCEL_LIST
                return self._show_bookings(current_user)

            return "Type BOOK to make a new booking or END to exit."
