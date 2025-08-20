# import requests
# import tkinter as tk
# from tkinter import messagebox
# from PIL import Image, ImageTk

# # Replace with your OpenWeatherMap API key
# API_KEY = "YOUR_API_KEY"
# BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
# FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric"

# # Fetch current weather data
# def get_weather(city):
#     try:
#         response = requests.get(BASE_URL.format(city, API_KEY))
#         data = response.json()

#         if data["cod"] != 200:
#             messagebox.showerror("Error", "City not found!")
#             return None

#         weather = {
#             "city": data["name"],
#             "temp": data["main"]["temp"],
#             "humidity": data["main"]["humidity"],
#             "description": data["weather"][0]["description"].capitalize(),
#             "icon": data["weather"][0]["icon"]
#         }
#         return weather

#     except Exception as e:
#         messagebox.showerror("Error", "Failed to fetch weather data!")
#         return None

# # Fetch weather forecast (next 3 days)
# def get_forecast(city):
#     try:
#         response = requests.get(FORECAST_URL.format(city, API_KEY))
#         data = response.json()

#         if data["cod"] != "200":
#             return None

#         forecast_list = []
#         for forecast in data["list"]:
#             time = forecast["dt_txt"]
#             if "12:00:00" in time:  # Select midday forecast
#                 forecast_list.append({
#                     "date": time.split()[0],
#                     "temp": forecast["main"]["temp"],
#                     "desc": forecast["weather"][0]["description"].capitalize()
#                 })

#             if len(forecast_list) == 3:  # Limit to 3 days
#                 break

#         return forecast_list

#     except Exception as e:
#         return None

# # Update UI with weather data
# def update_weather():
#     city = city_entry.get().strip()
#     if not city:
#         messagebox.showwarning("Warning", "Please enter a city name!")
#         return

#     weather = get_weather(city)
#     forecast = get_forecast(city)

#     if weather:
#         weather_label.config(text=f"{weather['city']}\n{weather['temp']}°C, {weather['description']}\nHumidity: {weather['humidity']}%")
        
#         # Load weather icon
#         icon_url = f"http://openweathermap.org/img/wn/{weather['icon']}@2x.png"
#         icon_image = ImageTk.PhotoImage(Image.open(requests.get(icon_url, stream=True).raw))
#         weather_icon.config(image=icon_image)
#         weather_icon.image = icon_image

#     if forecast:
#         forecast_text = "3-Day Forecast:\n" + "\n".join([f"{f['date']}: {f['temp']}°C, {f['desc']}" for f in forecast])
#         forecast_label.config(text=forecast_text)
#     else:
#         forecast_label.config(text="No forecast data available.")

# # GUI Setup
# root = tk.Tk()
# root.title("Weather App")
# root.geometry("400x500")

# tk.Label(root, text="Enter City Name:", font=("Arial", 12)).pack(pady=5)
# city_entry = tk.Entry(root, font=("Arial", 12), width=30)
# city_entry.pack(pady=5)

# tk.Button(root, text="Get Weather", command=update_weather, font=("Arial", 12), bg="blue", fg="white").pack(pady=5)

# weather_icon = tk.Label(root)
# weather_icon.pack()

# weather_label = tk.Label(root, text="", font=("Arial", 14))
# weather_label.pack()

# forecast_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
# forecast_label.pack(pady=10)

# root.mainloop()



import requests
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Set your OpenWeatherMap API Key
API_KEY = "your_api_key_here"  # Replace with your OpenWeatherMap API Key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data
def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data["cod"] != 200:
            messagebox.showerror("Error", f"City '{city}' not found!")
            return None

        weather_info = {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"]
        }
        return weather_info

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch weather: {e}")
        return None

# Function to update weather display
def update_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name!")
        return

    weather_data = get_weather(city)
    if weather_data:
        temp_label.config(text=f"Temperature: {weather_data['temperature']}°C")
        humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        weather_label.config(text=f"Condition: {weather_data['weather'].capitalize()}")

        # Fetch and display weather icon
        icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
        response = requests.get(icon_url)
        img_data = Image.open(BytesIO(response.content))
        img = ImageTk.PhotoImage(img_data)
        icon_label.config(image=img)
        icon_label.image = img

# Create GUI window
root = Tk()
root.title("Weather App")
root.geometry("300x350")

Label(root, text="Enter City:", font=("Arial", 12)).pack()
city_entry = Entry(root, font=("Arial", 12))
city_entry.pack()

Button(root, text="Get Weather", command=update_weather, font=("Arial", 12), bg="blue", fg="white").pack(pady=5)

icon_label = Label(root)
icon_label.pack()

temp_label = Label(root, text="", font=("Arial", 12))
temp_label.pack()

humidity_label = Label(root, text="", font=("Arial", 12))
humidity_label.pack()

weather_label = Label(root, text="", font=("Arial", 12))
weather_label.pack()

root.mainloop()
