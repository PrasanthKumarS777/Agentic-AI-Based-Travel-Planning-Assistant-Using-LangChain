# -------------------------------------------------------
# places_tool.py
# This tool searches tourist places from the cleaned
# places dataset.
#
# The cleaned dataset uses:
# - category instead of type
# - rating for sorting
#
# This makes the code simple and consistent.
# -------------------------------------------------------

import json
import os

from langchain.tools import tool

# -------------------------------------------------------
# Build the path to the cleaned places file
# -------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "places_cleaned.json")


def load_places():
    """
    Load cleaned place records from places_cleaned.json.
    """
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@tool
def places_search_tool(query: str) -> str:
    """
    Search tourist places in a city.

    Example input:
    'Delhi'

    This tool returns top places based on higher rating.
    """
    try:
        # -------------------------------------------------------
        # Clean the city name from input
        # -------------------------------------------------------
        city_name = query.strip().lower()

        if not city_name:
            return "Please enter a city name to search places."

        # -------------------------------------------------------
        # Load cleaned place data
        # -------------------------------------------------------
        places = load_places()

        # -------------------------------------------------------
        # Filter places by city
        # -------------------------------------------------------
        matching_places = []

        for place in places:
            place_city = str(place.get("city", "")).lower()

            if place_city == city_name:
                matching_places.append(place)

        # -------------------------------------------------------
        # If nothing matches, return a friendly message
        # -------------------------------------------------------
        if not matching_places:
            return f"No tourist places found in {city_name.title()}."

        # -------------------------------------------------------
        # Sort by rating in descending order
        # -------------------------------------------------------
        sorted_places = sorted(
            matching_places,
            key=lambda x: x.get("rating", 0),
            reverse=True
        )

        # Take top 5 places to keep output readable
        top_places = sorted_places[:5]

        # -------------------------------------------------------
        # Build the final readable result
        # -------------------------------------------------------
        result = f"Top tourist places in {city_name.title()}:\n\n"

        for index, place in enumerate(top_places, start=1):
            result += f"{index}. {place.get('name')}\n"
            result += f"   Place ID  : {place.get('place_id')}\n"
            result += f"   City      : {place.get('city')}\n"
            result += f"   Category  : {place.get('category')}\n"
            result += f"   Rating    : {place.get('rating')}\n\n"

        return result

    except Exception as e:
        return f"Error while searching places: {str(e)}"