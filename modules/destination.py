
from langchain_core.tools import tool


# Indian destination information
DESTINATIONS = [
    {
        "name": "Goa",
        "state": "Goa",
        "interests": ["beach", "adventure", "nightlife", "relaxation"],
        "daily_budget": 2500,
        "description": "Beaches, water sports, nightlife and coastal views."
    },
    {
        "name": "Coorg",
        "state": "Karnataka",
        "interests": ["nature", "relaxation", "adventure"],
        "daily_budget": 2200,
        "description": "Coffee estates, waterfalls, hills and greenery."
    },
    {
        "name": "Manali",
        "state": "Himachal Pradesh",
        "interests": ["mountains", "adventure", "nature"],
        "daily_budget": 3000,
        "description": "Snowy mountains, trekking and scenic valleys."
    },
    {
        "name": "Jaipur",
        "state": "Rajasthan",
        "interests": ["culture", "history", "sightseeing"],
        "daily_budget": 2000,
        "description": "Forts, palaces, markets and Rajasthani culture."
    },
    {
        "name": "Munnar",
        "state": "Kerala",
        "interests": ["nature", "mountains", "relaxation"],
        "daily_budget": 2500,
        "description": "Tea gardens, misty hills and beautiful viewpoints."
    },
    {
        "name": "Ooty",
        "state": "Tamil Nadu",
        "interests": ["nature", "mountains", "relaxation"],
        "daily_budget": 2300,
        "description": "Hill stations, gardens and scenic train journeys."
    },
    {
        "name": "Rishikesh",
        "state": "Uttarakhand",
        "interests": ["adventure", "nature", "spirituality"],
        "daily_budget": 2000,
        "description": "River rafting, yoga, temples and mountain views."
    },
    {
        "name": "Alleppey",
        "state": "Kerala",
        "interests": ["nature", "relaxation", "culture"],
        "daily_budget": 2800,
        "description": "Backwaters, houseboats and peaceful landscapes."
    }
]


@tool
def recommend_destinations(
    budget: int,
    days: int,
    travellers: int,
    interest: str
) -> str:
    """
    Recommend Indian travel destinations based on budget,
    number of days, number of travellers and travel interests.

    Budget is the total budget in INR.
    """

    if budget <= 0 or days <= 0 or travellers <= 0:
        return "Please provide positive values for budget, days and travellers."

    # Approximate daily budget per person
    daily_budget = budget / (days * travellers)

    preferences = [
        item.strip().lower()
        for item in interest.split(",")
    ]

    matches = []

    for place in DESTINATIONS:

        interest_match = any(
            preference in place["interests"]
            for preference in preferences
        )

        if interest_match and place["daily_budget"] <= daily_budget:
            matches.append(place)

    if not matches:
        return (
            "No close matches found within the approximate budget. "
            "Try increasing your budget or changing your travel interests."
        )

    results = []

    for place in matches[:5]:
        results.append(
            f"Destination: {place['name']}, {place['state']}\n"
            f"Description: {place['description']}\n"
            f"Approximate daily budget per person: "
            f"₹{place['daily_budget']}\n"
        )

    return (
        "Here are some Indian destinations matching your preferences.\n"
        "Budget figures are rough planning estimates, not live prices, "
        "and exclude travel to and from the destination.\n\n"
        + "\n".join(results)
    )
