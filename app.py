import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Function to get weather data from OpenWeather API
def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        # Debugging: print the response
        st.write("Weather API response:", data)
        weather_description = data.get("weather", [{}])[0].get("description", "No description available")
        temperature = data.get("main", {}).get("temp", "N/A")
        return f"Weather: {weather_description}, Temp: {temperature}°C"
    else:
        return f"Error: Unable to fetch weather data. API responded with {data.get('message', 'Unknown error')}."

# Function to get top places from Google Places API
def get_google_places(city, api_key):
    # Use geocoding to get latitude and longitude for the city
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={api_key}"
    geocode_response = requests.get(geocode_url)
    geocode_data = geocode_response.json()
    
    if geocode_response.status_code == 200 and geocode_data['status'] == 'OK':
        lat = geocode_data['results'][0]['geometry']['location']['lat']
        lng = geocode_data['results'][0]['geometry']['location']['lng']
        places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1500&type=tourist_attraction&key={api_key}"
        places_response = requests.get(places_url)
        places_data = places_response.json()
        
        if places_response.status_code == 200 and places_data['status'] == 'OK':
            # Extract top 5 attractions
            places = [place['name'] for place in places_data.get('results', [])[:5]]
            return places if places else ["No attractions found."]
        else:
            return ["Error: Unable to fetch places data."]
    else:
        return ["Error: Unable to geocode city for places."]

# Main function to display the trip details
def plan_trip(city):
    # Get weather info
    weather_info = get_weather(city, OPENWEATHER_API_KEY)
    # Get popular places info
    google_places = get_google_places(city, GOOGLE_API_KEY)

    # Display results in Streamlit
    st.title(f"🌍 Trip Planning for {city}")
    
    st.subheader("🗓️ Travel Dates")
    st.markdown(f"**January 16, 2025 to January 18, 2025**")

    st.subheader("☁️ Current Weather")
    st.markdown(weather_info)

    st.subheader("🌤️ Google Places (Top 5 Popular Attractions)")
    st.markdown(f"**{', '.join(google_places)}**")

    st.subheader("✈️ Flight Options")
    st.markdown("Flights are available from various international airports to this city. Please check flight aggregators like Skyscanner, Kayak, or Google Flights for the latest prices and availability.")

    st.subheader("🏨 Hotel Options")
    st.markdown("Several hotels are available in the area. We recommend checking out popular booking sites like Booking.com, Airbnb, or Trivago for the best deals.")

# Streamlit UI
city = st.text_input("Enter the city for your trip:", "Tokyo")
if city:
    plan_trip(city)


