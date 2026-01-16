# bot/states.py

from enum import Enum

class State(Enum):
    START = 0
    ASK_TRIP_TYPE = 1
    ASK_ROUTE = 2
    ASK_DATE = 3
    ASK_ADULTS = 4
    ASK_SEAT = 5
    END = 99
    CANCEL_LIST = 10

