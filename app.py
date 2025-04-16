import streamlit as st
import requests
from datetime import datetime, timedelta

# Function to get current weather using OpenWeather API
def get_weather(city_name, api_key):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if response.status_code == 200:
        return f"🌡️ {data['main']['temp']}°C, {data['weather'][0]['description']}, Humidity: {data['main']['humidity']}%"
    else:
        return "Weather data not available."

# Function to get flight information using Skyscanner API
def get_flights(origin, destination, date, api_key):
    url = f"https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/{origin}/{destination}/{date}"
    headers = {'apikey': api_key}
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'Quotes' in data:
        quote = data['Quotes'][0]
        return f"💺 Flight from {origin} to {destination} on {quote['MinPrice']} USD, departing {quote['OutboundLeg']['DepartureDate']}"
    else:
        return "No flight data available."

# Function to get hotel information using Google Places API
def get_hotels(location, api_key):
    base_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=1500&type=lodging&key={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if 'results' in data:
        hotels = data['results'][:3]  # Get top 3 hotels
        return "\n".join([f"🏨 {hotel['name']} - {hotel.get('vicinity', 'No address provided')}" for hotel in hotels])
    else:
        return "No hotel data available."

# Main function to handle the trip planning
def plan_trip(city, days, month, weather_api_key, flight_api_key, hotel_api_key):
    # Calculate the trip start and end date
    today = datetime.today()
    month_index = ["January", "February", "March", "April", "May", "June", "July"].index(month) + 1
    trip_start = today.replace(month=month_index, day=min(today.day, 28))  # Avoid month-end errors
    trip_end = trip_start + timedelta(days=days - 1)

    # Get weather information
    weather_now = get_weather(city, weather_api_key)

    # Get flight and hotel options
    flight_info = get_flights("JFK", city, trip_start.strftime('%Y-%m-%d'), flight_api_key)
    hotel_info = get_hotels("35.6895,139.6917", hotel_api_key)  # Example for Tokyo's coordinates

    # Display Results
    st.subheader(f"🌍 Cultural & Historic Introduction of {city}")
    st.markdown(f"**{city}** is known for its vibrant history and rich culture. The city offers a unique blend of traditional culture and modern attractions.")

    st.subheader("🗓️ Travel Dates")
    st.markdown(f"**{trip_start.strftime('%B %d, %Y')}** to **{trip_end.strftime('%B %d, %Y')}**")

    st.subheader("☁️ Current Weather")
    st.markdown(weather_now)

    st.subheader("🌤️ Weather Forecast During Trip")
    st.markdown(f"Expect pleasant weather during your trip to {city}. Ensure to carry light clothing and an umbrella.")

    st.subheader("✈️ Flight Option")
    st.markdown(flight_info)

    st.subheader("🏨 Hotel Option")
    st.markdown(hotel_info)

# Streamlit UI setup
def main():
    st.title("Trip Planner")
    
    # Inputs from the user
    city = st.text_input("Enter the city for your trip:", "Tokyo")
    days = st.number_input("Number of days for your trip:", min_value=1, max_value=10, value=3)
    month = st.selectbox("Select the month of your trip:", ["January", "February", "March", "April", "May", "June", "July"])

    # Add your API keys here
    weather_api_key = "YOUR_OPENWEATHER_API_KEY"
    flight_api_key = "YOUR_SKYSCANNER_API_KEY"
    hotel_api_key = "YOUR_GOOGLE_PLACES_API_KEY"

    if st.button("Plan Trip"):
        plan_trip(city, days, month, weather_api_key, flight_api_key, hotel_api_key)

if __name__ == "__main__":
    main()

