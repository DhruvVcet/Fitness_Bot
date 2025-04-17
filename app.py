from urllib import response
import pandas as pd
import cohere
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables 
load_dotenv()  
cohere_api_key = os.environ["COHERE_API_KEY"]
co = cohere.Client(cohere_api_key)

# --- Dataset Loading (Adapt This!) ---
def load_exercise_data(csv_file):
    df = pd.read_csv(csv_file)
    # ... potentially extract relevant columns & data cleaning ... 
    return df 

# Replace 'your_data.csv' with your actual filename
exercise_data = load_exercise_data('megaGymDataset.csv') 

# ---  Process User Queries ---
def gather_user_preferences():
    goal = st.selectbox("What's your main fitness goal?", 
                        ["Weight Loss", "Build Muscle", "Endurance", "General Fitness"])
    experience = st.radio("What's your experience level?",
                          ["Beginner", "Intermediate", "Advanced"])
    restrictions = st.checkbox("Any injuries or limitations?")
    # ... more questions can be added

    return goal, experience, restrictions

def process_query(user_input, exercise_data, user_preferences):
    # Construct a prompt or context for the chatbot
    prompt = f"""
    You are a helpful fitness assistant. Use the following data and user preferences to respond to the query.

    User preferences: {user_preferences}
    Data: {exercise_data.head().to_string()}

    Query: {user_input}
    """

    response = co.chat(
        model='command-nightly',
        message=prompt
    )
    
    return response.text


  


# --- Helper Functions (You might need to adjust) ---
def user_asks_about_exercise(query):
    # Simple keyword detection, make this smarter!
    return "describe" in query or "how to" in query 

def extract_exercise_name(query):
    # Basic extraction,  improve this with NLP techniques if needed
    return query.split("describe ")[1] 

def describe_exercise(exercise, data):
    # ... lookup  exercise in 'data' & construct a description ...
    return "Description from dataset here..." 

def craft_fitness_prompt(query, data):
    # ... construct the 'You are a fitness expert...' type prompt  ...
    return "User Query: " + query 

# --- Streamlit UI ---
st.title("Fitness Knowledge Bot")

# Gather preferences right at the start 
user_preferences = gather_user_preferences() 

user_input = st.text_input("Ask me about workouts or fitness...")

if st.button("Submit"): 
  chatbot_response = process_query(user_input, exercise_data, user_preferences)
  st.write("Chatbot:", chatbot_response) 
