
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model

# Load the API key before creating the Gemini connection
load_dotenv()

# Connect to Gemini
llm = init_chat_model("google_genai:gemini-3.5-flash-lite")


@tool
def generate_itinerary(
    destination: str,
    days: int,
    interests: str,
    travellers: int
) -> str:
    """
    Generate a day-wise travel itinerary for an Indian destination.
    """

    if days <= 0 or travellers <= 0:
        return "Days and number of travellers must be positive."

    if days > 14:
        return "Please request an itinerary for 14 days or fewer."

    prompt = f"""
    Create a practical {days}-day travel itinerary for {destination}, India.

    Number of travellers: {travellers}
    Interests: {interests}

    Requirements:
    1. Organise the plan day by day.
    2. Suggest morning, afternoon and evening activities.
    3. Include popular attractions and experiences.
    4. Keep the schedule realistic.
    5. Suggest local food experiences.
    6. Avoid repeating activities.
    7. Do not invent opening hours or ticket prices.
    8. Mention that travellers should verify timings before visiting.

    Format the answer clearly with headings for each day.
    """

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as error:
        return f"Could not generate itinerary: {error}"
