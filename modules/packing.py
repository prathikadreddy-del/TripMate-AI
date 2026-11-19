
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model("google_genai:gemini-3.5-flash-lite")


@tool
def generate_packing_list(destination: str, days: int, weather: str, trip_type: str) -> str:
    """Generate a personalised packing checklist based on destination, trip duration, weather and trip type."""

    if days <= 0:
        return "Please provide a valid number of travel days."

    if days > 30:
        return "Please enter a trip duration of 30 days or less."

    prompt = f"""
    Create a personalised packing checklist for a trip to {destination}, India.

    Trip duration: {days} days
    Expected weather: {weather}
    Type of trip: {trip_type}

    Organise the checklist into these categories:
    1. Clothing
    2. Toiletries and personal care
    3. Travel essentials and documents
    4. Electronics
    5. Destination-specific items

    Requirements:
    - Suggest practical quantities based on the trip duration.
    - Consider the weather and activities.
    - Avoid unnecessary items.
    - Include useful travel essentials.
    - Present the checklist using clear bullet points.
    """

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as error:
        return f"Could not generate packing list: {error}"
