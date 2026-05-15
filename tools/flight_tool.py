# -------------------------------------------------------
# flight_tool.py
# This file is responsible for searching flights
# from our local flights.json dataset.
# The agent will call this tool when user asks about flights.
# -------------------------------------------------------

# Importing required libraries
import json                          # to read our flights.json file
import os                            # to build correct file path
from datetime import datetime        # to calculate flight duration from times

# Importing the tool decorator from langchain
# @tool converts a normal python function into a LangChain tool
from langchain.tools import tool

# -------------------------------------------------------
# Building the path to our flights.json file
# __file__ refers to the current file (flight_tool.py)
# we go one level up (..) to reach root, then into data/
# -------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "flights.json")


def load_flights():
    # This function opens flights.json and loads all
    # flight records into a Python list of dictionaries
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data


def calculate_duration(departure_str, arrival_str):
    # This function calculates how long the flight is
    # by finding the difference between arrival and departure times
    # The time format in our JSON is like: '2025-01-04T11:32:00'
    try:
        # Parse both times using the datetime format from JSON
        departure = datetime.fromisoformat(departure_str)
        arrival = datetime.fromisoformat(arrival_str)

        # Find the difference and convert to total minutes
        diff = arrival - departure
        total_minutes = int(diff.total_seconds() / 60)

        # Convert to hours and remaining minutes for display
        hours = total_minutes // 60
        minutes = total_minutes % 60

        return f"{hours}h {minutes}m", total_minutes

    except Exception:
        # If time parsing fails, return unknown
        return "Unknown", 9999


@tool
def flight_search_tool(query: str) -> str:
    """
    Search for available flights based on source and destination city.
    Input format: 'source to destination'
    Example: 'Delhi to Goa'
    Returns the cheapest and fastest flight options available.
    """

    try:
        # -------------------------------------------------------
        # Step 1: Parse the user query
        # The agent sends input like "Delhi to Goa"
        # We split it by " to " to get source and destination
        # -------------------------------------------------------
        parts = query.lower().split(" to ")

        # If we don't get exactly 2 parts, the format is wrong
        if len(parts) != 2:
            return "Please use the format: 'CityA to CityB'. Example: 'Delhi to Goa'"

        # Clean up any extra spaces from both city names
        source = parts[0].strip()
        destination = parts[1].strip()

        # -------------------------------------------------------
        # Step 2: Load all flights from our JSON dataset
        # -------------------------------------------------------
        flights = load_flights()

        # -------------------------------------------------------
        # Step 3: Filter flights matching source and destination
        # Note: In our JSON the fields are "from" and "to"
        # not "source" and "destination"
        # -------------------------------------------------------
        filtered_flights = []

        for flight in flights:
            # Get the from and to fields from each flight record
            # and convert to lowercase for comparison
            flight_from = flight.get("from", "").lower()
            flight_to = flight.get("to", "").lower()

            # Only keep flights where both cities match
            if flight_from == source and flight_to == destination:
                filtered_flights.append(flight)

        # If no matching flights found, return friendly message
        if not filtered_flights:
            return f"Sorry, no flights found from {source.title()} to {destination.title()}."

        # -------------------------------------------------------
        # Step 4: Calculate duration for each flight
        # and add it to the flight dictionary for sorting
        # -------------------------------------------------------
        for flight in filtered_flights:
            duration_str, duration_mins = calculate_duration(
                flight.get("departure_time", ""),
                flight.get("arrival_time", "")
            )
            # Store both human-readable and numeric duration
            flight["duration_display"] = duration_str
            flight["duration_mins"] = duration_mins

        # -------------------------------------------------------
        # Step 5: Find cheapest flight by sorting on price
        # -------------------------------------------------------
        cheapest_flight = sorted(filtered_flights, key=lambda x: x.get("price", 0))[0]

        # -------------------------------------------------------
        # Step 6: Find fastest flight by sorting on duration
        # -------------------------------------------------------
        fastest_flight = sorted(filtered_flights, key=lambda x: x.get("duration_mins", 9999))[0]

        # -------------------------------------------------------
        # Step 7: Build a clean readable result string
        # -------------------------------------------------------
        result = f"Flights from {source.title()} to {destination.title()}:\n\n"

        # Add cheapest flight details
        result += f"Cheapest Option:\n"
        result += f"  Airline  : {cheapest_flight.get('airline')}\n"
        result += f"  Price    : Rs.{cheapest_flight.get('price')}\n"
        result += f"  Departure: {cheapest_flight.get('departure_time')}\n"
        result += f"  Duration : {cheapest_flight.get('duration_display')}\n\n"

        # Only show fastest separately if it is a different flight
        if fastest_flight.get("flight_id") != cheapest_flight.get("flight_id"):
            result += f"Fastest Option:\n"
            result += f"  Airline  : {fastest_flight.get('airline')}\n"
            result += f"  Price    : Rs.{fastest_flight.get('price')}\n"
            result += f"  Departure: {fastest_flight.get('departure_time')}\n"
            result += f"  Duration : {fastest_flight.get('duration_display')}\n"

        # Return the final result back to the agent
        return result

    except Exception as e:
        # If anything goes wrong, return the error so we can debug
        return f"Error while searching for flights: {str(e)}"