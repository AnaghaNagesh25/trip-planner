import streamlit as st

# Pre-loaded Mock Data for Weather, Flights, Hotels, Attractions, and Itinerary
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

places_data = {
    "Tokyo": ["Tokyo Tower", "Shibuya Crossing", "Meiji Shrine", "Asakusa Temple", "Odaiba"],
    "Udaipur": ["Lake Pichola", "City Palace", "Jag Mandir", "Sajjangarh Palace", "Bagore Ki Haveli"]
}

itinerary_data = {
    "Tokyo": {
        "Day 1": "Visit the iconic Tokyo Tower, explore the bustling Shibuya Crossing.",
        "Day 2": "Visit Meiji Shrine and explore the Odaiba area.",
        "Day 3": "Tour Asakusa Temple and shopping at Ginza."
    },
    "Udaipur": {
        "Day 1": "Explore the majestic City Palace and enjoy a boat ride on Lake Pichola.",
        "Day 2": "Visit Jag Mandir and Sajjangarh Palace.",
        "Day 3": "Explore Bagore Ki Haveli and the local markets."
    }
}

# Function to Generate Trip Plan
def generate_trip_plan(city, days, month):
    city_weather = weather_data.get(city, {"current": "Data not available", "forecast": "Data not available"})
    city_flights = flight_data.get(city, [])
    city_hotels = hotel_data.get(city, [])
    city_places = places_data.get(city, [])
    city_itinerary = itinerary_data.get(city, {})
    
    # Displaying the Trip Plan
    st.write(f"### Trip Plan for {city}")
    st.write(f"🗓️ **Travel Dates**: {days} days in {month}")
    
    # City Cultural and Historical Significance
    st.write(f"🏛️ **Cultural & Historic Significance**:")
    st.write(f"The city of {city} is known for its rich culture and history. Explore the historic landmarks and vibrant culture during your stay.")
    
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
    
    # Day-wise Itinerary (Adjust based on number of days)
    st.write("🗺️ **Day-wise Itinerary**:")
    days_in_itinerary = min(days, len(city_itinerary))  # Ensure itinerary doesn't exceed available days
    for i in range(1, days_in_itinerary + 1):
        day_plan = city_itinerary.get(f"Day {i}", "No plan available")
        st.write(f"Day {i}: {day_plan}")
    
# Streamlit UI Setup
def main():
    st.title("Trip Planner App")

    # City Input (User can input any city)
    city = st.text_input("Enter City Name", "Tokyo")
    
    # Travel Days Input
    days = st.number_input("Enter number of travel days", min_value=1, max_value=30, value=3)
    
    # Travel Month Input
    month = st.text_input("Enter travel month", "May")

    # Button to generate trip plan
    if st.button("Generate Trip Plan"):
        generate_trip_plan(city, days, month)

if __name__ == "__main__":
    main()

