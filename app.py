# app.py

from bot.chatbot import FlightBot

def main():
    bot = FlightBot()
    print("FlightBot: Do you want to BOOK a ticket or CANCEL a ticket?")
    print("(Type 'BOOK' or 'CANCEL'. Type 'END' to finish.)\n")

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nFlightBot: Goodbye — safe travels!")
            break

        if user.lower() in ("end", "exit", "quit"):
            print("FlightBot: Goodbye — safe travels!")
            break
        reply = bot.respond(user)
        print("\nFlightBot:", reply, "\n")

if __name__ == "__main__":
    main()