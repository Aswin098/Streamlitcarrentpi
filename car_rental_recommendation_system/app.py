import streamlit as st
import requests

# Set your Gemini API key here
API_KEY = 'AIzaSyBX7FjwaAgFT4-kBWw78U8nZ_D1YkyWdWs'  # Replace with your actual API key
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

# Bootstrap-based CSS styling with black car background
st.markdown("""
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
    .main {
        background-image: url('https://wallpapercrafter.com/th800/14002-car-sunset-night-movement-speed-4k.jpg'); /* Replace with a black car image URL */
        background-size: cover;
        background-color: black;
        padding: 30px;
        color: white;
        font-family: 'Dancing Script', cursive;
        font-size: 18px;
    }
    .title {
        font-size: 60px;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.9);
    }
    .stTextArea textarea {
        font-size: 20px;
        padding: 15px;
        border-radius: 5px;
        border: 2px solid rgba(255, 255, 255, 0.7);
        background: rgba(0, 0, 0, 0.8);
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
    }
    .stButton>button {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 5px;
        border: 2px solid rgba(255, 255, 255, 0.7);
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        transition: none;
    }
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.2);
        color: white;
    }
    .stAlert {
        font-size: 18px;
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 5px;
    }
    .stSpinner {
        color: rgba(0, 123, 255, 0.7);
    }
    </style>
    """, unsafe_allow_html=True)

def generate_content(prompt):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'contents': [{
            'parts': [{
                'text': prompt
            }]
        }]
    }
    
    response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=data)
    
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.json())

    if response.status_code == 200:
        response_data = response.json()
        if 'candidates' in response_data and len(response_data['candidates']) > 0:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        else:
            return 'No candidates found in response.'
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    st.markdown("<div class='title'>CAR for me</div>", unsafe_allow_html=True)

    st.write("Welcome to the Car Rental Chatbot! Please answer the questions below:")
    
    # Collect user inputs through text boxes
    city = st.text_input("Where are you going? (City, state, or region):")
    rental_duration = st.text_input("How long will you be renting the car for? (Days or weeks):")
    road_type = st.text_input("What kind of roads will you be driving on? (Highway, city, off-road):")
    
    travelers = st.text_input("How many people are you traveling with?")
    luggage_space = st.text_input("Do you need a lot of luggage space? (Yes/No):")
    budget_style = st.text_input("Are you on a budget or willing to spend more for comfort/features? (Budget/Comfort):")
    
    transmission = st.text_input("Do you prefer a manual or automatic transmission?")
    air_conditioning = st.text_input("Do you need a car with air conditioning? (Yes/No):")
    fuel_efficient = st.text_input("Are you looking for a fuel-efficient car? (Yes/No):")
    
    budget = st.text_input("What is your budget per day in rupees?")
    
    if st.button("Generate Recommendations"):
        if all([city, rental_duration, road_type, travelers, luggage_space, budget_style, 
                 transmission, air_conditioning, fuel_efficient, budget]):
            with st.spinner("Generating recommendations..."):
                # Create the prompt based on user inputs
                prompt = (
                    f"Please provide car recommendations based on the following details:\n\n"
                    f"1. Trip Details:\n"
                    f"   - City/Region: {city}\n"
                    f"   - Rental Duration: {rental_duration}\n"
                    f"   - Road Type: {road_type}\n\n"
                    f"2. Travel Style:\n"
                    f"   - Number of Travelers: {travelers}\n"
                    f"   - Luggage Space Needed: {luggage_space}\n"
                    f"   - Budget Style: {budget_style}\n\n"
                    f"3. Driving Preferences:\n"
                    f"   - Transmission: {transmission}\n"
                    f"   - Air Conditioning: {air_conditioning}\n"
                    f"   - Fuel Efficiency: {fuel_efficient}\n\n"
                    f"4. Budget:\n"
                    f"   - Budget per Day: {budget} INR\n"
                )
                
                content = generate_content(prompt)
                st.success("Recommendations generated successfully!")
                st.write(content)
        else:
            st.warning("Please fill in all the details.")

if __name__ == "__main__":
    main()
