import os
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Load API keys
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# LangChain LLM Setup
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GEMINI_API_KEY)

# Streamlit fancy UI
st.set_page_config(page_title="AI Trip Planner", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .title { font-size:36px; font-weight:bold; color:#2c3e50; }
    .section { background-color: white; padding:20px; border-radius:15px; margin-top:20px; box-shadow: 0 0 10px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>✈️ AI Trip Planner</div>", unsafe_allow_html=True)

# Input
city = st.text_input("Enter city (e.g., Tokyo)", value="Tokyo")
days = st.slider("Trip duration (in days)", min_value=1, max_value=10, value=3)
month = st.selectbox("Select month", ["April", "May", "June", "July", "August"])
submit = st.button("Plan My Trip!")

# Helper Functions
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    r = requests.get(url)
    data = r.json()
    if "main" in data:
        return f"{data['weather'][0]['description'].capitalize()}, {data['main']['temp']}°C"
    return "Weather info unavailable"

def get_places(city):
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=tourist+attractions+in+{city}&key={GOOGLE_API_KEY}"
    r = requests.get(url)
    data = r.json()
    places = [place["name"] for place in data.get("results", [])[:5]]
    return places if places else ["No data found"]

# Main Logic
if submit:
    start_date = datetime(2025, list(["January", "February", "March", "April", "May", "June", "July", "August"]).index(month) + 1, 16)
    end_date = start_date + timedelta(days=days - 1)

    with st.spinner("Talking to Gemini..."):
        city_info = llm([HumanMessage(content=f"Tell me about the cultural and historical significance of {city}.")]).content

    weather = get_weather(city)
    places = get_places(city)

    # Display Results
    st.markdown(f"<div class='section'><h3>🗓️ Travel Dates</h3>{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section'><h3>🏙️ About {city}</h3>{city_info}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section'><h3>☁️ Current Weather</h3>{weather}</div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section'><h3>🌟 Top Attractions in {city}</h3><ul>" + "".join([f"<li>{p}</li>" for p in places]) + "</ul></div>", unsafe_allow_html=True)

    st.markdown(f"<div class='section'><h3>✈️ Flight Options</h3>Flights are available from major cities. Check Google Flights or Skyscanner for best deals.</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section'><h3>🏨 Hotel Options</h3>Check Google Hotels, Booking.com, or Airbnb for accommodation near top attractions.</div>", unsafe_allow_html=True)

