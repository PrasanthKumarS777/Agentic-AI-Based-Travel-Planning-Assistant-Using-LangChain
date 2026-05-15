# -------------------------------------------------------
# weather_tool.py
# This tool gets weather forecast using Open-Meteo.
#
# We first convert city name into latitude and longitude.
# Then we call the weather forecast API.
# Finally, we convert weather codes into simple labels
# so the output is easier to understand.
# -------------------------------------------------------

import requests

from langchain.tools import tool

# -------------------------------------------------------
# City coordinates for our project
# -------------------------------------------------------
CITY_COORDINATES = {
    "delhi": {"latitude": 28.6139, "longitude": 77.2090},
    "mumbai": {"latitude": 19.0760, "longitude": 72.8777},
    "kolkata": {"latitude": 22.5726, "longitude": 88.3639},
    "chennai": {"latitude": 13.0827, "longitude": 80.2707},
    "bengaluru": {"latitude": 12.9716, "longitude": 77.5946},
    "bangalore": {"latitude": 12.9716, "longitude": 77.5946},
    "hyderabad": {"latitude": 17.3850, "longitude": 78.4867},
    "goa": {"latitude": 15.2993, "longitude": 74.1240},
    "jaipur": {"latitude": 26.9124, "longitude": 75.7873},
}


def get_coordinates(city_name):
    """
    Get latitude and longitude for a city.
    """
    key = city_name.strip().lower()
    return CITY_COORDINATES.get(key)


def weather_code_to_text(code):
    """
    Convert Open-Meteo weather codes into easy words.
    """
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }

    return weather_map.get(code, f"Unknown weather code ({code})")


@tool
def weather_tool(query: str) -> str:
    """
    Get a simple weather forecast for a city.
    Example input: 'Delhi'
    """
    try:
        # -------------------------------------------------------
        # Clean the city name
        # -------------------------------------------------------
        city_name = query.strip()

        if not city_name:
            return "Please enter a city name for weather lookup."

        # -------------------------------------------------------
        # Get coordinates for the city
        # -------------------------------------------------------
        coordinates = get_coordinates(city_name)

        if not coordinates:
            return f"Coordinates not found for {city_name}."

        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]

        # -------------------------------------------------------
        # Build the Open-Meteo forecast URL
        # -------------------------------------------------------
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}"
            f"&longitude={longitude}"
            "&daily=temperature_2m_max,temperature_2m_min,weather_code"
            "&timezone=auto"
        )

        # -------------------------------------------------------
        # Call the weather API
        # -------------------------------------------------------
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # -------------------------------------------------------
        # Read daily forecast values
        # -------------------------------------------------------
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        weather_codes = daily.get("weather_code", [])

        if not dates:
            return f"No weather data found for {city_name.title()}."

        # -------------------------------------------------------
        # Build readable forecast
        # -------------------------------------------------------
        result = f"Weather forecast for {city_name.title()}:\n\n"

        for i in range(min(3, len(dates))):
            code = weather_codes[i]
            weather_text = weather_code_to_text(code)

            result += f"Day {i + 1}:\n"
            result += f"  Date        : {dates[i]}\n"
            result += f"  Max Temp    : {max_temps[i]}°C\n"
            result += f"  Min Temp    : {min_temps[i]}°C\n"
            result += f"  Weather     : {weather_text}\n\n"

        return result

    except requests.exceptions.RequestException as e:
        return f"Weather API request failed: {str(e)}"
    except Exception as e:
        return f"Error while fetching weather: {str(e)}"