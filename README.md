# 🌍 Multi-Agent Tourism System

An AI-powered multi-agent tourism system that helps users get travel-related information for any location.

The system can:
- Show current weather
- Suggest popular tourist attractions
- Help plan a complete trip
- Display the location on an interactive map

---

## 🌐 Live Demo (Deployed Application)

👉 Click here to use the application live:  
https://multi-agent-tourism-system-72mvdgjtjclcj9m4aaxcpl.streamlit.app/

---

## 🔗 GitHub Repository

https://github.com/Soujanya315/Multi-Agent-Tourism-System

---

## 🚀 Features

✅ Multi-agent architecture  
✅ Live weather information (Open-Meteo API)  
✅ Tourist places listing (Overpass API)  
✅ Location detection (Nominatim API)  
✅ Clean & interactive UI (Streamlit / CustomTkinter)  
✅ Map view using OpenStreetMap  
✅ Real-time API-based results (NO hardcoding)  

---

## 🧠 Agents Used

1. **Geocoding Agent**  
   Converts the entered place name into latitude and longitude using the Nominatim API.

2. **Weather Agent**  
   Retrieves the live temperature and rain probability using Open-Meteo API.

3. **Places Agent**  
   Finds nearby tourist attractions using the Overpass API and OpenStreetMap data.

4. **Parent Tourism Agent**  
   Orchestrates all child agents and returns a combined response.

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Requests
- Nominatim API
- Open-Meteo API
- Overpass API
- OpenStreetMap

---

## 📦 Requirements

streamlit
requests

Install using:

pip install -r requirements.txt

---

## ▶ How To Run Locally

1. Clone the repository:
git clone https://github.com/Soujanya315/Multi-Agent-Tourism-System.git

2. Go inside the folder:

3. Install requirements:

4. Run the Streamlit app:
python -m streamlit run app.py

---

## 📥 Example Inputs

- `I am going to Bangalore`
- `I am going to Hampi, what is the temperature?`
- `Plan a trip to Mangalore`
- `Show places in Chikkamagaluru`

---

## ✅ Output

The system displays:
- Current temperature
- Rain probability
- Top tourist attractions
- Travel suggestions
- Map location

---

## 🎓 Project Info

Developed as part of a **Multi-Agent Systems Assignment**  
Role selected: **AI Developer**

