import streamlit as st
import datetime

# Pre-loaded Data for Mocking API Responses

# Mock Weather Data
weather_data = {
    "Tokyo": {
        "current": "16°C, Clear Sky",
        "forecast": "17°C to 19°C for the next 3 days"
    },
    "Udaipur": {
        "current": "28°C, Sunny",
        "forecast": "30°C to 32°C for the next 3 days"
    }
}

# Mock Flight Data
flight_data = {
    "Tokyo": [
        {"flight": "Flight 1: Air India", "time": "10:30 AM", "price": "$500"},
        {"flight": "Flight 2: Emirates", "time": "2:00 PM", "price": "$650"}
    ],
    "Udaipur": [
        {"flight": "Flight 1: SpiceJet", "time": "7:00 AM", "price": "$150"},
        {"flight": "Flight 2: Indigo", "time": "12:00 PM", "price": "$180"}
    ]
}

# Mock Hotel Data
hotel_data = {
    "Tokyo": [
        {"name": "Hotel Tokyo Bay", "price": "$150 per night", "rating": "4.5/5"},
        {"name": "Shibuya Crossing Hotel", "price": "$180 per night", "rating": "4.7/5"}
    ],
    "Udaipur": [
        {"name": "Lake Pichola Hotel", "price": "$120 per night", "rating": "4.8/5"},
        {"name": "Udaipur Palace Hotel", "price": "$130 per night", "rating": "4.6/5"}
    ]
}

# Mock Google Places Data (Tourist Attractions)
places_data = {
    "Tokyo": ["Tokyo Tower", "Shibuya Crossing", "Meiji Shrine", "Asakusa Temple", "Odaiba"],
    "Udaipur": ["Lake Pichola", "City Palace", "Jag Mandir", "Sajjangarh Palace", "Bagore Ki Haveli"]
}

# Define the Trip Planning function
def plan_trip(city, days, month):
    # Get city data
    city_weather = weather_data.get(city, {"current": "Data not available", "forecast": "Data not available"})
    city_flights = flight_data.get(city, [])
    city_hotels = hotel_data.get(city, [])
    city_places = places_data.get(city, [])

    # Display Trip Plan
    st.write(f"### Trip Plan for {city}")
    st.write(f"🗓️ **Travel Dates**: {days} days in {month}")
    
    # Weather Information
    st.write(f"☁️ **Current Weather**: {city_weather['current']}")
    st.write(f"🌤️ **Weather Forecast**: {city_weather['forecast']}")
    
    # Google Places (Top Attractions)
    if city_places:
        st.write("🌟 **Top 5 Attractions**:")
        for place in city_places:
            st.write(f"- {place}")
    else:
        st.write("❌ No places data found.")
    
    # Flight Options
    if city_flights:
        st.write("✈️ **Flight Options**:")
        for flight in city_flights:
            st.write(f"- {flight['flight']} at {flight['time']}, Price: {flight['price']}")
    else:
        st.write("❌ No flight options found.")
    
    # Hotel Options
    if city_hotels:
        st.write("🏨 **Hotel Options**:")
        for hotel in city_hotels:
            st.write(f"- {hotel['name']}, Price: {hotel['price']}, Rating: {hotel['rating']}")
    else:
        st.write("❌ No hotel options found.")

# Streamlit UI Setup
def main():
    st.title("Trip Planner App")

    # City Input
    city = st.selectbox("Select City", ["Tokyo", "Udaipur"])
    
    # Travel Days Input
    days = st.number_input("Enter number of travel days", min_value=1, max_value=30, value=3)
    
    # Travel Month Input
    month = st.text_input("Enter travel month", "May")

    # Button to generate trip plan
    if st.button("Generate Trip Plan"):
        plan_trip(city, days, month)

if __name__ == "__main__":
    main()

