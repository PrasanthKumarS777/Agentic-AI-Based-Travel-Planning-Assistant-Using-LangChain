# -------------------------------------------------------
# flight_tool.py
# This tool searches flights from the cleaned flights dataset.
# The cleaned dataset uses:
# - source
# - destination
# - duration_minutes
#
# This makes the code easier to read and easier to debug.
# -------------------------------------------------------

import json
import os

from langchain.tools import tool

# -------------------------------------------------------
# Build the path to the cleaned flights file
# -------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "flights_cleaned.json")

def format_duration(minutes):
    hours, mins = divmod(int(minutes), 60)
    if hours and mins:
        return f"{hours}h {mins}m"
    if hours:
        return f"{hours}h"
    return f"{mins}m"
    
def load_flights():
    """
    Load cleaned flight records from flights_cleaned.json.
    """
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@tool
def flight_search_tool(query: str) -> str:
    """
    Search for flights using a query like:
    'Delhi to Kolkata'
    """
    try:
        # -------------------------------------------------------
        # Split the input into source and destination
        # -------------------------------------------------------
        parts = query.lower().split(" to ")

        if len(parts) != 2:
            return "Please use the format: 'CityA to CityB'. Example: 'Delhi to Kolkata'"

        source = parts[0].strip()
        destination = parts[1].strip()

        # -------------------------------------------------------
        # Load all cleaned flight records
        # -------------------------------------------------------
        flights = load_flights()

        # -------------------------------------------------------
        # Find matching flights
        # -------------------------------------------------------
        matching_flights = []

        for flight in flights:
            flight_source = str(flight.get("source", "")).lower()
            flight_destination = str(flight.get("destination", "")).lower()

            if flight_source == source and flight_destination == destination:
                matching_flights.append(flight)

        # -------------------------------------------------------
        # If no flights are found, return a simple message
        # -------------------------------------------------------
        if not matching_flights:
            return f"No flights found from {source.title()} to {destination.title()}."

        # -------------------------------------------------------
        # Sort by price for cheapest flight
        # -------------------------------------------------------
        cheapest_flight = sorted(
            matching_flights,
            key=lambda x: x.get("price", 0)
        )[0]

        # -------------------------------------------------------
        # Sort by duration for fastest flight
        # -------------------------------------------------------
        fastest_flight = sorted(
            matching_flights,
            key=lambda x: x.get("duration_minutes", 999999)
        )[0]

        # -------------------------------------------------------
        # Build the output in a readable format
        # -------------------------------------------------------
        result = f"Flights from {source.title()} to {destination.title()}:\n\n"

        result += "Cheapest Option:\n"
        result += f"  Airline   : {cheapest_flight.get('airline')}\n"
        result += f"  Price     : Rs.{cheapest_flight.get('price')}\n"
        result += f"  Departure : {cheapest_flight.get('departure_time')}\n"
        result += f"  Duration  : {cheapest_flight.get('duration_minutes')} minutes\n\n"

        # Show fastest only if different from cheapest
        if fastest_flight.get("flight_id") != cheapest_flight.get("flight_id"):
            result += "Fastest Option:\n"
            result += f"  Airline   : {fastest_flight.get('airline')}\n"
            result += f"  Price     : Rs.{fastest_flight.get('price')}\n"
            result += f"  Departure : {fastest_flight.get('departure_time')}\n"
            result += f"  Duration  : {fastest_flight.get('duration_minutes')} minutes\n"

        return result

    except Exception as e:
        return f"Error while searching flights: {str(e)}"