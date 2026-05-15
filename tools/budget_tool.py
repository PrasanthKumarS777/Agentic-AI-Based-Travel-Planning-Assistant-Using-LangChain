# -------------------------------------------------------
# budget_tool.py
# This tool helps estimate trip budget.
#
# It combines:
# - flight cost
# - hotel cost
# - daily local expenses
#
# The goal is to give a simple trip budget summary.
# -------------------------------------------------------

from langchain.tools import tool


@tool
def budget_tool(query: str) -> str:
    """
    Estimate budget from a simple comma-separated input.

    Expected input format:
    flight_price, hotel_price_per_night, number_of_nights, daily_local_expense

    Example:
    3779, 3650, 3, 1000
    """
    try:
        # -------------------------------------------------------
        # Split the input by commas
        # -------------------------------------------------------
        parts = query.split(",")

        if len(parts) != 4:
            return "Please use the format: flight_price, hotel_price_per_night, number_of_nights, daily_local_expense"

        # -------------------------------------------------------
        # Convert values to numbers
        # -------------------------------------------------------
        flight_price = float(parts[0].strip())
        hotel_price_per_night = float(parts[1].strip())
        number_of_nights = int(parts[2].strip())
        daily_local_expense = float(parts[3].strip())

        # -------------------------------------------------------
        # Calculate total hotel cost
        # -------------------------------------------------------
        hotel_total = hotel_price_per_night * number_of_nights

        # -------------------------------------------------------
        # Calculate local travel and food cost
        # -------------------------------------------------------
        local_total = daily_local_expense * number_of_nights

        # -------------------------------------------------------
        # Calculate final budget
        # -------------------------------------------------------
        total_cost = flight_price + hotel_total + local_total

        # -------------------------------------------------------
        # Build a readable result
        # -------------------------------------------------------
        result = "Estimated Trip Budget:\n\n"
        result += f"Flight Cost        : Rs.{flight_price:.2f}\n"
        result += f"Hotel Cost         : Rs.{hotel_total:.2f} ({number_of_nights} nights)\n"
        result += f"Local Expenses     : Rs.{local_total:.2f}\n"
        result += f"Daily Local Expense : Rs.{daily_local_expense:.2f}\n\n"
        result += f"Total Estimated Cost: Rs.{total_cost:.2f}"

        return result

    except ValueError:
        return "Invalid input. Please enter only numeric values separated by commas."
    except Exception as e:
        return f"Error while calculating budget: {str(e)}"