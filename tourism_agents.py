import requests
import re
import traceback

# ==========================
# Child Agent: Geocoding (Nominatim)
# ==========================
class GeocodingAgent:
    BASE_URL = "https://nominatim.openstreetmap.org/search"

    @staticmethod
    def get_coordinates(place_name: str):

        headers = {"User-Agent": "multi-agent-tourism/1.0"}

        search_variations = [
            place_name,
            place_name + " India",
            place_name + " city",
            place_name.replace("alore", "aluru"),
            place_name.replace("galore", "galuru"),
            place_name.replace("bangalore", "bengaluru"),
            place_name.replace("mysore", "mysuru"),
            place_name.replace("mantralaym", "mantralayam"),
            place_name.replace("mantralyam", "mantralayam"),
        ]

        for query in search_variations:

            params = {"q": query, "format": "json", "limit": 1}

            try:
                response = requests.get(
                    GeocodingAgent.BASE_URL,
                    params=params,
                    headers=headers,
                    timeout=10
                )
            except:
                continue

            if response.status_code != 200:
                continue

            try:
                data = response.json()
            except:
                continue

            if data:
                first = data[0]
                lat = float(first["lat"])
                lon = float(first["lon"])
                return {"lat": lat, "lon": lon}

        return None


# ==========================
# Child Agent: Weather (Open-Meteo)
# ==========================
class WeatherAgent:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def get_weather(lat, lon):

        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m",
            "hourly": "precipitation_probability",
            "timezone": "auto"
        }

        response = requests.get(WeatherAgent.BASE_URL, params=params, timeout=10)

        if response.status_code != 200:
            raise Exception("Weather API error")

        data = response.json()

        temperature = data.get("current", {}).get("temperature_2m")
        rain_list = data.get("hourly", {}).get("precipitation_probability", [])
        rain_chance = rain_list[0] if rain_list else None

        return temperature, rain_chance


# ==========================
# Child Agent: Places (Overpass) ✅ UPDATED
# ==========================
class PlacesAgent:

    OVERPASS_SERVERS = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.openstreetmap.ru/api/interpreter"
    ]

    @staticmethod
    def get_places(lat, lon, radius=40000, limit=5):   # ✅ radius increased

        query = f"""
        [out:json][timeout:40];
        (
          node["tourism"](around:{radius},{lat},{lon});
          way["tourism"](around:{radius},{lat},{lon});
          relation["tourism"](around:{radius},{lat},{lon});

          node["historic"](around:{radius},{lat},{lon});
          way["historic"](around:{radius},{lat},{lon});
          relation["historic"](around:{radius},{lat},{lon});

          node["leisure"="park"](around:{radius},{lat},{lon});
          way["leisure"="park"](around:{radius},{lat},{lon});

          node["natural"="beach"](around:{radius},{lat},{lon});
          way["natural"="beach"](around:{radius},{lat},{lon});

          node["natural"="peak"](around:{radius},{lat},{lon});
          way["natural"="peak"](around:{radius},{lat},{lon});

          node["waterway"](around:{radius},{lat},{lon});
        );
        out tags center qt;
        """

        data = None

        for server in PlacesAgent.OVERPASS_SERVERS:
            try:
                response = requests.post(server, data={"data": query}, timeout=40)
                if response.status_code == 200:
                    data = response.json()
                    break
            except:
                continue

        if not data:
            raise Exception("All Overpass servers failed")

        ignore_words = [
            "guest", "resort", "lodge", "hotel", "hostel",
            "homestay", "residency", "villa", "apartment",
            "building", "complex", "tower", "office",
            "school", "hospital", "company",
            "bridge", "road", "junction", "layout",
            "mosque", "masjid", "church"
        ]

        valid_words = [
            "palace", "garden", "park", "fort", "monument",
            "beach", "falls", "waterfall", "hill", "peak",
            "lake", "dam", "zoo", "sanctuary", "forest",
            "botanical", "national", "island", "viewpoint",

            # ✅ ADDED FOR HAMPI / MANTRALAYAM
            "ruins", "heritage", "archaeological", "temple", "ghat"
        ]

        bad_suffixes = [" entrance", " gate", " arch", " main gate"]

        # ----- STRICT MODE -----
        places = []
        seen = set()

        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name")

            if not name:
                continue

            if "wikipedia" not in tags and "wikidata" not in tags:
                continue

            lname = name.lower().strip()

            if any(word in lname for word in ignore_words):
                continue

            if not any(word in lname for word in valid_words):
                continue

            display_name = name
            for suf in bad_suffixes:
                if display_name.lower().endswith(suf):
                    display_name = display_name[: -len(suf)].strip()
                    break

            if display_name not in seen:
                places.append(display_name)
                seen.add(display_name)

            if len(places) >= limit:
                break

        # ----- RELAX MODE -----
        if len(places) < 2:
            places = []
            seen = set()

            for element in data.get("elements", []):
                tags = element.get("tags", {})
                name = tags.get("name")

                if not name:
                    continue

                lname = name.lower().strip()

                if any(word in lname for word in ignore_words):
                    continue

                if not any(word in lname for word in valid_words):
                    continue

                display_name = name
                for suf in bad_suffixes:
                    if display_name.lower().endswith(suf):
                        display_name = display_name[: -len(suf)].strip()
                        break

                if display_name not in seen:
                    places.append(display_name)
                    seen.add(display_name)

                if len(places) >= limit:
                    break

        return places


# ==========================
# Parent Agent
# ==========================
class TourismAgent:
    def __init__(self):
        self.geocoder = GeocodingAgent()
        self.weather = WeatherAgent()
        self.places = PlacesAgent()

    def extract_place(self, user_input: str):

        match = re.search(r"\bto\s+([A-Za-z\s]+?)(?:[,.!?]|$)", user_input, re.I)
        if match:
            return match.group(1).strip()

        match = re.search(r"\bin\s+([A-Za-z\s]+?)(?:[,.!?]|$)", user_input, re.I)
        if match:
            return match.group(1).strip()

        matches = re.findall(r"(?:[A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", user_input)
        if matches:
            return max(matches, key=len)

        return user_input.strip()

    def parse_intent(self, text: str):

        text = text.lower()

        # ✅ FIX: plan + trip → BOTH
        if "plan" in text and "trip" in text:
            return True, True

        weather_keywords = [
            "weather", "temperature", "climate",
            "hot", "cold", "rain", "rainfall"
        ]

        place_keywords = [
            "visit", "places", "spots", "attractions",
            "sightseeing", "tourist"
        ]

        want_weather = any(word in text for word in weather_keywords)
        want_places = any(word in text for word in place_keywords)

        if not want_weather and not want_places:
            want_weather = True
            want_places = True

        return want_weather, want_places

    def handle_request(self, user_input: str):

        place = self.extract_place(user_input)
        want_weather, want_places = self.parse_intent(user_input)

        coords = self.geocoder.get_coordinates(place)

        if not coords:
            return "I don’t know this place exists."

        lat = coords['lat']
        lon = coords['lon']

        output = ""

        if want_weather:
            try:
                temp, rain = self.weather.get_weather(lat, lon)
                if temp is not None and rain is not None:
                    output += f"In {place} it’s currently {temp}°C with a {rain}% chance of rain.\n"
                elif temp is not None:
                    output += f"In {place} it’s currently {temp}°C.\n"
            except:
                output += "Weather service unavailable.\n"

        if want_places:
            try:
                places = self.places.get_places(lat, lon)

                if places:
                    output += "\nAnd these are the places you can go:\n"
                    for p in places:
                        output += p + "\n"
                else:
                    output += "\nNo tourist attractions found nearby."
            except:
                output += "\nPlaces service unavailable."

        return output.strip()


# ==========================
# MAIN
# ==========================
if __name__ == "__main__":

    agent = TourismAgent()

    print("\nMulti-Agent Tourism System (Nominatim + Open-Meteo + Overpass)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        try:
            reply = agent.handle_request(user_input)
            print("\nAgent:", reply)
        except Exception:
            print("\nAgent: Something went wrong")
            traceback.print_exc()
