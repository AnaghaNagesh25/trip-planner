import streamlit as st
import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain.llms import GooglePalm

# Load environment variables
load_dotenv()

# Get API keys
OPENWEATHER_API_KEY = os.getenv("714ea86f8689ebafb30f12dd9c09cbaa")
GOOGLE_API_KEY = os.getenv("AIzaSyDqztuqGS6N8ciIDlfWxW2CcuUQbFaXGfM")
GEMINI_API_KEY = os.getenv("AIzaSyDqztuqGS6N8ciIDlfWxW2CcuUQbFaXGfM")

# Initialize Gemini LLM
llm = GooglePalm(google_api_key=GEMINI_API_KEY)

# Streamlit UI configuration
st.set_page_config(page_title="AI Trip Planner", layout="wide")
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to right, #e0f7fa, #fff3e0);
        padding: 2rem;
    }
    .block-container {
        max-width: 900px;
        margin: auto;
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌍 AI-Powered Trip Planner")
st.markdown("Plan your next adventure with the power of AI. Get suggestions for weather, attractions, flights, and hotels!")

# User Inputs
city = st.text_input("Enter city name", "Tokyo")
days = st.slider("Select number of days", 1, 7, 3)
month = st.selectbox("Select travel month", ["January", "February", "March", "April", "May", "June", "July"])

# Button to generate plan
if st.button("Generate Trip Plan"):

    today = datetime.today()
    month_index = ["January", "February", "March", "April", "May", "June", "July"].index(month) + 1
    trip_start = today.replace(month=month_index, day=min(today.day, 28))
    trip_end = trip_start + timedelta(days=days - 1)

    # LLM for cultural/historic intro
    intro_prompt = f"Provide a 1-paragraph cultural and historical introduction for {city}."
    trip_summary = llm.invoke(intro_prompt)

    # Weather API call
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    weather_data = requests.get(weather_url).json()

    current_weather = "Error: Unable to fetch weather data."
    if weather_data.get("main"):
        temp = weather_data["main"]["temp"]
        desc = weather_data["weather"][0]["description"]
        current_weather = f"**{temp}°C**, {desc.capitalize()}"

    # Google Places API for attractions
    places_url = (
        f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=tourist+attractions+in+{city}&key={GOOGLE_API_KEY}"
    )
    places_data = requests.get(places_url).json()
    places_list = []
    if places_data.get("results"):
        for place in places_data["results"][:5]:
            places_list.append(f"**{place['name']}** - {place.get('formatted_address', 'No address available')}")

    # Display Results
    st.subheader("🌍 Cultural & Historic Introduction")
    st.markdown(trip_summary)

    st.subheader("🗓️ Travel Dates")
    st.markdown(f"**{trip_start.strftime('%B %d, %Y')}** to **{trip_end.strftime('%B %d, %Y')}**")

    st.subheader("☁️ Current Weather")
    st.markdown(current_weather)

    st.subheader("🌤️ Google Places (Top 5 Popular Attractions)")
    if places_list:
        for place in places_list:
            st.markdown(f"- {place}")
    else:
        st.markdown("No places data found.")

    st.subheader("✈️ Flight Options")
    st.markdown("Flights are available from various international airports to this city.\nPlease check [Google Flights](https://www.google.com/travel/flights) for the latest prices and availability.")

    st.subheader("🏨 Hotel Options")
    st.markdown("We recommend checking out [Google Hotels](https://www.google.com/travel/hotels) or [Booking.com](https://www.booking.com) for the best deals.")


