import os
import streamlit as st
from dotenv import load_dotenv
import requests
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load from .env (for local testing)
load_dotenv()

# Use Streamlit secrets for deployed environments
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", st.secrets.get("GOOGLE_API_KEY", ""))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", st.secrets.get("GEMINI_API_KEY", ""))
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", st.secrets.get("OPENWEATHER_API_KEY", ""))

# Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)

# Streamlit UI
st.set_page_config(page_title="✈️ AI Trip Planner", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧳 AI-Powered Trip Planner</h1>", unsafe_allow_html=True)

# User Inputs
city = st.text_input("🌍 Enter Destination City (e.g. Tokyo)", "Tokyo")
start_date = st.date_input("🗓️ Start Date", datetime(2025, 1, 16))
end_date = st.date_input("🗓️ End Date", datetime(2025, 1, 18))

# Fetch Weather
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['weather'][0]['description'].title()}, {data['main']['temp']}°C"
    return "❌ Unable to fetch weather data."

# Fetch Google Places
def get_places(city):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=top+attractions+in+{city}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        places = response.json().get("results", [])[:5]
        return [place["name"] for place in places]
    return []

# Generate Itinerary Suggestions
def generate_itinerary(city, start_date, end_date, places):
    prompt = f"""
    I am planning a trip to {city} from {start_date} to {end_date}.
    Can you suggest a 3-day itinerary including these attractions:
    {', '.join(places)}? Include morning, afternoon, and evening plans each day.
    """
    return llm.invoke([HumanMessage(content=prompt)]).content

# Display Results
if st.button("🚀 Plan My Trip"):
    st.markdown(f"### 🗓️ Travel Dates\n{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}")
    
    # Weather
    weather = get_weather(city)
    st.markdown(f"### ☁️ Current Weather\n{weather}")
    
    # Places
    places = get_places(city)
    if places:
        st.markdown("### 🌟 Top 5 Attractions")
        for i, place in enumerate(places, 1):
            st.write(f"{i}. {place}")
    else:
        st.markdown("### 🌟 Top 5 Attractions\n❌ No places data found.")

    # Itinerary
    if places:
        st.markdown("### 📋 Suggested Itinerary")
        itinerary = generate_itinerary(city, start_date, end_date, places)
        st.write(itinerary)
    else:
        st.warning("Unable to generate itinerary without attractions.")
