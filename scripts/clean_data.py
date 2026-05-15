# ------------------------------------------------------------
# clean_data.py
# This script is used to clean and standardize the raw JSON
# datasets used in our travel planning project.
#
# Why we are doing this:
# - Raw datasets may use different field names
# - Different files may follow different structures
# - Cleaning once makes tool building easier later
#
# In this first version, we are only cleaning flights.json
# and creating a new cleaned file called flights_cleaned.json
# ------------------------------------------------------------

# Importing required libraries
import json
import os
from datetime import datetime

# ------------------------------------------------------------
# Build file paths
# BASE_DIR points to the root project folder
# DATA_DIR points to the data folder
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Raw input file path
FLIGHTS_RAW_PATH = os.path.join(DATA_DIR, "flights.json")

# Cleaned output file path
FLIGHTS_CLEANED_PATH = os.path.join(DATA_DIR, "flights_cleaned.json")


def calculate_duration_minutes(departure_time, arrival_time):
    """
    This function calculates flight duration in minutes
    using departure and arrival timestamps.
    """
    try:
        # Convert string timestamps into datetime objects
        departure = datetime.fromisoformat(departure_time)
        arrival = datetime.fromisoformat(arrival_time)

        # Find time difference in seconds and convert to minutes
        duration = arrival - departure
        duration_minutes = int(duration.total_seconds() / 60)

        return duration_minutes

    except Exception:
        # If any issue happens while parsing date/time,
        # return None so that we can identify problematic rows
        return None


def clean_flights_data():
    """
    This function reads raw flights.json,
    standardizes field names,
    adds calculated duration_minutes,
    and saves cleaned data into flights_cleaned.json
    """
    # Open raw flights data
    with open(FLIGHTS_RAW_PATH, "r", encoding="utf-8") as file:
        raw_flights = json.load(file)

    # This list will store all cleaned flight records
    cleaned_flights = []

    # Loop through each raw flight record one by one
    for flight in raw_flights:
        # Calculate duration in minutes
        duration_minutes = calculate_duration_minutes(
            flight.get("departure_time"),
            flight.get("arrival_time")
        )

        # Create a cleaned flight record with standardized keys
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

        # Add cleaned record to the final list
        cleaned_flights.append(cleaned_flight)

    # Save cleaned data to a new JSON file
    with open(FLIGHTS_CLEANED_PATH, "w", encoding="utf-8") as file:
        json.dump(cleaned_flights, file, indent=4)

    # Print a success message so we know it worked
    print("Flights data cleaned successfully.")
    print(f"Cleaned file saved at: {FLIGHTS_CLEANED_PATH}")
    print(f"Total cleaned flight records: {len(cleaned_flights)}")


# ------------------------------------------------------------
# This block runs only when this file is executed directly
# ------------------------------------------------------------
if __name__ == "__main__":
    clean_flights_data()