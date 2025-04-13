import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

API_KEY = "b5d6454f2f9c68f7b1d832c058bc0db9"
cities = ["Mumbai", "Pune", "Chennai", "Delhi", "Bangalore", "Kolkata", "Jaipur", "Hyderabad", "Ahmedabad", "Chandigarh"]

def get_all_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            # Core weather data
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "temp_min": data["main"]["temp_min"],
            "temp_max": data["main"]["temp_max"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            
            # Weather conditions
            "weather_main": data["weather"][0]["main"],
            "weather_desc": data["weather"][0]["description"],
            "weather_icon": data["weather"][0]["icon"],
            
            # Wind data
            "wind_speed": data["wind"]["speed"],
            "wind_deg": data["wind"].get("deg", None),
            
            # Additional info
            "cloudiness": data["clouds"]["all"],
            "visibility": data.get("visibility", None),
            "sunrise": pd.to_datetime(data["sys"]["sunrise"], unit='s'),
            "sunset": pd.to_datetime(data["sys"]["sunset"], unit='s'),
            "timezone": data["timezone"],
            
            # Location data
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
            "country": data["sys"]["country"]
        }
    else:
        print(f"Failed to fetch {city}: HTTP {response.status_code}")
        return None

# Fetch all data
all_data = []
for city in cities:
    city_data = get_all_weather_data(city)
    if city_data:
        all_data.append(city_data)

# Create DataFrame
df = pd.DataFrame(all_data)

# Plotting --> Creating Subplots 
if not df.empty:
    plt.figure(figsize=(20, 12))
    sns.set_style("whitegrid")
    
    # Plot1 : Line Plot (Temperature)
    plt.subplot(2, 2, 1) # 2 rows, 2 columns, 1st subplot
    sns.lineplot(x="city", y="temperature", data=df, marker='o', linestyle='-', color='blue')
    plt.title("Temperature by City (Line Plot)")
    plt.xlabel("City", fontweight='bold')
    plt.ylabel("Temperature (°C)", fontweight='bold')
    plt.xticks(fontsize=9, rotation=45, fontfamily='monospace')
    plt.yticks(fontsize=9)

    # Plot 2 : Bar Plot (Humidity)
    plt.subplot(2,2,2) # 2 rows, 2 columns, 2nd subplot
    b = sns.barplot(x="city", y="humidity", data=df, color='red')
    plt.title("Humidity Levels (Bar Plot)")
    plt.xlabel("City", fontweight='bold')
    plt.ylabel("Humidity", fontweight='bold')
    plt.xticks(fontsize=9, rotation=45, fontfamily='monospace')
    plt.yticks(fontsize=9)
    b.bar_label(b.containers[0], 
             label_type='edge', 
             fontsize=8, 
             padding=0, 
             fmt='%.1f%%')

    # Plot 3 : Scatter Plot (Temperature vs Humidity)
    plt.subplot(2,2,3) # 2 rows, 2 columns, 3rd subplot
    sns.scatterplot(x="temperature", y="humidity", data=df, color='green')
    plt.title("Temperature vs Humidity (Scatter Plot)")
    plt.xlabel("Temperature", fontweight='bold')
    plt.ylabel("Humidity", fontweight='bold')
    plt.xticks(fontsize=9, rotation=45, fontfamily='monospace')
    plt.yticks(fontsize=9)

    # Plot 4 : Box Plot (Wind Speed)
    plt.subplot(2,2,4) # 2 rows, 2 columns, 4th subplot
    sns.boxplot(x="city", y="wind_speed", data=df, color='yellow')
    plt.title("Wind Speed by City (Box Plot)")
    plt.xlabel("City", fontweight='bold')
    plt.ylabel("Wind Speed", fontweight='bold')
    plt.xticks(fontsize=9, rotation=45, fontfamily='monospace')
    plt.yticks(fontsize=9)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2, hspace=0.9, wspace=0.3)
    plt.show()

    # Display data table
    print("\nWeather Data:")
    print(df)
else:
    print("Failed to fetch data")
    