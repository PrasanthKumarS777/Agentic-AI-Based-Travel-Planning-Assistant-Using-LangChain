# ------------------------------------------------------------
# clean_data.py
# This script cleans and standardizes all raw JSON datasets
# used in our Agentic AI Travel Planner project.
#
# Why this script is useful:
# - Raw datasets use different field names
# - Some files use source/destination, some use from/to
# - Hotels use stars instead of rating
# - Places use type instead of category
#
# To make tool building easier, we convert all datasets into
# a cleaner and more consistent structure.
# ------------------------------------------------------------

# Import required libraries
import json
import os
from datetime import datetime

# ------------------------------------------------------------
# Define base folder paths
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# ------------------------------------------------------------
# Raw dataset paths
# ------------------------------------------------------------
FLIGHTS_RAW_PATH = os.path.join(DATA_DIR, "flights.json")
HOTELS_RAW_PATH = os.path.join(DATA_DIR, "hotels.json")
PLACES_RAW_PATH = os.path.join(DATA_DIR, "places.json")

# ------------------------------------------------------------
# Cleaned dataset paths
# ------------------------------------------------------------
FLIGHTS_CLEANED_PATH = os.path.join(DATA_DIR, "flights_cleaned.json")
HOTELS_CLEANED_PATH = os.path.join(DATA_DIR, "hotels_cleaned.json")
PLACES_CLEANED_PATH = os.path.join(DATA_DIR, "places_cleaned.json")


def calculate_duration_minutes(departure_time, arrival_time):
    """
    This function calculates flight duration in minutes
    using departure and arrival timestamps.
    """
    try:
        departure = datetime.fromisoformat(departure_time)
        arrival = datetime.fromisoformat(arrival_time)

        duration = arrival - departure
        duration_minutes = int(duration.total_seconds() / 60)

        return duration_minutes

    except Exception:
        return None


def clean_flights_data():
    """
    Clean and standardize flights dataset.
    Changes:
    - from -> source
    - to -> destination
    - add duration_minutes
    """
    with open(FLIGHTS_RAW_PATH, "r", encoding="utf-8") as file:
        raw_flights = json.load(file)

    cleaned_flights = []

    for flight in raw_flights:
        duration_minutes = calculate_duration_minutes(
            flight.get("departure_time"),
            flight.get("arrival_time")
        )

        cleaned_flight = {
            "flight_id": flight.get("flight_id"),
            "airline": flight.get("airline"),
            "source": flight.get("from"),
            "destination": flight.get("to"),
            "departure_time": flight.get("departure_time"),
            "arrival_time": flight.get("arrival_time"),
            "price": flight.get("price"),
            "duration_minutes": duration_minutes
        }

        cleaned_flights.append(cleaned_flight)

    with open(FLIGHTS_CLEANED_PATH, "w", encoding="utf-8") as file:
        json.dump(cleaned_flights, file, indent=4)

    print("Flights data cleaned successfully.")
    print(f"Total cleaned flight records: {len(cleaned_flights)}")


def clean_hotels_data():
    """
    Clean and standardize hotels dataset.
    Changes:
    - stars -> rating
    """
    with open(HOTELS_RAW_PATH, "r", encoding="utf-8") as file:
        raw_hotels = json.load(file)

    cleaned_hotels = []

    for hotel in raw_hotels:
        cleaned_hotel = {
            "hotel_id": hotel.get("hotel_id"),
            "name": hotel.get("name"),
            "city": hotel.get("city"),
            "rating": hotel.get("stars"),
            "price_per_night": hotel.get("price_per_night"),
            "amenities": hotel.get("amenities", [])
        }

        cleaned_hotels.append(cleaned_hotel)

    with open(HOTELS_CLEANED_PATH, "w", encoding="utf-8") as file:
        json.dump(cleaned_hotels, file, indent=4)

    print("Hotels data cleaned successfully.")
    print(f"Total cleaned hotel records: {len(cleaned_hotels)}")


def clean_places_data():
    """
    Clean and standardize places dataset.
    Changes:
    - type -> category
    """
    with open(PLACES_RAW_PATH, "r", encoding="utf-8") as file:
        raw_places = json.load(file)

    cleaned_places = []

    for place in raw_places:
        cleaned_place = {
            "place_id": place.get("place_id"),
            "name": place.get("name"),
            "city": place.get("city"),
            "category": place.get("type"),
            "rating": place.get("rating")
        }

        cleaned_places.append(cleaned_place)

    with open(PLACES_CLEANED_PATH, "w", encoding="utf-8") as file:
        json.dump(cleaned_places, file, indent=4)

    print("Places data cleaned successfully.")
    print(f"Total cleaned place records: {len(cleaned_places)}")


if __name__ == "__main__":
    print("Starting dataset cleaning process...\n")

    clean_flights_data()
    print()

    clean_hotels_data()
    print()

    clean_places_data()
    print()

    print("All datasets cleaned and saved successfully.")