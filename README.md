## Τask-Oriented Dialog System - Restaurant Reservation Chatbot

## Domain and Motivation
The chatbot operates in the restaurant booking and management domain.The motivation behind developing this chatbot is to provide users with an efficient way to discover restaurants based on their cuisine preferences,book restaurant tables, cancel reservations and get real-time weather updates for a restaurant’s location or any user-specified location
It is built using Rasa Open Source and dynamically interacts with real-world data sources, including restaurant listings stored in CSV files, booking data managed dynamically in CSV and weather APIs (OpenStreetMap & Open-Meteo) for live weather forecasts.

## Implemented Scenarios

This chatbot handles these distinct scenarios:

1. **Booking a Table** - Users can book a restaurant table by entering their information such as date, time, number of people and the name of the restaurant.
2. **Canceling a Reservation** - Users can cancel an existing reservation by providing their name.
3. **Finding Restaurants** - Users can search for restaurants based on their cuisine preference, with data fetched from a predefined restaurant database.

All described scenarios have been developed with intent recognition, slot filling and suitable responses directed at user inquiries.

## Real-world Data Integrations

1. **Restaurant Data (CSV File)** - The chatbot gets restaurant data from the CSV file named (`restaurants.csv`), which contains restaurant names, cuisines and addresses. 
2. **Booking Data (CSV File)** - All table reservations are stored and managed in (`bookings.csv.`). The users can add, view, or delete reservations dynamically.
3. **Weather API Integration** - The chatbot fetches real-time weather updates for both restaurant locations and any location specified by the user. Uses OpenStreetMap to retrieve the latitude and longitude of the location. Once geolocation data is obtained, it queries the Open-Meteo API for weather information.

## Error Handling and Robustness

The chatbot contains error handling mechanisms to handle incomplete or incorrect data:

1. Fallback messages for missing data:

 - If no restaurants are available → "Sorry, there are no restaurants available at the moment."
 - If no restaurants match the requested cuisine → "Sorry, no restaurants found for {cuisine} cuisine."
 - If no restaurants match the requested name → "Sorry, no restaurants found for {user_restaurant} restaurant."
 - If weather data cannot be fetched → "Sorry, I couldn't fetch the weather data at the moment."
 - If the address of a restaurant cannot be found →  Sorry, I couldn't fetch the address.
 - If an unexpected error occurs while fetching weather data → "An error occurred while fetching the weather data. Please try again later."
 - If a user tries to cancel a non-existent booking → "No booking found for {name}."

 2. Exception Handling in API Requests:
 - Try-except blocks for handling network failures.
 - Checks for missing or malformed API responses.

 3. File Handling for CSV Data:
 - Verifies if CSV files exist before reading/writing data.

These measures guarantee that the chatbot handles errors with grace and offers substantial feedback to users instead of silently failing.


## Setup and Installation

### Prerequisites

- Python 3.8+
- Rasa Open Source
- Anaconda (optional, for virtual environment management)

### Installation Steps

1. Open Anaconda and create a new environment through the GUI.
2. Activate the environment.
3. Install Rasa: pip install rasa
4. Train the chatbot: rasa train
5. Run the action server: rasa run actions
6. Run the chatbot: rasa shell

## Optional: Interactive Learning Mode

If you want to test and improve the chatbot dynamically, use Interactive Learning Mode: rasa interactive

## Setting up Keys, Credentials, and Environment Variables

The chatbot does not require any API keys for its current integrations.

- The **weather API (Open-Meteo)** is a free service and does not require authentication.
- The **restaurant database** and **booking database** are loaded from a local CSV file, so no database credentials are needed.

Ensure that the files `restaurants.csv` and `booking.csv` are placed in the correct directory (`data/`), before running the chatbot.


## Example Runs

### Booking a Table

**User:** "I want to book a table at a restaurant."

**Bot:** "Which restaurant do you prefer?"

**User:** "The Gourmet Table"

**Bot:** "What date would you like to book a table for?"

**User:** "22/3/25"

**Bot:** "What time should I reserve the table?"

**User:** "2:00 pm"

**Bot:** "How many people will be joining?"

**User:** "4 people"

**Bot:** "What is your name?"

**User:**  "Vasiliki"

**Bot:**  "Ok. Thanks!
Great! I have booked a table at The Gourmet Table on 22/3/25 at 2:00 pm for 4 people under the name Vasiliki.
The address of the restaurant is Ermou 50, Athens 105 63, Greece and the current temperature is 6.8°C and the wind speed is 8.4 m/s.
Your booking has been saved successfully!"


### Canceling a Reservation

**User:** "Ι want to cancel my reservation"
**Bot:** "What is your name for the reservation?"
**User:** "Vasiliki"
**Bot:** "Booking for Vasiliki has been successfully deleted."


### Finding Restaurants

**User:** "Show me Italian restaurants."
**Bot:** "Here are some Italian restaurants: The Gourmet Table, Spice & Herb Eatery, Savory Street Kitchen."

### Weather API Integration

1. Restaurant-Specific Weather

**User:** "Tell me the current weather for Gourmet Table"
**Bot:** "The current temperature is 6.8°C and the wind speed is 8.4 m/s."

2. Any Location Weather Check

**User:** "Can you check the weather in Thessaloniki,Greece?"
**Bot:**  "The current temperature is 3.8°C and the wind speed is 4.8 m/s."


## Decision-Making Approach

The chatbot follows Rasa’s default **RulePolicy, MemoizationPolicy, and TEDPolicy** to determine its responses.
- **Rule-based approach:** Handles structured interactions such as greetings, restaurant searches, and weather inquiries.
- **Form-based approach:** Ensures that all required booking information (restaurant name, date, time, number of people, customer name) is collected before confirming a reservation.
- **Memoization & TED Policy:** Helps the chatbot recall past interactions and predict responses more effectively.

These policies allow the chatbot to provide accurate and structured responses while efficiently guiding users through the reservation and information retrieval processes.

## Challenges and Solutions

### Challenge: Handling API Failures

- **Issue:** API requests for weather data sometimes fail due to network issues.
- **Solution:** Implemented a fallback response to notify the user, when data cannot be fetched.

### Challenge: Improving Intent Recognition

- **Issue:** The chatbot sometimes misclassified user intents.
- **Solution:** Tuned the training data and added more examples to improve classification accuracy.

## Future Improvements

- Implement a more robust natural language understanding (NLU) pipeline.
- Enhance the restaurant database by integrating real-time APIs for restaurant availability.
- Add support for voice-based interaction.
- Expand multi-language support for international users.

##  Presentation
- You can view the presentation here (https://drive.google.com/file/d/1UujIuYX_9b39zqjjfkwrA5JklRrVsJPd/view?usp=sharing).