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

# Expanded Cultural Significance Articles (Sample)
cultural_articles = {
    "Tokyo": """
        Tokyo, the capital city of Japan, stands as a testament to the rich cultural and historical fabric of the nation. This sprawling metropolis has a history that stretches back more than 400 years, originating as a humble fishing village called Edo. By the 17th century, it became the seat of the Tokugawa shogunate, which ruled Japan for over 250 years. Tokyo is a city where ancient traditions and cutting-edge modernity coexist, making it one of the most vibrant cities in the world.

        At the heart of Tokyo’s cultural significance is its deep connection to both Shintoism and Buddhism. Landmarks such as the Meiji Shrine and Senso-ji Temple represent the city's religious devotion and serve as spiritual havens amidst the bustling urban landscape. Meiji Shrine, dedicated to Emperor Meiji, is a tranquil escape, with its beautiful Torii gates leading into serene wooded areas. On the other hand, Asakusa's Senso-ji Temple, one of the oldest in Tokyo, offers a look into traditional Japanese architecture, culture, and religious practices.

        Tokyo's culture is not only defined by its temples but also by its modern achievements. The city is a global hub for technology, fashion, and design. Akihabara is known for its cutting-edge electronics, while districts like Harajuku showcase Tokyo's vibrant street fashion. The fusion of Western influences with traditional Japanese elements is seen in everything from cuisine to pop culture. Tokyo's culinary scene, exemplified by sushi, ramen, and tempura, reflects the city’s history and its embrace of both global and local influences.

        In addition to its historical landmarks and modern innovations, Tokyo is home to a thriving arts scene, with museums like the Tokyo National Museum and teamLab Borderless. Traditional Japanese arts like tea ceremonies, ikebana (flower arranging), and kabuki theatre can still be experienced, giving travelers a deeper understanding of the nation's cultural heritage.

        As the epicenter of Japanese pop culture, Tokyo also leads the world in anime, manga, and gaming. Locations like Akihabara and Nakano Broadway have earned global recognition for their contribution to this genre, attracting fans from all over the world. Tokyo's blend of the old and the new, tradition and innovation, makes it a truly dynamic city to explore.

        Overall, Tokyo is more than just a bustling metropolis; it is a city that tells the story of Japan's past, its present, and its future. It’s a place where visitors can experience ancient temples, admire breathtaking skyscrapers, shop in trendy districts, and immerse themselves in the rich tapestry of Japanese culture.
    """,
    "Udaipur": """
        Udaipur, often referred to as the "City of Lakes," is one of the most culturally and historically rich cities in Rajasthan, India. Located in the southwestern part of the state, Udaipur is a symbol of royal grandeur, art, and the rich traditions of Rajasthan. Known for its picturesque lakes and majestic palaces, Udaipur has a rich heritage that dates back to 1559 when Maharana Udai Singh II founded the city.

        Udaipur's City Palace, perched on the banks of Lake Pichola, is a magnificent testament to the architectural prowess of the Mewar dynasty. It is the largest palace complex in Rajasthan, with over 400 rooms, courtyards, and gardens, showcasing intricate carvings, murals, and stunning views of the surrounding lakes and hills. This palace is not just an architectural marvel, but it also holds the cultural significance of the royal family’s legacy in Rajasthan’s history.

        The city's culture is deeply rooted in the arts, especially in music, dance, and painting. Udaipur is home to several traditional dance forms like Ghoomar and Kalbeliya, which are performed during cultural festivals and celebrations. The city also boasts a rich tradition of miniature painting, which is famous for its vivid colors and intricate details, often depicting scenes from Indian mythology and royal court life.

        Udaipur is also famous for its festivals, with the Mewar Festival being the most notable. This festival celebrates the arrival of spring and marks the beginning of the new year in the Hindu calendar. It is celebrated with grand processions, folk music, and dance performances, providing a window into the vibrant cultural life of Udaipur.

        Aside from its royal heritage, Udaipur's lakes play an essential role in its cultural significance. The boat rides on Lake Pichola offer visitors the chance to witness the natural beauty of the city, while enjoying views of the City Palace, Jag Mandir, and the Lake Palace Hotel, which seems to float on the water. These experiences allow visitors to connect with the natural beauty and tranquility of the region, which has inspired poets, artists, and travelers for centuries.

        Udaipur's culture is also closely linked to its craftsmanship. The city is known for its intricate silver jewelry, traditional pottery, and hand-woven textiles, which are prized by collectors and travelers alike. The markets in Udaipur are filled with vibrant stalls selling local crafts, giving visitors the opportunity to bring home a piece of Rajasthan's rich artistic heritage.

        Overall, Udaipur offers an unforgettable blend of royal heritage, cultural vibrancy, and natural beauty. Whether exploring the palaces, attending a traditional dance performance, or simply enjoying a boat ride on the lakes, visitors can experience the timeless charm of this majestic city. Udaipur is a place where the past and the present come together to offer a truly immersive cultural experience.
    """
}

# Function to Generate Detailed Trip Plan
def generate_trip_plan(city, days, month):
    city_weather = weather_data.get(city, {"current": "Data not available", "forecast": "Data not available"})
    city_flights = flight_data.get(city, [])
    city_hotels = hotel_data.get(city, [])
    city_places = places_data.get(city, [])
    city_itinerary = itinerary_data.get(city, {})
    city_culture = cultural_articles.get(city, "Cultural information not available.")
    
    # Displaying the Trip Plan
    st.write(f"### Trip Plan for {city}")
    st.write(f"🗓️ **Travel Dates**: {days} days in {month}")
    
    # City Cultural and Historical Significance
    st.write(f"🏛️ **Cultural & Historic Significance**:")
    st.write(city_culture)
    
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
            st.write(f"- {flight['flight

