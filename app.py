# Package imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import anthropic

# Loading classifier model
with open('mental_health_classifier.pkl', 'rb') as f:
    mental_health_classifier = pickle.load(f)

# Loading Claude AI
anthropic_key = st.secrets["anthropic_key"]
anthropic = anthropic.Anthropic(api_key=anthropic_key)

# Loading data
sample_data = pd.read_csv('database_sample.csv')

# Headers for all pages
st.title("MindTheAge")
st.markdown('Bridging the gap between older folks and mental healthcare.')

# Initialization of session states
if 'email' not in st.session_state:
    st.session_state['email'] = ''

def login():
    st.header("Login with your email")
    email = st.text_input("Email", placeholder='Type your email here')
    login_button = st.button("Login", type='primary')

    # Need to add email in order to get through
    if email == "" and login_button:
        st.error("Please enter a valid email address.")
    elif login_button:
        if email in st.secrets["registered_users"]:
            st.session_state['logged_in'] = True
            st.session_state['active_page'] = "Home"
            st.session_state['email'] = email  
            st.rerun()
        else:
            st.error("Email not found. Please register first.")

# Function for the home page (only accessible if logged in)
def home():
    email = st.session_state['email']  # Access the email from session state

    # Check if the email exists in the sample_data
    matched_rows = sample_data[sample_data['email'] == email]

    if not matched_rows.empty:
        index = matched_rows.index[0]
        welcome_text = f"Hello **{sample_data['first_name'][index]}** **{sample_data['last_name'][index]}**!  Please take a look at the following information."
        
        st.header("Home Page")
        st.write(welcome_text)

        # Display the user's information
        st.subheader("Name", divider="blue")
        st.write(f"{sample_data['first_name'][index]} {sample_data['last_name'][index]}")

        st.subheader("Birthday", divider="blue")
        st.write(f"{sample_data['birthday'][index]}")

        st.subheader("Medicare Status", divider="blue")
        st.write(f"{sample_data['on_medicare'][index]}")
    else:
        st.error("Email not found in the database.")

# Function for another page (only accessible if logged in)
def another_page():
    email = st.session_state['email']  # Access the email from session state

    # Check if the email exists in the sample_data
    matched_rows = sample_data[sample_data['email'] == email]

    if not matched_rows.empty:
        index = matched_rows.index[0]
        welcome_text = f"Hello **{sample_data['first_name'][index]}** **{sample_data['last_name'][index]}**! Welcome to the multi-page app!"
        st.header("Another page")
        st.write(welcome_text)
    else:
        st.error("Email not found in the database.")

# Main function to control the flow
def main():
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if 'active_page' not in st.session_state:
        st.session_state['active_page'] = "Home"
    
    # If logged in, allow access to pages
    if st.session_state['logged_in']:
        # Create a navigation sidebar
        st.sidebar.title("Navigation")
        if st.sidebar.button("Home"):
            st.session_state['active_page'] = "Home"
        if st.sidebar.button("Another Page"):
            st.session_state['active_page'] = "Another Page"
        
        # Add Logout button to sidebar
        if st.sidebar.button("Logout", type='primary'):
            st.session_state['logged_in'] = False
            st.rerun()

        # Render the selected page based on session state
        if st.session_state['active_page'] == "Home":
            home()
        elif st.session_state['active_page'] == "Another Page":
            another_page()
    else:
        # Show login page if not logged in
        login()

if __name__ == "__main__":
    main()


# Wonder if we could have an account option to save the data? -> probably use a dataframe object and .csv sheet?
# Would want to preload some account information? -> probably use a .csv sheet