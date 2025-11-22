import customtkinter as ctk
import webbrowser
from tkinter import messagebox
from tourism_agents import TourismAgent


# =============================
# APP SETTINGS
# =============================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1100x650")
app.title("🌍 AI Tourism System")

agent = TourismAgent()


# =============================
# FUNCTIONS
# =============================

def clear_output():
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")
    output_box.configure(state="disabled")


# ✅ NEW: Beautiful output formatter
def display_result(result):
    output_box.configure(state="normal")
    output_box.delete("1.0", "end")

    # ============ WEATHER ============
    if "currently" in result:
        weather_line = result.split("\n")[0]
        output_box.insert("end", "🌤 WEATHER REPORT\n\n", "title")
        output_box.insert("end", weather_line + "\n\n", "weather")

    # ============ PLACES ============
    if "And these are the places you can go" in result:
        output_box.insert("end", "📍 TOP PLACES TO VISIT\n\n", "title")

        lines = result.split("\n")
        for line in lines:
            if (
                line.strip()
                and "And these" not in line
                and "currently" not in line
            ):
                output_box.insert("end", f"• {line}\n", "place")

    elif "No tourist attractions" in result:
        output_box.insert("end", "\n🚫 No tourist attractions found\n", "error")

    output_box.configure(state="disabled")


def open_map():
    place = place_entry.get().strip()
    if not place:
        messagebox.showerror("Error", "Enter place first")
        return

    url = f"https://www.openstreetmap.org/search?query={place}"
    webbrowser.open(url)


def get_weather():
    place = place_entry.get().strip()

    if not place:
        messagebox.showerror("Error", "Please enter place name")
        return

    status_label.configure(text="Fetching weather...", text_color="yellow")

    user_input = f"I am going to {place}, what is the temperature there"
    result = agent.handle_request(user_input)

    display_result(result)

    status_label.configure(text="Weather loaded ✅", text_color="lightgreen")


def get_places():
    place = place_entry.get().strip()

    if not place:
        messagebox.showerror("Error", "Please enter place name")
        return

    status_label.configure(text="Finding places...", text_color="yellow")

    user_input = f"I am going to {place}, what places can I visit"
    result = agent.handle_request(user_input)

    display_result(result)

    status_label.configure(text="Places loaded ✅", text_color="lightgreen")


def plan_trip():
    place = place_entry.get().strip()

    if not place:
        messagebox.showerror("Error", "Please enter place name")
        return

    status_label.configure(text="Planning trip...", text_color="yellow")

    user_input = f"I am going to {place}, plan a trip"
    result = agent.handle_request(user_input)

    display_result(result)

    status_label.configure(text="Trip planned ✅", text_color="lightgreen")


# =============================
# SIDEBAR
# =============================

sidebar = ctk.CTkFrame(app, width=200, corner_radius=0)
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="🌍 Tourism AI",
    font=ctk.CTkFont(size=20, weight="bold")
)
logo.pack(pady=30)


weather_btn = ctk.CTkButton(
    sidebar,
    text="☁ Weather",
    height=40,
    command=get_weather
)
weather_btn.pack(pady=10, padx=20, fill="x")


places_btn = ctk.CTkButton(
    sidebar,
    text="📍 Places",
    height=40,
    command=get_places
)
places_btn.pack(pady=10, padx=20, fill="x")


trip_btn = ctk.CTkButton(
    sidebar,
    text="🧭 Plan Trip",
    height=40,
    command=plan_trip
)
trip_btn.pack(pady=10, padx=20, fill="x")


map_btn = ctk.CTkButton(
    sidebar,
    text="🗺️ Open Map",
    height=40,
    fg_color="green",
    command=open_map
)
map_btn.pack(pady=10, padx=20, fill="x")


# =============================
# MAIN AREA
# =============================

main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)


title = ctk.CTkLabel(
    main_frame,
    text="Multi-Agent Tourism System",
    font=ctk.CTkFont(size=24, weight="bold")
)
title.pack(pady=10)


subtitle = ctk.CTkLabel(
    main_frame,
    text="Get Weather • Discover Places • Plan your trip",
    font=ctk.CTkFont(size=14),
    text_color="gray"
)
subtitle.pack()


# =============================
# SEARCH BAR
# =============================

search_frame = ctk.CTkFrame(main_frame)
search_frame.pack(pady=15)

place_entry = ctk.CTkEntry(
    search_frame,
    width=500,
    height=40,
    placeholder_text="Enter location e.g. Bangalore, Hampi, Mangalore..."
)
place_entry.pack(padx=10, pady=10)


# =============================
# OUTPUT BOX
# =============================

output_box = ctk.CTkTextbox(
    main_frame,
    width=820,
    height=350,
    font=ctk.CTkFont(size=14)
)
output_box.pack(pady=20)

# TEXT TAGS (colors)
output_box.tag_config("title", foreground="#00ADB5")
output_box.tag_config("weather", foreground="#4D96FF")
output_box.tag_config("place", foreground="#EEEEEE")
output_box.tag_config("error", foreground="red")

output_box.configure(state="disabled")


# =============================
# STATUS BAR
# =============================

status_label = ctk.CTkLabel(
    main_frame,
    text="Ready ✅",
    text_color="lightgreen"
)
status_label.pack()


# =============================
# FOOTER
# =============================

footer = ctk.CTkLabel(
    main_frame,
    text="Powered by Nominatim | Open-Meteo | Overpass API",
    text_color="gray"
)
footer.pack(pady=5)


# =============================
# START APP
# =============================
app.mainloop()
