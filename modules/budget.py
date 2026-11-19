
from langchain_core.tools import tool


@tool
def estimate_budget(
    destination: str,
    days: int,
    travellers: int,
    accommodation_per_night: float,
    food_per_person_per_day: float,
    transport_per_day: float,
    activities_per_person: float,
    miscellaneous: float
) -> str:
    """
    Estimate the total travel budget in Indian Rupees.

    Calculate accommodation, food, local transport, activities,
    miscellaneous expenses, total cost and cost per traveller.

    All amounts are in INR.
    """

    if days <= 0 or travellers <= 0:
        return "Days and number of travellers must be positive."

    amounts = [
        accommodation_per_night,
        food_per_person_per_day,
        transport_per_day,
        activities_per_person,
        miscellaneous
    ]

    if any(amount < 0 for amount in amounts):
        return "Expenses cannot be negative."

    # Calculate individual expenses
    accommodation = accommodation_per_night * days

    food = food_per_person_per_day * days * travellers

    transport = transport_per_day * days

    activities = activities_per_person * travellers

    # Add all expenses
    total = (
        accommodation
        + food
        + transport
        + activities
        + miscellaneous
    )

    per_person = total / travellers

    return (
        f"Estimated Travel Budget for {destination}\n\n"
        f"Number of days: {days}\n"
        f"Number of travellers: {travellers}\n\n"
        f"Accommodation: ₹{accommodation:,.2f}\n"
        f"Food: ₹{food:,.2f}\n"
        f"Local transport: ₹{transport:,.2f}\n"
        f"Activities and sightseeing: ₹{activities:,.2f}\n"
        f"Miscellaneous: ₹{miscellaneous:,.2f}\n\n"
        f"TOTAL ESTIMATED COST: ₹{total:,.2f}\n"
        f"COST PER PERSON: ₹{per_person:,.2f}\n\n"
        "Note: These are estimates based on the supplied expenses. "
        "Travel to and from the destination is not included unless "
        "accounted for separately."
    )
