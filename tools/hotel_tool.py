# -------------------------------------------------------
# hotel_tool.py
# This tool searches hotels from the cleaned hotels dataset.
# The cleaned dataset uses:
# - rating instead of stars
# - consistent city names
#
# This makes hotel search code simpler and easier to maintain.
# -------------------------------------------------------

import json
import os

from langchain.tools import tool

# -------------------------------------------------------
# Build the path to the cleaned hotels file
# -------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hotels_cleaned.json")


def load_hotels():
    """
    Load cleaned hotel records from hotels_cleaned.json.
    """
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


@tool
def hotel_search_tool(query: str) -> str:
    """
    Search for hotels in a city.
    Example input: 'Delhi'
    """
    try:
        # -------------------------------------------------------
        # Clean the input city name
        # -------------------------------------------------------
        city_name = query.strip().lower()

        if not city_name:
            return "Please enter a city name to search hotels."

        # -------------------------------------------------------
        # Load cleaned hotel data
        # -------------------------------------------------------
        hotels = load_hotels()

        # -------------------------------------------------------
        # Filter hotels by city
        # -------------------------------------------------------
        matching_hotels = []

        for hotel in hotels:
            hotel_city = str(hotel.get("city", "")).lower()

            if hotel_city == city_name:
                matching_hotels.append(hotel)

        # -------------------------------------------------------
        # If no hotels match, return a message
        # -------------------------------------------------------
        if not matching_hotels:
            return f"No hotels found in {city_name.title()}."

        # -------------------------------------------------------
        # Sort hotels by:
        # 1. higher rating
        # 2. lower price per night
        # -------------------------------------------------------
        sorted_hotels = sorted(
            matching_hotels,
            key=lambda x: (-x.get("rating", 0), x.get("price_per_night", 999999))
        )

        # Take only top 3 hotels so output stays readable
        top_hotels = sorted_hotels[:3]

        # -------------------------------------------------------
        # Build a simple human-readable result
        # -------------------------------------------------------
        result = f"Top hotel recommendations in {city_name.title()}:\n\n"

        for index, hotel in enumerate(top_hotels, start=1):
            amenities = hotel.get("amenities", [])

            if amenities:
                amenities_text = ", ".join(amenities)
            else:
                amenities_text = "No amenities listed"

            result += f"{index}. {hotel.get('name')}\n"
            result += f"   Hotel ID        : {hotel.get('hotel_id')}\n"
            result += f"   City            : {hotel.get('city')}\n"
            result += f"   Rating          : {hotel.get('rating')} star\n"
            result += f"   Price per night : Rs.{hotel.get('price_per_night')}\n"
            result += f"   Amenities       : {amenities_text}\n\n"

        return result

    except Exception as e:
        return f"Error while searching hotels: {str(e)}"