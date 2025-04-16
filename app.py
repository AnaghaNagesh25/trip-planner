import streamlit as st
from datetime import datetime, timedelta
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import WeatherAPI, FlightAPI, HotelAPI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import requests
import googlemaps

# Setup LLM (OpenAI or other engines like Llama3)
llm = OpenAI(temperature=0.7)

# API Keys for services
weather_api_key = "YOUR_OPENWEATHER_API_KEY"
flight_api_key = "YOUR_SKYSCANNER_API_KEY"
hotel_api_key = "YOUR_HOTEL_API_KEY"

# Tools for LangChain
tools = [
    WeatherAPI(api_key=weather_api_key),
    FlightAPI(api_key=flight_api_key),
    HotelAPI(api_key=hotel_api_key)
]

# LangChain Agent Setup
agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Function to plan a trip
def plan_trip(city, days, month):
    prompt = f"Plan a {days}-day trip to {city} in {month}. Provide cultural information, weather, travel dates, flight & hotel options."
    response = agent.run(city=city, days=days, month=month)
    return response

# Streamlit Interface
st.title("Trip Planner with LLM")

city = st.text_input("Enter the city you'd like to visit:")
days = st.number_input("Enter the number of days for your trip:", min_value=1, max_value=10, value=3)
month = st.selectbox("Select the month for your trip:", ["January", "February", "March", "April", "May", "June"])

if city and days and month:
    trip_details = plan_trip(city, days, month)

    st.subheader(f"🌍 Cultural & Historic Introduction of {city}")
    st.markdown(trip_details['city_summary'])

    # Calculate and Display Travel Dates
    today = datetime.now()
    trip_start = today.replace(month=month, day=min(today.day, 28))  # Avoid month-end errors
    trip_end = trip_start + timedelta(days=days - 1)
    st.subheader("🗓️ Travel Dates")
    st.markdown(f"**{trip_start.strftime('%B %d, %Y')}** to **{trip_end.strftime('%B %d, %Y')}**")

    st.subheader("☁️ Current Weather")
    st.markdown(f"Weather: {trip_details['weather_description']}, Temperature: {trip_details['temperature']}°C")

    st.subheader("🌤️ Weather Forecast During Trip")
    st.text(trip_details['forecast'])

    st.subheader("✈️ Flight Option")
    st.markdown(trip_details['flight_info'])

    st.subheader("🏨 Hotel Option")
    st.markdown(trip_details['hotel_info'])
