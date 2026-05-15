# -------------------------------------------------------
# travel_agent.py
# This file acts as the main controller of the travel planner.
#
# It takes a user query, extracts travel details,
# calls different tools one by one,
# and combines all results into one final travel plan.
# -------------------------------------------------------

import os
import re
import sys

# -------------------------------------------------------
# Add project root folder to Python path
# This helps Python find the tools/ folder correctly
# even when we run this file directly from agents/
# -------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

# -------------------------------------------------------
# Import all tool functions
# -------------------------------------------------------
from tools.flight_tool import flight_search_tool
from tools.hotel_tool import hotel_search_tool
from tools.places_tool import places_search_tool
from tools.weather_tool import weather_tool
from tools.budget_tool import budget_tool

def extract_first_price(text):
    """
    This function looks through text and tries to find the first price value.

    We use it to extract flight and hotel prices from tool outputs.
    """
    price_match = re.search(r"Rs\.(\d+)", text)

    if price_match:
        return int(price_match.group(1))

    return None

def extract_trip_details(user_query):
    """
    This function extracts basic trip information
    from the user query.

    We try to find:
    - source city
    - destination city
    - number of days
    - budget
    """
    query = user_query.lower()

    source = None
    destination = None
    days = 3
    budget = None

    # -------------------------------------------------------
    # Extract number of days from text
    # Example: "3 day trip"
    # -------------------------------------------------------
    day_match = re.search(r"(\d+)\s*day", query)
    if day_match:
        days = int(day_match.group(1))

    # -------------------------------------------------------
    # Extract budget from text
    # Example: "budget of 15000"
    # -------------------------------------------------------
    budget_match = re.search(r"budget\s*(of)?\s*(\d+)", query)
    if budget_match:
        budget = int(budget_match.group(2))

    # -------------------------------------------------------
    # Extract source and destination more carefully
    # This pattern stops destination before:
    # - with
    # - under
    # - for
    # - budget
    # - end of line
    # Example:
    # "from Delhi to Goa with a budget of 15000"
    # -------------------------------------------------------
    route_match = re.search(
        r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+?)(?:\s+with|\s+under|\s+for|\s+budget|$)",
        query
    )

    if route_match:
        source = route_match.group(1).strip().title()
        destination = route_match.group(2).strip().title()

    return {
        "source": source,
        "destination": destination,
        "days": days,
        "budget": budget
    }


def run_travel_agent(user_query):
    """
    This function runs the full travel planning process.
    """
    try:
        # -------------------------------------------------------
        # Extract trip details from user input
        # -------------------------------------------------------
        trip_details = extract_trip_details(user_query)

        source = trip_details["source"]
        destination = trip_details["destination"]
        days = trip_details["days"]
        budget = trip_details["budget"]

        # -------------------------------------------------------
        # Validate source and destination
        # -------------------------------------------------------
        if not source or not destination:
            return (
                "Could not understand source and destination.\n"
                "Please use a format like:\n"
                "Plan a 3 day trip from Delhi to Goa with a budget of 15000"
            )

        # -------------------------------------------------------
        # Call each tool one by one
        # -------------------------------------------------------
        flight_result = flight_search_tool.run(f"{source} to {destination}")
        hotel_result = hotel_search_tool.run(destination)
        places_result = places_search_tool.run(destination)
        weather_result = weather_tool.run(destination)

               # -------------------------------------------------------
        # Extract real values from the tool outputs
        # If a price is not found, we keep a simple fallback
        # -------------------------------------------------------
        flight_price = extract_first_price(flight_result)
        hotel_price = extract_first_price(hotel_result)

        if flight_price is None:
            flight_price = 5000

        if hotel_price is None:
            hotel_price = 3500

        daily_expense = 1000

        # -------------------------------------------------------
        # Send extracted values to the budget tool
        # -------------------------------------------------------
        budget_result = budget_tool.run(
            f"{flight_price}, {hotel_price}, {days}, {daily_expense}"
        )

        # -------------------------------------------------------
        # Build final travel plan output
        # -------------------------------------------------------
        final_result = ""
        final_result += "TRIP SUMMARY\n"
        final_result += "-------------------------\n"
        final_result += f"Source      : {source}\n"
        final_result += f"Destination : {destination}\n"
        final_result += f"Duration    : {days} days\n"

        if budget:
            final_result += f"User Budget : Rs.{budget}\n"

        final_result += "\n"

        final_result += "FLIGHT DETAILS\n"
        final_result += "-------------------------\n"
        final_result += flight_result + "\n\n"

        final_result += "HOTEL OPTIONS\n"
        final_result += "-------------------------\n"
        final_result += hotel_result + "\n\n"

        final_result += "TOP PLACES TO VISIT\n"
        final_result += "-------------------------\n"
        final_result += places_result + "\n\n"

        final_result += "WEATHER FORECAST\n"
        final_result += "-------------------------\n"
        final_result += weather_result + "\n\n"

        final_result += "BUDGET ESTIMATE\n"
        final_result += "-------------------------\n"
        final_result += budget_result + "\n"

        return final_result

    except Exception as e:
        return f"Error while running travel planner: {str(e)}"


# -------------------------------------------------------
# Run this file directly from terminal
# -------------------------------------------------------
if __name__ == "__main__":
    user_query = input("Enter your travel query: ")
    result = run_travel_agent(user_query)

    print("\nFinal Travel Plan:\n")
    print(result)