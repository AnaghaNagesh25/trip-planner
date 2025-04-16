import streamlit as st
import requests
import google.generativeai as genai
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load API keys
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("714ea86f8689ebafb30f12dd9c09cbaa")
GOOGLE_API_KEY = os.getenv("AIzaSyDqztuqGS6N8ciIDlfWxW2CcuUQbFaXGfM")
GEMINI_API_KEY = os.getenv("AIzaSyDqztuqGS6N8ciIDlfWxW2CcuUQbFaXGfM")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Styling
st.set_page_config(page_title="Trip Planner", layout="wide")
st.markdown("<h1 style='text-align: center; color: #00A6ED;'>🧳 AI Trip Planner</h1>", unsafe_allow_html=True)
st.markdown("---")

# Function: Get Weather
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        desc = data['weather'][0]['description'].title()
        temp = data['main']['temp']
        return f"{desc}, {temp}°C"
    return None

# Function: Get Places
def get_places(city):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=tourist+attractions+in+{city}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results", [])[:5]
        return [place["name"] for place in results]
    return None

# Function: Ask Gemini
def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "❌ Gemini LLM Error."

# UI: Sidebar Inputs
with st.sidebar:
    st.markdown("## 📍 Trip Settings")
    city = st.text_input("Destination City", "Tokyo")
    days = st.slider("Number of Days", 1, 7, 3)
    start_date = st.date_input("Trip Start Date", datetime.today())

# Processing
if st.button("Plan My Trip"):
    end_date = start_date + timedelta(days=days - 1)
    trip_range = f"{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
    st.markdown(f"### 🗓️ Travel Dates\n{trip_range}")

    # Weather
    weather = get_weather(city)
    if weather:
        st.markdown(f"### ☁️ Current Weather\n{weather}")
    else:
        st.markdown("### ☁️ Current Weather\n❌ Unable to fetch weather data.")

    # Places
    places = get_places(city)
    if places:
        st.markdown("### 🌟 Top 5 Attractions")
        for i, place in enumerate(places, 1):
            st.markdown(f"{i}. {place}")
    else:
        st.markdown("### 🌟 Top 5 Attractions\n❌ No places data found.")

    # Gemini: City Summary & Itinerary
    with st.spinner("🧠 Generating itinerary using Gemini..."):
        prompt = (
            f"Plan a {days}-day trip to {city}. Include:\n"
            f"1 paragraph on its cultural and historical background,\n"
            f"weather forecast for the trip between {trip_range},\n"
            f"a suggested itinerary with must-visit attractions,\n"
            f"hotel and flight suggestions.\n"
            f"If possible, include things to eat and tips."
        )
        response = ask_gemini(prompt)
        st.markdown("### 🧠 Trip Summary & Itinerary")
        st.markdown(response)

    # Placeholder Flight/Hotel Info
    st.markdown("### ✈️ Flight Options")
    st.markdown("Flights are available from various international airports to this city. Please check Google Flights or Skyscanner.")

    st.markdown("### 🏨 Hotel Options")
    st.markdown("Several hotels are available. Please check Booking.com, Airbnb, or Trivago for best deals.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; font-size: 13px;'>Built with ❤️ using Gemini + Streamlit</p>", unsafe_allow_html=True)

