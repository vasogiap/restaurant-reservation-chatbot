# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

#Importing necessary libraries
import requests
import pandas as pd

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset

#Reset All Slots
class ActionResetAllSlots(Action):
    def name(self) -> Text:
        return "action_reset_all_slots"

    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]

#Delete a Booking
class ActionDeleteBooking(Action):
    def name(self):
        return "action_delete_booking"

    def run(self, dispatcher, tracker, domain):
        #Extract name from user input
        name = tracker.get_slot("cancel_customer_name")
        #Define CSV file path
        file_path = "data/bookings.csv"

        try:
            #Load the CSV file
            df = pd.read_csv(file_path, sep=";", encoding="utf-8")

            #Check if the name exists
            if name not in df["Name"].values:
                dispatcher.utter_message(text=f"No booking found for {name}.")
                return []

            #Remove the booking
            df = df[df["Name"] != name]

            #Save the updated CSV file
            df.to_csv(file_path, sep=";", index=False, encoding="utf-8")

            dispatcher.utter_message(text=f"Booking for {name} has been successfully deleted.")

        except FileNotFoundError:
            dispatcher.utter_message(text="No bookings found.")

        return []

#Save a New Booking
class ActionSaveBooking(Action):
    def name(self) -> Text:
        return "action_save_booking"

    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        restaurant = tracker.get_slot("restaurant_name")
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        people = tracker.get_slot("people")
        name = tracker.get_slot("customer_name")

        #Define the CSV file path
        file_path = "data/bookings.csv"
        #Create a new DataFrame with the new booking
        new_booking = pd.DataFrame(
            [[restaurant, date, time, people, name]],
            columns=["Restaurant", "Date", "Time", "People", "Name"]
        )

        try:
            #Load existing CSV file if it exists
            existing_data = pd.read_csv(file_path, sep=";", encoding="utf-8")

            #Append new data
            updated_data = pd.concat([existing_data, new_booking], ignore_index=True)
        except FileNotFoundError:
            #If file does not exist, create a new one
            updated_data = new_booking

        #Save the updated CSV file
        updated_data.to_csv(file_path, sep=";", index=False, encoding="utf-8")

        dispatcher.utter_message(text="Your booking has been saved successfully!")

        return []
    
#List All Available Restaurants
class ActionListAvailableRestaurants(Action):
    def name(self) -> Text:
        return "action_list_available_restaurants"

    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_cuisine = tracker.get_slot("cuisine")
        
        #Load restaurant data from CSV
        file_path = "data/restaurants.csv"
        df = pd.read_csv(file_path, sep=";")

        if df.empty:
            response = "Sorry, there are no restaurants available at the moment."
        else:
            restaurant_list = "\n".join(
                [f"{row['name']} - {row['cuisine']} - {row['address']}" for _, row in df.iterrows()]
            )
            response = f"Here are all available restaurants:\n{restaurant_list}"

        dispatcher.utter_message(text=response)

        return []

#Find Restaurants by Cuisine
class ActionFindRestaurants(Action):
    def name(self):
        return "action_find_restaurants"

    def run(self, dispatcher, tracker, domain):
        #Get the user's cuisine preference from a slot
        user_cuisine = tracker.get_slot("cuisine")
        
        #Load restaurant data from CSV
        file_path = "data/restaurants.csv"
        df = pd.read_csv(file_path, sep=";")

        #Filter restaurants based on cuisine
        filtered_df = df[df["cuisine"].str.lower() == user_cuisine.lower()]

        if filtered_df.empty:
            response = f"Sorry, no restaurants found for {user_cuisine} cuisine."
        else:
            restaurant_list = "\n".join(filtered_df["name"].tolist())
            response = f"Here are some {user_cuisine} restaurants:\n{restaurant_list}"

        dispatcher.utter_message(text=response)
        return []
    
#Fetch Weather for a Restaurant
class ActionFetchWeather(Action):
    def name(self) -> Text:
        return "action_fetch_weather"

    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_restaurant = tracker.get_slot("restaurant_name")
        #Load restaurant data from CSV
        file_path = "data/restaurants.csv"
        df = pd.read_csv(file_path, sep=";")

        #Filter restaurants based on cuisine
        filtered_df = df[df["name"].str.contains(user_restaurant, case=False, na=False)]

        if filtered_df.empty:
            response = f"Sorry, no restaurants found for {user_restaurant} restaurant."
            return []
        
        else:
            address =  filtered_df["address"].iloc[0]
     
        #address = "Syntagma Square, Athens 105 57, Greece"
        url = f"https://nominatim.openstreetmap.org/search?q={address}&limit=1&format=json"

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()

        #Extract latitude and longitude if data is available
        if data:
            lat = data[0].get("lat", "N/A")
            lon = data[0].get("lon", "N/A")
                
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                current_weather = data.get("current_weather", {})
                temperature = current_weather.get("temperature", "N/A")
                wind_speed = current_weather.get("windspeed", "N/A")

                #Respond to the user
                dispatcher.utter_message(
                    text=f"The address of the restaurant is {address} and the current temperature is {temperature}°C and the wind speed is {wind_speed} m/s."
                )
            else:
                dispatcher.utter_message(
                    text ="Sorry, I couldn't fetch the weather data at the moment."
                )
        except Exception as e:
            dispatcher.utter_message(
                text ="An error occurred while fetching the weather data. Please try again later."
            )

        return []

#Fetch Weather for Any Location
class ActionFetchWeather(Action):
    def name(self) -> Text:
        return "action_fetch_weather_for_place"

    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_place = tracker.get_slot("place")
        
        url = f"https://nominatim.openstreetmap.org/search?q={user_place}&limit=1&format=json"

        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                data = response.json()
                lat = data[0].get("lat", "N/A")
                lon = data[0].get("lon", "N/A")               
                
            else:
                dispatcher.utter_message(
                    text ="Sorry, I couldn't fetch the address."
                )
        except Exception as e:
            dispatcher.utter_message(
                text ="An error occurred while fetching the address data. Please try again later."
            )
        

        #Extract latitude and longitude if data is available
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                current_weather = data.get("current_weather", {})
                temperature = current_weather.get("temperature", "N/A")
                wind_speed = current_weather.get("windspeed", "N/A")

                #Respond to the user
                dispatcher.utter_message(
                    text=f"The current temperature is {temperature}°C and the wind speed is {wind_speed} m/s."
                )
            else:
                dispatcher.utter_message(
                    text ="Sorry, I couldn't fetch the weather data at the moment."
                )
        except Exception as e:
            dispatcher.utter_message(
                text =f"An error occurred while fetching the weather data for {user_place}. Please try again later."
            )

        return []

#Submit Booking
class ActionSubmitBooking(Action):
    def name(self):
        return "action_submit_booking"

    def run(self, dispatcher, tracker, domain):
        restaurant_name = tracker.get_slot("restaurant_name")
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        people = tracker.get_slot("people")
        customer_name = tracker.get_slot("customer_name")

        #Save booking info (e.g., in a database or API)
        booking_details = f"Booking confirmed: {restaurant_name}, {date}, {time}, for {people} people, under {customer_name}."

        dispatcher.utter_message(text="Your booking has been recorded.")
        dispatcher.utter_message(text=booking_details)

        return []

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
