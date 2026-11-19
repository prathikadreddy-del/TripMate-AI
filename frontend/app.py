
import streamlit as st
import sys
from pathlib import Path
import folium
from streamlit_folium import st_folium

# Add the main project folder to Python's import path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agent import graph, get_text
from modules.budget import estimate_budget


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="TripMate AI",
    page_icon="✈️",
    layout="wide"
)


# --------------------------------------------------
# WEBSITE STYLING
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #F8F6EF;
    color: #263C38;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

h1, h2, h3 {
    color: #174C43 !important;
    font-family: 'Trebuchet MS', sans-serif;
}

p, label {
    color: #354D46;
}

.stButton > button {
    background-color: #267568;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.7rem 1.2rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #174C43;
    color: white;
}

.stTextInput input,
.stNumberInput input {
    background-color: white;
    border-radius: 10px;
}

.stAlert {
    border-radius: 12px;
}

hr {
    border-color: #D7E3D9;
}

.destination-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #E1EAE2;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(30, 70, 55, 0.07);
}

.destination-card img {
    width: 100%;
    height: 165px;
    object-fit: cover;
    display: block;
}

.destination-info {
    padding: 15px;
}

.destination-info h3 {
    margin: 0 0 6px 0;
    font-size: 21px;
}

.destination-info p {
    color: #63766D;
    font-size: 14px;
}

.destination-tag {
    display: inline-block;
    background: #E8F0E9;
    color: #267568;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
}

.hero-banner {
    background:
        linear-gradient(90deg, rgba(15,55,48,0.82),
        rgba(15,55,48,0.25)),
        url("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1600");
    background-size: cover;
    background-position: center;
    padding: 65px 45px;
    border-radius: 22px;
    margin: 25px 0;
    color: white;
}

.hero-banner h1 {
    color: white !important;
    font-size: 42px;
}

.hero-banner p {
    color: white !important;
    font-size: 18px;
    max-width: 600px;
}

.hero-tag {
    background: rgba(255,255,255,0.2);
    padding: 8px 15px;
    border-radius: 20px;
    display: inline-block;
    color: white;
    margin-bottom: 15px;
}

/* Destination cards */
.destination-card {
    height: 340px;
    display: flex;
    flex-direction: column;
    background: #FFFFFF;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #E1EAE2;
}

/* Equal image sizes */

.destination-card img {
    display: block !important;
    width: 100% !important;
    height: 160px !important;
    min-height: 160px !important;
    max-height: 160px !important;
    object-fit: cover !important;
    border-radius: 12px 12px 0 0;
}


/* Card content */
.destination-info {
    padding: 15px;
    flex: 1;
}
</style>

""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("✈️ TripMate AI")

st.subheader("Your AI-powered travel planning assistant")

st.write(
    "Plan your next adventure with personalised destinations, "
    "itineraries, budgets and packing lists."
)


# --------------------------------------------------
# HERO BANNER
# --------------------------------------------------

st.html("""
<div class="hero-banner">
    <div class="hero-tag">
        ✈️ YOUR NEXT ADVENTURE STARTS HERE
    </div>

    <h1>Explore More.<br>Worry Less.</h1>

    <p>
        Discover beautiful destinations, plan unforgettable
        journeys and make every trip count with TripMate AI.
    </p>
</div>
""")


# --------------------------------------------------
# FEATURED DESTINATIONS
# --------------------------------------------------

st.markdown("## 🌿 Explore Popular Destinations")

st.write("Find the perfect place for your next adventure.")

destinations = [
    {
        "name": "Coorg",
        "description": "Coffee estates, waterfalls and misty hills.",
        "tag": "🌿 Nature",
        "image": "https://images.unsplash.com/photo-1511497584788-876760111969?w=600"
    },
    {
        "name": "Goa",
        "description": "Golden beaches and beautiful sunsets.",
        "tag": "🏖️ Beach",
        "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600"
    },
    {
        "name": "Manali",
        "description": "Snowy mountains and thrilling adventures.",
        "tag": "🏔️ Adventure",
        "image": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600"
    },
    {
        "name": "Jaipur",
        "description": "Royal palaces and colourful culture.",
        "tag": "🏰 Heritage",
        "image": "https://images.unsplash.com/photo-1599661046827-dacff0c0f09a?w=600"
    }
]

dest_cols = st.columns(4)

for col, place in zip(dest_cols, destinations):
    with col:
        st.image(place["image"], use_container_width=True)

        st.subheader(place["name"])
        st.write(place["description"])

        st.caption(place["tag"])

        if st.button(
            f"Explore {place['name']}",
            key=f"explore_{place['name']}",
            use_container_width=True
        ):
            st.session_state["selected_destination"] = place["name"]
            st.rerun()


st.divider()


# --------------------------------------------------
# DETAILED BUDGET INPUTS
# --------------------------------------------------

with st.expander("💰 Add detailed budget information"):

    accommodation = st.number_input(
        "Accommodation per night (₹)",
        min_value=0,
        value=2000,
        step=500
    )

    food = st.number_input(
        "Food per person per day (₹)",
        min_value=0,
        value=500,
        step=100
    )

    transport = st.number_input(
        "Local transport per day (₹)",
        min_value=0,
        value=800,
        step=100
    )

    activities = st.number_input(
        "Activities per person (₹)",
        min_value=0,
        value=1000,
        step=100
    )

    miscellaneous = st.number_input(
        "Miscellaneous expenses (₹)",
        min_value=0,
        value=500,
        step=100
    )


# --------------------------------------------------
# TRIP PLANNER FORM
# --------------------------------------------------

st.header("🌍 Plan Your Trip")

col1, col2 = st.columns(2)

with col1:

          
    if "selected_destination" not in st.session_state:
       st.session_state.selected_destination = ""
  
    destination = st.text_input(
      "Where would you like to go?",
       placeholder="e.g. Coorg",
       key="selected_destination"
    )


    days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=30,
        value=3
    )

    travellers = st.number_input(
        "Number of travellers",
        min_value=1,
        max_value=20,
        value=2
    )

with col2:

    budget = st.number_input(
        "Total budget (₹)",
        min_value=1000,
        value=15000,
        step=1000
    )

    interests = st.multiselect(
        "What are you interested in?",
        [
            "Nature",
            "Adventure",
            "Beaches",
            "History",
            "Food",
            "Shopping",
            "Relaxation"
        ],
        default=["Nature", "Adventure"]
    )

    weather = st.selectbox(
        "Expected weather",
        ["Cool", "Sunny", "Rainy", "Cold", "Not sure"]
    )


st.divider()


# --------------------------------------------------
# SESSION STATE
# Keep results visible after Streamlit reruns
# --------------------------------------------------

if "trip_data" not in st.session_state:
    st.session_state.trip_data = None


# --------------------------------------------------
# PLAN MY TRIP BUTTON
# --------------------------------------------------

if st.button("✨ Plan My Trip", use_container_width=True):

    if not destination.strip():
        st.warning("Please enter a destination.")

    elif not interests:
        st.warning("Please select at least one interest.")

    else:

        prompt = f"""
        Plan a trip to {destination}, India.

        Number of days: {days}
        Number of travellers: {travellers}
        Total available budget: ₹{budget}
        Interests: {", ".join(interests)}
        Expected weather: {weather}

        Please provide:

        1. A detailed day-wise itinerary with morning,
           afternoon and evening activities.

        2. A personalised packing checklist.

        3. Current weather information using the weather tool.
           Do not invent live weather information.

        Do not calculate or display a separate budget.
        The website has its own detailed budget calculator.

        Keep all sections organised and preserve the complete
        itinerary and packing checklist.
        """

        with st.spinner("✈️ TripMate AI is planning your trip..."):

            try:

                result = graph.invoke({
                    "messages": [("user", prompt)]
                })

                answer = get_text(
                    result["messages"][-1].content
                )

                budget_result = estimate_budget.invoke({
                    "destination": destination,
                    "days": int(days),
                    "travellers": int(travellers),
                    "accommodation_per_night": accommodation,
                    "food_per_person_per_day": food,
                    "transport_per_day": transport,
                    "activities_per_person": activities,
                    "miscellaneous": miscellaneous
                })

                st.session_state.trip_data = {
                    "answer": answer,
                    "budget_result": budget_result,
                    "destination": destination,
                    "budget": budget
                }

            except Exception as error:
                st.error(f"Something went wrong: {error}")


# --------------------------------------------------
# DISPLAY GENERATED RESULTS
# --------------------------------------------------

if st.session_state.trip_data is not None:

    data = st.session_state.trip_data

    st.success("Your travel plan is ready!")

    st.markdown("## 🌍 Your Travel Plan")

    st.markdown(data["answer"])

    st.divider()


    # --------------------------------------------------
    # DESTINATION MAP
    # --------------------------------------------------

    st.subheader("🗺️ Explore Your Destination")

    destination_coordinates = {
        "goa": [15.2993, 74.1240],
        "coorg": [12.4244, 75.7382],
        "manali": [32.2396, 77.1887],
        "jaipur": [26.9124, 75.7873],
        "munnar": [10.0889, 77.0595],
        "ooty": [11.4102, 76.6950],
        "rishikesh": [30.0869, 78.2676],
        "alleppey": [9.4981, 76.3388]
    }

    place = data["destination"].strip().lower()

    if place in destination_coordinates:

        location = destination_coordinates[place]

        travel_map = folium.Map(
            location=location,
            zoom_start=12
        )

        folium.Marker(
            location=location,
            popup=data["destination"].title(),
            tooltip=data["destination"].title(),
            icon=folium.Icon(
                color="green",
                icon="info-sign"
            )
        ).add_to(travel_map)

        st_folium(
            travel_map,
            width=None,
            height=450,
            use_container_width=True
        )

    else:
        st.info(
            "Map is not available for this destination yet."
        )


    # --------------------------------------------------
    # ONE DETAILED BUDGET SECTION
    # --------------------------------------------------

    st.divider()

    st.subheader("💰 Your Detailed Budget")

    st.markdown(data["budget_result"])

    st.caption(
        "Budget figures are estimates based on the expenses "
        "you entered. Travel to and from the destination is "
        "not included unless entered separately."
    )
