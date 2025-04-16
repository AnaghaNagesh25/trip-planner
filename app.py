import streamlit as st
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("714ea86f8689ebafb30f12dd9c09cbaa")
GOOGLE_API_KEY = os.getenv("AIzaSyDqztuqGS6N8ciIDlfWxW2CcuUQbFaXGfM")

# Function to get weather data from OpenWeather API
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        weather_now = f"**Current Weather:** {data['weather'][0]['description'].capitalize()}, {data['main']['temp']}°C"
        weather_forecast = f"**Weather Forecast:** {data['weather'][0]['main']} with a temperature range from {data['main']['temp_min']}°C to {data['main']['temp_max']}°C."
        return weather_now, weather_forecast
    else:
        return None, "Error: Unable to fetch weather data."

# Function to get Google Places data (like popular attractions)
def get_google_places(city, api_key):
    # Example: Fetching places near the city center (latitude, longitude)
    # Using Tokyo coordinates as placeholder, change it based on city if needed
    coordinates = {
        "Tokyo": (35.6762, 139.6503),
        "New York": (40.7128, -74.0060),
        "Paris": (48.8566, 2.3522)
    }
    
    # Defaulting to Tokyo for testing if city is not found
    lat, lon = coordinates.get(city, coordinates["Tokyo"])

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&key={api_key}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            places = [place['name'] for place in data['results'][:5]]  # Get top 5 places
            return places
        else:
            return []
    else:
        return []

# Main function to display trip info
def plan_trip(city, days, month, weather_api_key, google_api_key):
    today = datetime.today()
    month_index = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(month) + 1
    trip_start = today.replace(month=month_index, day=min(today.day, 28))  # Avoid month-end errors
    trip_end = trip_start + timedelta(days=days - 1)

    # Fetch weather data
    weather_now, weather_forecast = get_weather(city, weather_api_key)

    # Fetch Google Places data
    places = get_google_places(city, google_api_key)

    # Display Results
    st.subheader(f"🌍 Cultural & Historic Introduction of {city}")
    st.markdown(f"**City Overview**: {city} is known for its rich history and vibrant culture. From ancient temples to modern skyscrapers, there's something for every traveler.")
    
    st.subheader("🗓️ Travel Dates")
    st.markdown(f"**{trip_start.strftime('%B %d, %Y')}** to **{trip_end.strftime('%B %d, %Y')}**")

    if weather_now:
        st.subheader("☁️ Current Weather")
        st.markdown(weather_now)
        st.subheader("🌤️ Weather Forecast")
        st.markdown(weather_forecast)
    else:
        st.subheader("☁️ Current Weather")
        st.markdown(weather_forecast)

    if places:
        st.subheader("🌤️ Google Places (Top 5 Popular Attractions)")
        for place in places:
            st.write(f"- {place}")
    else:
        st.subheader("🌤️ Google Places (Top 5 Popular Attractions)")
        st.write("No places data found.")

    # Flight and Hotel Options
    st.subheader("✈️ Flight Options")
    st.write("Flights are available from various international airports to this city. Please check flight aggregators like Skyscanner, Kayak, or Google Flights for the latest prices and availability.")

    st.subheader("🏨 Hotel Options")
    st.write("Several hotels are available in the area. We recommend checking out popular booking sites like Booking.com, Airbnb, or Trivago for the best deals.")

# Streamlit UI
def main():
    st.title("🗺️ Trip Planner")
    
    # City, Days, Month Input
    city = st.text_input("Enter your city of destination", "Tokyo")
    days = st.number_input("Number of days for your trip", min_value=1, max_value=30, value=3)
    month = st.selectbox("Month of Travel", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    if st.button("Plan My Trip"):
        plan_trip(city, days, month, OPENWEATHER_API_KEY, GOOGLE_API_KEY)

if __name__ == "__main__":
    main()

