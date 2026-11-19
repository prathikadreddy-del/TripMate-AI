

import os
import ast
import json
import operator
import urllib.parse
import urllib.request

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from modules.destination import recommend_destinations
from modules.itinerary import generate_itinerary
from modules.budget import estimate_budget
from modules.packing import generate_packing_list

# Load API key
load_dotenv()

# Connect to Gemini
MODEL = "google_genai:gemini-3.5-flash-lite"
llm = init_chat_model(MODEL)


# --------------------------------
# 1. CALCULATOR TOOL
# --------------------------------

@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expressions.
    Use this tool whenever the user asks for calculations.
    """

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value

            if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
                left = evaluate(node.left)
                right = evaluate(node.right)
                return allowed_operators[type(node.op)](left, right)

            if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
                return allowed_operators[type(node.op)](
                    evaluate(node.operand)
                )

            raise ValueError("Unsupported expression")

        return str(evaluate(tree))

    except Exception as error:
        return f"Calculation error: {error}"


# --------------------------------
# 2. WEATHER TOOL
# --------------------------------

def get_json(url):
    """Fetch JSON data from a URL."""
    with urllib.request.urlopen(url, timeout=15) as response:
        return json.load(response)


@tool
def get_weather(city: str) -> str:
    """Get current weather information for a city.
    Use this when the user asks about weather at a destination.
    """

    try:
        city_query = urllib.parse.quote(city)

        # Find the city coordinates
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={city_query}&count=1"
        )

        places = get_json(geo_url).get("results")

        if not places:
            return f"Sorry, I could not find the city {city}."

        place = places[0]

        latitude = place["latitude"]
        longitude = place["longitude"]

        # Get current weather
        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}"
            "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
        )

        weather = get_json(weather_url)["current"]

        return (
            f"Weather in {place['name']}, "
            f"{place.get('country', '')}: "
            f"Temperature: {weather['temperature_2m']}°C, "
            f"Humidity: {weather['relative_humidity_2m']}%, "
            f"Wind speed: {weather['wind_speed_10m']} km/h."
        )

    except Exception as error:
        return f"Could not retrieve weather information: {error}"


# --------------------------------
# 3. REGISTER TOOLS
# --------------------------------

tools = [calculate, get_weather,recommend_destinations,generate_itinerary,estimate_budget,generate_packing_list]
llm_with_tools = llm.bind_tools(tools)


# --------------------------------
# 4. AI AGENT
# --------------------------------

SYSTEM_MESSAGE = SystemMessage(
    content=(
        "You are TripMate AI, a friendly Indian travel planning assistant. "
        "Use calculate for mathematical calculations. "
        "Use get_weather for current weather information. "
        "Use recommend_destinations for destination suggestions. "
        "Use generate_itinerary for day-wise travel plans. "
        "IMPORTANT: When a tool returns an itinerary, display the COMPLETE "
        "itinerary exactly as provided. Do not shorten it or replace it "
        "with a summary. Preserve every day's activities. "
        "Never invent live weather information. "
        "Clearly explain that destination budget estimates are approximate."
        "Use estimate_budget whenever users ask for a travel expense breakdown or total trip cost."
        "Use estimate_budget whenever users ask for a travel expense breakdown or total trip cost. "
        "IMPORTANT: When estimate_budget returns a result, display the COMPLETE result exactly as provided. Do not summarise or omit the expense breakdown or total. "
        "Use generate_packing_list whenever users ask for a travel packing checklist."
    )
)


def agent(state: MessagesState):
    response = llm_with_tools.invoke(
        [SYSTEM_MESSAGE] + state["messages"]
    )
    return {"messages": [response]}


# --------------------------------
# 5. BUILD LANGGRAPH
# --------------------------------

builder = StateGraph(MessagesState)

builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()


# --------------------------------
# 6. EXTRACT CLEAN TEXT
# --------------------------------

def get_text(content):

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))

            elif isinstance(item, str):
                parts.append(item)

        return "\n".join(parts)

    return str(content)


# --------------------------------
# 7. RUN TRIPMATE AI
# --------------------------------

if __name__ == "__main__":

    print("\n================================")
    print("          TRIPMATE AI")
    print("================================")
    print("Your AI travel assistant is ready!")
    print("Type 'quit' to exit.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() == "quit":
            print("\nThank you for using TripMate AI!")
            break

        if not question:
            continue

        try:
            result = graph.invoke({
                "messages": [("user", question)]
            })

            # Display tools called by Gemini
            for msg in result["messages"]:
                for call in getattr(msg, "tool_calls", []):
                    print(f"\n[Tool called: {call['name']}]")

            # Display final response
            final_message = result["messages"][-1]
            answer = get_text(final_message.content)

            print("\nTripMate AI:", answer)
            print()

        except Exception as error:
            print("\nSomething went wrong:", error)
            print("Please try again.\n")
