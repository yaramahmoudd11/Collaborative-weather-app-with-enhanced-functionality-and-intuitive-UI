# Importing necessary libraries
import requests
import random
import tkinter as tk
from tkinter import Label, Button, messagebox, ttk, simpledialog
import os
from datetime import datetime
from plyer import notification

# Setting up the OpenWeatherMap API key and initializing variables
API_KEY = '4bea4fecede16b4b3d4b30ef0a1dab3e'
score = 0
game_round = 1

# Function to create the main window
def window():
    # Creating the main Tkinter window
    r = tk.Tk()
    r.title("Weather App")
    r.geometry("450x250")

    # Creating and configuring labels for the window
    title = Label(r, text="Weather application", font='times 18 bold', bg='#625FFF')
    title.pack()
    r.configure(bg='#C1D9FB')

    choice = Label(r, text="Choose option:\n", font='times 14 bold underline', bg='#C1D9FB')
    choice.pack()

    # Creating a frame for the buttons with a border
    data_border = tk.Frame(r, highlightbackground="black", highlightthickness=2, bd=0)

    # Button for entertainment menu
    entertainment_button = tk.Button(data_border, text="Entertainment", font='times 12', command=entertainment_menu, width=17,
                                     height=2)
    entertainment_button.pack()
    entertainment_button.pack_propagate(0)

    # Button for weather data menu
    data = tk.Button(data_border, text="Weather Data", font='times 12', command=data_menu, width=17, height=2)
    data.pack()
    data.pack_propagate(0)

    # Packing the frame with buttons
    data_border.pack()

    # Running the Tkinter main loop
    r.mainloop()
#weather app first menu shap
def entertainment_menu():
    # Using global variables to maintain state across function calls
    global game_round, score
    game_round = 1  # Resetting game round to 1

    # Creating a new top-level window for the Entertainment Menu
    entertainment = tk.Toplevel()
    entertainment.title("Entertainment Menu")
    entertainment.geometry("450x250")

    # Creating and configuring labels for the entertainment menu window
    ent_title = Label(entertainment, text="Entertainment menu", font='times 18 bold', bg='#625FFF')
    ent_title.pack()

    choice = Label(entertainment, text="Choose option:\n", font='times 14 bold underline', bg='#C1D9FB')
    choice.pack()

    # Creating a frame for the buttons with a border
    data_border = tk.Frame(entertainment, highlightbackground="black", highlightthickness=2, bd=0)
    entertainment.configure(bg='#C1D9FB')

    # Button for the Encoding/Decoding Game
    game = Button(entertainment, text="Encoding/Decoding\nGame", font='times 12',
                  command=weather_encoding_decoding_game, width=17, height=2)
    game.pack()
    game.pack_propagate(0)

    # Button for the Weather Quiz
    quiz = Button(entertainment, text="Weather Quiz", font='times 12', command=weather_quiz, width=17, height=2)
    quiz.pack()
    quiz.pack_propagate(0)

    # Packing the frame with buttons
    data_border.pack()

    # Running the Tkinter main loop for the entertainment menu window
    entertainment.mainloop()
def entertainment_menu():
    # Using global variables to maintain state across function calls
    global game_round, score
    game_round = 1  # Resetting game round to 1

    # Creating a new top-level window for the Entertainment Menu
    entertainment = tk.Toplevel()
    entertainment.title("Entertainment Menu")
    entertainment.geometry("450x250")

    # Creating and configuring labels for the entertainment menu window
    ent_title = Label(entertainment, text="Entertainment menu", font='times 18 bold', bg='#625FFF')
    ent_title.pack()

    choice = Label(entertainment, text="Choose option:\n", font='times 14 bold underline', bg='#C1D9FB')
    choice.pack()

    # Creating a frame for the buttons with a border
    data_border = tk.Frame(entertainment, highlightbackground="black", highlightthickness=2, bd=0)
    entertainment.configure(bg='#C1D9FB')

    # Button for the Encoding/Decoding Game
    game = Button(entertainment, text="Encoding/Decoding\nGame", font='times 12',
                  command=weather_encoding_decoding_game, width=17, height=2)
    game.pack()
    game.pack_propagate(0)

    # Button for the Weather Quiz
    quiz = Button(entertainment, text="Weather Quiz", font='times 12', command=weather_quiz, width=17, height=2)
    quiz.pack()
    quiz.pack_propagate(0)

    # Packing the frame with buttons
    data_border.pack()

    # Running the Tkinter main loop for the entertainment menu window
    entertainment.mainloop()

# Function to retrieve and display weather data for a specific city
def data_menu():
    # Prompt the user to enter a city
    city = simpledialog.askstring("Weather Data", "Enter city:")

    if city:
        # Check if the city is a special keyword (e.g., "sunrise" or "sunset")
        if city.lower() == "sunset" or city.lower() == "sunrise":
            time_type = "sunrise" if city.lower() == "sunrise" else "sunset"
            time = get_sun_time(city, time_type)

            # Display the sunrise or sunset time
            if time is not None:
                messagebox.showinfo("Sun Time", f"{city.capitalize()} time: {time}")
            else:
                messagebox.showerror("Error", f"Unable to fetch {city} time.")
        else:
            try:
                # Retrieve weather data from the OpenWeatherMap API
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    # Extract relevant weather information from the API response
                    temperature = data['main']['temp']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    weather_description = data['weather'][0]['description']

                    # Prepare a formatted text with weather information
                    result_text = f"Weather in {city}:\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nDescription: {weather_description}"

                    # Display the result to the user
                    messagebox.showinfo("Weather Data", result_text)

                    # Trigger a desktop notification with temperature and weather description
                    getnotification(temperature, weather_description)

                    # Save the data to a text file
                    save_data_to_file(city, "general", None, result_text)

                    # Ask the user if they want more weather data
                    response = messagebox.askyesno("Weather Data", "Do you want more weather data?")

                    if response:
                        data_options(city)
                else:
                    messagebox.showerror("Error", f"Unable to fetch weather data for {city}")

            except requests.RequestException:
                messagebox.showerror("Error", "Unable to connect to the weather API")

# Function to start the Encoding/Decoding Game
def weather_encoding_decoding_game():
    # Using global variables to maintain state across function calls
    global game_round, score

    # Prompt the user to enter their username
    username = simpledialog.askstring("Game Start", "Enter your username:")

    if username:
        filename = f"{username}_encoding_decoding_game_score.txt"

    # List of words for the Encoding/Decoding Game
    words = ["temperature", "humidity", "wind", "clouds", "rain", "snow", "thunder", "lightning", "storm", "sunset",
             "sunrise", "fog", "precipitation", "blizzard"]

    # Choose a random word and shuffle its letters
    chosen_word = random.choice(words)
    shuffled_word = ''.join(random.sample(chosen_word, len(chosen_word)))

    # Display the shuffled word to the user and prompt for their guess
    messagebox.showinfo("Python Weather Game", f"Shuffled word: {shuffled_word}")
    user_guess = simpledialog.askstring("Python Weather Game", "Your guess:")

    # Check if the user's guess is correct and update the score
    if user_guess and user_guess.lower() == chosen_word:
        messagebox.showinfo("Python Weather Game", "Correct! You decoded the word.")
        score += 1
    elif user_guess:
        messagebox.showinfo("Python Weather Game", f"Wrong! The correct word was: {chosen_word}")

    # Ask the user if they want to play again
    response = messagebox.askyesno("Python Weather Game", f"Your score: {score}\nDo you want to play again?")

    if response:
        # If the user wants to play again, increment the game round and restart the game
        game_round += 1
        weather_encoding_decoding_game()
    else:
        # Save the user's final score and end the game
        save_user_score("encoding_decoding_game", score)


# Function to conduct a weather quiz with multiple-choice questions
def weather_quiz():
    # List of quiz questions with options and correct answers
    questions = [
        {"question": "What is the unit of temperature in the metric system?",
         "options": ["Celsius", "Fahrenheit", "Kelvin"], "correct": "Celsius"},
        {"question": "Which instrument is used to measure wind speed?",
         "options": ["Hygrometer", "Barometer", "Anemometer"], "correct": "Anemometer"},
        {"question": "A rainbow is a spectrum of light that appears when the Sun shines onto water droplets in the air",
         "options": ["True", "False", "0"], "correct": "True"},
        {"question": "What is the driest desert on Earth",
         "options": ["the Sahara", "the Kalahari", "the Atacama"], "correct": "the Atacama"},
        {"question": "How many points does a snowflake have?",
         "options": ["4", "6", "8"], "correct": "6"}
    ]

    global score
    for question in questions:
        # Prompt the user for their answer to each question
        user_answer = simpledialog.askinteger("Weather Quiz",
                                              f"{question['question']}\n\nOptions:\n1. {question['options'][0]}\n2. {question['options'][1]}\n3. {question['options'][2]}\n\nYour answer (enter the option number):")
        # Check if the user's answer is correct and update the score
        if user_answer and question["options"][user_answer - 1] == question["correct"]:
            messagebox.showinfo("Weather Quiz", "Correct!")
            score += 1
        elif user_answer:
            messagebox.showinfo("Weather Quiz", f"Wrong! The correct answer is: {question['correct']}")

    # Save the user's quiz score and display the final score
    save_user_score("quiz", score)
    messagebox.showinfo("Weather Quiz", f"Your final score: {score}")

# Function to read a user's score from a file based on the game type

def read_user_score(game_type):
    username = simpledialog.askstring("Game Start", "Enter your username:")
    if username:
        filename = f"{username}_{game_type}_score.txt"

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return int(file.read())
        else:
            return 0


def save_user_score(game_type, new_score):
    username = simpledialog.askstring("Game Over", "Enter your username:")
    if username:
        filename = f"{username}_{game_type}_score.txt"

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                old_score = int(file.read())
                score = old_score + new_score

            messagebox.showinfo("Game Over", f"Welcome back, {username}!\nYour old score: {old_score}\nNew score: {score}")

            with open(filename, 'w') as file:
                file.write(str(score))
        else:
            with open(filename, 'w') as file:
                file.write(str(new_score))
            messagebox.showinfo("Game Over", f"Welcome, {username}!\nYour first score: {new_score}")



# Function to retrieve and display weather data for a specific city
def get_weather_data(city):
    try:
        # Construct the API URL for weather data
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Check if the API response is successful (status code 200)
        if response.status_code == 200:
            # Extract relevant weather information from the API response
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            weather_description = data['weather'][0]['description']

            # Prepare a formatted text with weather information
            result_text = f"Weather in {city}:\nTemperature: {temperature}°C\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nDescription: {weather_description}"

            # Trigger a desktop notification with temperature and weather description
            getnotification(temperature, weather_description)

            # Display the result to the user
            messagebox.showinfo("Weather Data", result_text)

            # Save the data to a text file based on user options
            save_data_to_file(city, "general", None, result_text)

            # Ask the user if they want more weather data
            response = messagebox.askyesno("Weather Data", "Do you want more weather data?")

            if response:
                data_options(city)
        else:
            # Display an error message if unable to fetch weather data
            messagebox.showerror("Error", f"Unable to fetch weather data for {city}")

    except requests.RequestException:
        # Display an error message if unable to connect to the weather API
        messagebox.showerror("Error", "Unable to connect to the weather API")

# Function to save weather data to a text file based on user options
def save_data_to_file(city, option, columns, data):
    filename = f"{city}_{option}_data.txt"
    with open(filename, 'a') as file:
        if option in ["temperature_table", "wind_table"]:
            # Save temperature or wind data in tabular format
            file.write(f"{option.capitalize()} for {city}\n")
            file.write("\t".join(columns) + "\n")
            for unit, value in data.items():
                file.write(f"{unit}\t{value}\n")
        elif option in ["sunrise_time", "sunset_time"]:
            # Save sunrise or sunset time for the city
            file.write(f"{option.capitalize()} in {city}\n")
            file.write(f"{data}\n")
        elif option == "compare_data":
            # Save comparison data between cities
            file.write(f"Initial City: {city}\n")
            file.write("\t".join(columns) + "\n")
            for row in data:
                file.write("\t".join(map(str, row)) + "\n")
        else:
            # Save general weather data
            file.write(f"Weather Data for {city}\n")
            file.write(data)
# Function to display additional weather data options for a specific city
def data_options(city):
    # Create a new top-level window for additional weather data options
    data = tk.Toplevel()
    data.geometry("450x375")
    data.title("Additional Weather Data")
    data.configure(bg='#C1D9FB')

    # Create and configure labels for the window
    title = tk.Label(data, text="Other Data", font='times 18 bold', bg='#625FFF')
    title.pack()

    choice = tk.Label(data, text="Choose option:\n", font='times 14 bold underline', bg='#C1D9FB')
    choice.pack()

    # Create buttons for various additional weather data options
    temperature = tk.Button(data, text="Temperature Table", command=lambda: temperature_table(city), font="times 10", width=17,
                            height=2)
    temperature.pack()

    wind = tk.Button(data, text="Wind Speed Table", command=lambda: wind_table(city), font="times 10", width=17, height=2)
    wind.pack()

    sunset_button = tk.Button(data, text="Sunset Time", command=lambda: show_sun_time(city, "sunset"), font="times 10",
                              width=17, height=2)
    sunset_button.pack()

    sunrise_button = tk.Button(data, text="Sunrise Time", command=lambda: show_sun_time(city, "sunrise"), font="times 10",
                               width=17, height=2)
    sunrise_button.pack()

    compare_button = tk.Button(data, text="Compare", command=lambda: compare_weather_data_option(city), font="times 10",
                               width=17, height=2)
    compare_button.pack()

    forecast_button = tk.Button(data, text="Weather Forecast", command=lambda: weather_forecast_option(city),
                                font="times 10", width=17, height=2)
    forecast_button.pack()

    # Run the Tkinter main loop for the data options window
    data.mainloop()
# Function to display weather forecast for a specific city over the next 'num_days' days
def weather_forecast_option(city):
    try:
        # Prompt the user to enter the number of days for the forecast
        num_days = simpledialog.askinteger("Weather Forecast", "Enter the number of days for the forecast:")

        # Check if the entered number of days is valid
        if num_days is not None and num_days > 0:
            # Construct the API URL for weather forecast
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            forecast_data = response.json()

            # Check if the API response is successful (status code 200)
            if response.status_code == 200:
                forecast_list = forecast_data['list']

                # Group forecast data by date
                grouped_forecast = {}
                for forecast in forecast_list:
                    date = forecast['dt_txt'].split(' ')[0]
                    if date not in grouped_forecast:
                        grouped_forecast[date] = []
                    grouped_forecast[date].append(forecast)

                # Create a new window to display the weather forecast table
                forecast_table = tk.Toplevel()
                forecast_table.title(f"Weather Forecast for {city} - Next {num_days} Days")

                columns = ('Date', 'Temperature (°C)', 'Humidity (%)', 'Description')
                tree = ttk.Treeview(forecast_table, columns=columns, show='headings')
                tree.heading('Date', text='Date')
                tree.heading('Temperature (°C)', text='Temperature (°C)')
                tree.heading('Humidity (%)', text='Humidity (%)')
                tree.heading('Description', text='Description')

                # Populate the forecast table with average values for each date
                for date, daily_forecast in list(grouped_forecast.items())[:num_days]:
                    avg_temperature = sum(forecast['main']['temp'] for forecast in daily_forecast) / len(daily_forecast)
                    avg_humidity = sum(forecast['main']['humidity'] for forecast in daily_forecast) / len(daily_forecast)
                    description = daily_forecast[0]['weather'][0]['description']

                    tree.insert("", "end", values=(date, round(avg_temperature, 2), round(avg_humidity, 2), description))

                tree.pack()

                # Run the Tkinter main loop for the forecast table window
                forecast_table.mainloop()

                # Save the forecast data to a text file
                save_forecast_data_to_file(city, num_days, columns, grouped_forecast)
            else:
                messagebox.showerror("Error", f"Unable to fetch weather forecast for {city}")
        else:
            # Display a message for an invalid number of days
            messagebox.showinfo("Weather Forecast", "Invalid number of days. Please enter a positive integer.")

    except requests.RequestException:
        # Display an error message if unable to connect to the weather API
        messagebox.showerror("Error", "Unable to connect to the weather API")

# Function to save weather forecast data to a text file
def save_forecast_data_to_file(city, num_days, columns, grouped_forecast):
    filename = f"{city}_forecast_data.txt"
    with open(filename, 'w') as file:
        file.write(f"Weather Forecast for {city} - Next {num_days} Days\n")
        file.write("\t".join(columns) + "\n")
        for date, daily_forecast in list(grouped_forecast.items())[:num_days]:
            avg_temperature = sum(forecast['main']['temp'] for forecast in daily_forecast) / len(daily_forecast)
            avg_humidity = sum(forecast['main']['humidity'] for forecast in daily_forecast) / len(daily_forecast)
            description = daily_forecast[0]['weather'][0]['description']
            file.write(f"{date}\t{round(avg_temperature, 2)}\t{round(avg_humidity, 2)}\t{description}\n")

# Function to initiate a comparison of weather data for multiple cities
def compare_weather_data_option(initial_city):
    try:
        # Prompt the user to enter the number of cities for comparison
        num_cities = simpledialog.askinteger("Compare Weather Data", "How many cities do you want to add?")

        # Check if the entered number of cities is valid
        if num_cities is not None and num_cities > 0:
            cities = [initial_city]
            # Prompt the user to enter names of cities for comparison
            for i in range(num_cities):
                city = simpledialog.askstring("Compare Weather Data", f"Enter city {i + 1}:")
                if city:
                    cities.append(city)

            # Initialize an empty list to store weather data for each city
            data = []
            headers = ["City", "Temperature (°C)", "Humidity (%)", "Wind Speed (m/s)", "Description"]

            # Fetch weather data for each city and append it to the data list
            for city in cities:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                weather_data = response.json()

                # Check if the API response is successful (status code 200)
                if response.status_code == 200:
                    temperature = weather_data['main']['temp']
                    humidity = weather_data['main']['humidity']
                    wind_speed = weather_data['wind']['speed']
                    description = weather_data['weather'][0]['description']
                    data.append([city, temperature, humidity, wind_speed, description])
                else:
                    # If fetching data fails, append placeholders (N/A) to the data list
                    data.append([city, "N/A", "N/A", "N/A", "N/A"])

            # Create and display a comparison table for weather data
            compare_table(data, headers)

            # Highlight the row with the highest temperature in the comparison table
            highlight_highest_temperature(tree)

            # Save the comparison data to a text file
            save_compare_data_to_file(initial_city, cities, headers, data)
        else:
            # Display a message for an invalid number of cities
            messagebox.showinfo("Compare Weather Data", "Invalid number of cities. Please enter a positive integer.")

    except requests.RequestException:
        # Display an error message if unable to connect to the weather API
        messagebox.showerror("Error", "Unable to connect to the weather API")

# Function to save comparison data to a text file
def save_compare_data_to_file(initial_city, cities, headers, data):
    filename = f"{initial_city}_compare_data.txt"
    with open(filename, 'w') as file:
        file.write(f"Initial City: {initial_city}\n")
        file.write("\t".join(headers) + "\n")
        for row in data:
            file.write("\t".join(map(str, row)) + "\n")


# Function to create a comparison table for weather data and display it in a new window
def compare_table(data, headers):
    # Create a new window for the comparison table
    compare_table = tk.Toplevel()
    compare_table.title("Weather Data Comparison")

    # Create a Treeview widget for the comparison table with specified columns
    tree = ttk.Treeview(compare_table, columns=headers, show='headings')
    for header in headers:
        tree.heading(header, text=header)

    # Configure tags for highlighting specific conditions in the comparison table
    tree.tag_configure('high_temperature', background='red')
    tree.tag_configure('about_to_rain', background='blue')
    tree.tag_configure('high_humidity', background='lightblue')

    highest_temp_item = None
    highest_temp = -float('inf')

    # Populate the comparison table with data and apply tags based on conditions
    for row in data:
        item_id = tree.insert("", "end", values=row)

        temperature = float(row[1])
        humidity = float(row[2])
        description = row[4].lower()

        # Highlight the row with the highest temperature
        if temperature > highest_temp:
            highest_temp = temperature
            highest_temp_item = item_id

        # Apply tags based on specific weather conditions
        if 'rain' in description:
            tree.item(item_id, tags=('about_to_rain',))

        if humidity > 70:
            tree.item(item_id, tags=('high_humidity',))

    # Highlight the row with the highest temperature using the 'high_temperature' tag
    if highest_temp_item:
        tree.item(highest_temp_item, tags=('high_temperature',))

    # Set column properties and pack the Treeview widget
    for idx, header in enumerate(headers):
        tree.column(idx, anchor="center", width=100)

    tree.pack()

    # Run the Tkinter main loop for the comparison table window
    compare_table.mainloop()

# Function to highlight the row with the highest temperature in a Treeview widget
def highlight_highest_temperature(tree):
    highest_temp_item = None
    highest_temp = -float('inf')

    # Iterate through items in the Treeview to find the highest temperature
    for item_id in tree.get_children():
        temperature = float(tree.item(item_id, 'values')[1])
        if temperature > highest_temp:
            highest_temp = temperature
            highest_temp_item = item_id

    # Highlight the row with the highest temperature using the 'high_temperature' tag
    if highest_temp_item:
        tree.tag_configure('high_temperature', background='red')
        tree.tag_add('high_temperature', highest_temp_item)

# Function to create and display a temperature table for a specific city
def temperature_table(city):
    # Fetch temperature data in different units for the specified city
    temperature_data = temperature_in_units(city)

    # Check if temperature data is available
    if temperature_data:
        # Create a new window for the temperature table
        temperature_table = tk.Toplevel()
        temperature_table.title(f"Temperature Table for {city}")

        # Define columns for the temperature table
        columns = ('Unit', 'Temperature (°C)')
        tree = ttk.Treeview(temperature_table, columns=columns, show='headings')
        tree.heading('Unit', text='Unit')
        tree.heading('Temperature (°C)', text='Temperature (°C)')

        # Populate the temperature table with data
        for unit, temperature in temperature_data.items():
            tree.insert("", "end", values=(unit, temperature))

        # Pack the Treeview widget
        tree.pack()

        # Save temperature data to a text file
        save_data_to_file(city, "temperature_table", columns, temperature_data)

        # Run the Tkinter main loop for the temperature table window
        temperature_table.mainloop()

# Function to create and display a wind speed table for a specific city
def wind_table(city):
    # Fetch wind speed data in different units for the specified city
    wind_data = wind_speed_in_units(city)

    # Check if wind speed data is available
    if wind_data:
        # Create a new window for the wind speed table
        wind_table = tk.Toplevel()
        wind_table.title(f"Wind Speed Table for {city}")

        # Define columns for the wind speed table
        columns = ('Unit', 'Wind Speed (m/s)')
        tree = ttk.Treeview(wind_table, columns=columns, show='headings')
        tree.heading('Unit', text='Unit')
        tree.heading('Wind Speed (m/s)', text='Wind Speed (m/s)')

        # Populate the wind speed table with data
        for unit, wind_speed in wind_data.items():
            tree.insert("", "end", values=(unit, wind_speed))

        # Pack the Treeview widget
        tree.pack()

        # Save wind speed data to a text file
        save_data_to_file(city, "wind_table", columns, wind_data)

        # Run the Tkinter main loop for the wind speed table window
        wind_table.mainloop()

# Function to display sunrise or sunset time for a specific city
def show_sun_time(city, time_type):
    # Fetch sunrise or sunset time for the specified city
    time = get_sun_time(city, time_type)
    if time is not None:
        # Display the sunrise or sunset time in a messagebox
        messagebox.showinfo("Sun Time", f"{time_type.capitalize()} time in {city}: {time}")

        # Save sunrise or sunset time to a text file
        save_data_to_file(city, f"{time_type}_time", time_type.capitalize(), time)
    else:
        # Display an error message if unable to fetch sunrise or sunset time
        messagebox.showerror("Error", f"Unable to fetch {time_type} time.")

# Function to fetch temperature data in different units for a specific city
def temperature_in_units(city):
    try:
        # Make an API request to fetch weather data for the specified city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Check if the API request was successful
        if response.status_code == 200:
            # Extract temperature in Celsius from the API response
            celsius = data['main']['temp']

            # Convert temperature to Fahrenheit and Kelvin
            fahrenheit = (celsius * 9 / 5) + 32
            temperature_kelvin = celsius + 273.15

            # Return temperature data in different units
            return {
                'celsius': celsius,
                'fahrenheit': fahrenheit,
                'kelvin': temperature_kelvin,
            }
        else:
            # Return None if unable to fetch weather data
            return None
    except requests.RequestException:
        # Return None if there is a request exception (e.g., unable to connect to the API)
        return None

# Function to fetch wind speed data in different units for a specific city
def wind_speed_in_units(city):
    try:
        # Make an API request to fetch weather data for the specified city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Check if the API request was successful
        if response.status_code == 200:
            # Extract wind speed in meters per second from the API response
            wind_speed_mps = data['wind']['speed']

            # Convert wind speed to kilometers per hour and miles per hour
            wind_speed_kmph = wind_speed_mps * 3.6
            wind_speed_mph = wind_speed_kmph / 1.60934

            # Return wind speed data in different units
            return {
                'mps': wind_speed_mps,
                'kmph': wind_speed_kmph,
                'mph': wind_speed_mph
            }
        else:
            # Return None if unable to fetch weather data
            return None
    except requests.RequestException:
        # Return None if there is a request exception (e.g., unable to connect to the API)
        return None

# Function to fetch sunrise or sunset time for a specific city
def get_sun_time(city, time_type):
    try:
        # Make an API request to fetch weather data for the specified city
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        # Check if the API request was successful
        if response.status_code == 200:
            # Extract sunrise or sunset timestamp from the API response
            if time_type == "sunrise":
                sunrise_timestamp = data['sys']['sunrise']
                sunrise_time = datetime.utcfromtimestamp(sunrise_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                return sunrise_time
            elif time_type == "sunset":
                sunset_timestamp = data['sys']['sunset']
                sunset_time = datetime.utcfromtimestamp(sunset_timestamp).strftime('%Y-%m-%d %H:%M:%S')
                return sunset_time
            else:
                return None
        else:
            # Return None if unable to fetch weather data
            return None
    except requests.RequestException:
        # Return None if there is a request exception (e.g., unable to connect to the API)
        return None

# Function to display system notifications based on temperature and weather description
def getnotification(temperature, weather_description):
    title = "Temperature Notification"

    # Determine the message based on temperature and weather description
    if temperature < 0:
        message = "Oh seems like it's cold today, better grab a jacket!"
    elif temperature < 23:
        message = "The temperature is chilly today, best time to be outside and enjoy it"
    elif temperature > 23:
        message = "It's hot today, best time for refreshing drinks"
    if "rain" in weather_description.lower():
        message = "It's raining outside better grab a coat"
    if "snow" in weather_description.lower():
        message = "Looks like it's snowing, time to build a snowman!"

    # Display the notification with the determined title and message
    notification.notify(title=title, message=message, app_icon=None, timeout=10)
