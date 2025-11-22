import streamlit as st
from tourism_agents import TourismAgent

agent = TourismAgent()

st.set_page_config(
    page_title="Multi-Agent Tourism System",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Multi-Agent Tourism System")
st.subheader("Get Weather • Discover Places • Plan Your Trip")

place = st.text_input("Enter place name", placeholder="Ex: Bangalore, Hampi, Chikkamagaluru")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("☁ Get Weather"):
        if place:
            query = f"I am going to {place}, what is the temperature there"
            result = agent.handle_request(query)

            st.success("Weather Info Loaded ✅")
            st.text_area("Result", result, height=250)
        else:
            st.error("Please enter a place")

with col2:
    if st.button("📍 Get Places"):
        if place:
            query = f"I am going to {place}, what places can I visit"
            result = agent.handle_request(query)

            st.success("Places Loaded ✅")
            st.text_area("Result", result, height=250)
        else:
            st.error("Please enter a place")

with col3:
    if st.button("🧭 Plan Trip"):
        if place:
            query = f"I am going to {place}, let's plan a trip"
            result = agent.handle_request(query)

            st.success("Trip Planned ✅")
            st.text_area("Result", result, height=250)
        else:
            st.error("Please enter a place")

st.markdown("---")
st.write("Powered by Nominatim | Open-Meteo | Overpass API")
