import streamlit as st
from tourism_agents import TourismAgent
import urllib.parse

agent = TourismAgent()

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="AI Tourism System",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #141e30, #243b55);
}

.main {
    background-color: transparent;
}

.title {
    text-align: center;
    font-size: 38px;
    font-weight: bold;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #aaaaaa;
    margin-bottom:20px;
}

.card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
    border-left: 6px solid #00ffa6;
}

.place-title {
    font-size: 20px;
    font-weight: bold;
    color: #222;
}

.badge {
    background: #ff7e5f;
    padding: 5px 12px;
    border-radius: 20px;
    color: white;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 10px;
}

.weather-box {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    font-size: 22px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.3);
}

.footer {
    text-align: center;
    margin-top: 40px;
    color: #999;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------
# HEADER
# --------------------------------
st.markdown('<div class="title">🌍 Multi-Agent Tourism System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Weather • Attractions • Trip Planning</div>', unsafe_allow_html=True)

place = st.text_input(
    "Enter place name",
    placeholder="Ex: Bangalore, Hampi, Chikkamagaluru"
)

col1, col2, col3 = st.columns(3)


# --------------------------------
# FUNCTION TO SHOW PLACES IN CARDS
# --------------------------------
def display_places(places_list, city):
    st.markdown("## 📍 Top Attractions")

    for place_name in places_list:
        maps_url = f"https://www.google.com/maps/search/{urllib.parse.quote_plus(place_name + ' ' + city)}"

        card_html = f"""
        <div class="card">
            <div class="badge">ATTRACTION</div>
            <div class="place-title">{place_name}</div>
            <br>
            📍 <a href="{maps_url}" target="_blank">Open in Google Maps</a>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)


# --------------------------------
# WEATHER BUTTON
# --------------------------------
with col1:
    if st.button("☁️ Get Weather"):
        if place:
            query = f"I am going to {place}, what is the temperature there"
            result = agent.handle_request(query)

            st.markdown(f"""
            <div class="weather-box">
                🌤️ Weather in {place} <br><br>
                {result}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Please enter a place")


# --------------------------------
# PLACES BUTTON
# --------------------------------
with col2:
    if st.button("📍 Get Places"):
        if place:
            query = f"I am going to {place}, what places can I visit"
            result = agent.handle_request(query)

            if "And these are the places you can go:" in result:
                places_list = result.split("And these are the places you can go:")[1].strip().split("\n")
                display_places(places_list, place)
            else:
                st.warning(result)
        else:
            st.error("Please enter a place")


# --------------------------------
# PLAN TRIP BUTTON (WEATHER + PLACES)
# --------------------------------
with col3:
    if st.button("🧭 Plan Trip"):
        if place:
            query = f"I am going to {place}, let's plan a trip"
            result = agent.handle_request(query)

            lines = result.split("\n")

            # Weather part
            weather_info = lines[0]
            st.markdown(f"""
            <div class="weather-box">
                🌍 Trip Weather for {place} <br><br>
                {weather_info}
            </div>
            """, unsafe_allow_html=True)

            # Places part
            if "And these are the places you can go:" in result:
                places_list = result.split("And these are the places you can go:")[1].strip().split("\n")
                display_places(places_list, place)

        else:
            st.error("Please enter a place")


# --------------------------------
# FOOTER
# --------------------------------
st.markdown("""
<div class="footer">
    Powered by Nominatim | Open-Meteo | Overpass API <br><br>
    Developed for Multi-Agent Systems Assignment
</div>
""", unsafe_allow_html=True)
