import streamlit as st
import requests
from datetime import datetime, timedelta
from langchain.llms import OpenAI
from langchain.tools import WeatherAPI, FlightAPI, HotelAPI
import json

# Define the API keys and endpoints
weather_api_key = 'your_weather_api_key'
flight_api_key = 'your_flight_api_key'
hotel_api_key = 'your_hotel_api_key'

# Helper functions to fetch data from APIs
def get_weather(city, api_key):
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(weather_url)
    if response.status_code != 200:
        st.error(f"Error fetching weather data: {response.status_code}")
        return None
    try:
        data = response.json()
        return f"🌡️ Current Weather: {data['weather'][0]['description']}, {data['main']['temp']}°C"
    except json.JSONDecodeError as e:
        st.error(f"Error decoding weather JSON: {str(e)}")
        return None

def get_flights(origin, destination, date, api_key):
    flight_url = f"https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/{origin}/{destination}/{date}"
    headers = {'apikey': api_key}
    response = requests.get(flight_url, headers=headers)
    if response.status_code != 200:
        st.error(f"Failed to fetch flights: Status Code: {response.status_code}")
        return None
    try:
        data = response.json()
        if 'Quotes' in data:
            quote = data['Quotes'][0]
            return f"💺 Flight: {quote['MinPrice']} USD, Departing: {quote['OutboundLeg']['DepartureDate']}"
        else:
            return "No flight data available."
    except json.JSONDecodeError as e:
        st.error(f"Error decoding flight JSON: {str(e)}")
        return None

def get_hotels(city, api_key):
    hotel_url = f"https://api.hotels.com/v1/hotels?location={city}&apiKey={api_key}"
    response = requests.get(hotel_url)
    if response.status_code != 200:
        st.error(f"Failed to fetch hotel data: Status Code: {response.status_code}")
        return None
    try:
        data = response.json()
        if 'hotels' in data:
            hotel = data['hotels'][0]
            return f"🏨 Hotel: {hotel['name']}, Price: {hotel['price']['totalPrice']} USD"
        else:
            return "No hotel data available."
    except json.JSONDecodeError as e:
        st.error(f"Error decoding hotel JSON: {str(e)}")
        return None

# Main function to handle the trip planning
def plan_trip(city, days, month, weather_api_key, flight_api_key, hotel_api_key):
    today = datetime.today()
    month_index = ["January", "February", "March", "April", "May", "June", "July"].index(month) + 1
    trip_start = today.replace(month=month_index, day=min(today.day, 28))  # Avoid month-end errors
    trip_end = trip_start + timedelta(days=days - 1)

    # Display results
    st.subheader(f"🌍 Cultural & Historic Introduction of {city}")
    st.markdown(f"**{city}** is known for its rich cultural heritage and stunning historical landmarks. A visit to {city} provides an enriching experience with a mix of ancient traditions and modern architecture.")

    st.subheader("🗓️ Travel Dates")
    st.markdown(f"**{trip_start.strftime('%B %d, %Y')}** to **{trip_end.strftime('%B %d, %Y')}**")

    st.subheader("☁️ Current Weather")
    weather_now = get_weather(city, weather_api_key)
    if weather_now:
        st.markdown(weather_now)

    st.subheader("🌤️ Weather Forecast During Trip")
    # Weather forecast data can be added here
    st.markdown("Forecast details coming soon...")

    st.subheader("✈️ Flight Options")
    flight_info = get_flights("JFK", city, trip_start.strftime('%Y-%m-%d'), flight_api_key)
    if flight_info:
        st.markdown(flight_info)

    st.subheader("🏨 Hotel Options")
    hotel_info = get_hotels(city, hotel_api_key)
    if hotel_info:
        st.markdown(hotel_info)

# Streamlit UI enhancements
def main():
    st.title("🌏 Trip Planner App")
    st.sidebar.header("Trip Planning")

    # Inputs for the trip
    city = st.sidebar.text_input("Enter City Name", "Tokyo")
    days = st.sidebar.slider("Number of Days", 1, 7, 3)
    month = st.sidebar.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July"])

    if st.sidebar.button("Plan My Trip"):
        plan_trip(city, days, month, weather_api_key, flight_api_key, hotel_api_key)

# Add custom CSS to enhance UI/UX
st.markdown("""
    <style>
    .css-1aumxhk {
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .css-1vo0ouq {
        background-color: #4CAF50;
        color: white;
        font-size: 20px;
        border-radius: 10px;
        padding: 10px;
    }
    .css-1dp0lxu {
        color: #333333;
        font-size: 16px;
    }
    .stButton>button {
        background-color: #008CBA;
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #007B9A;
    }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

