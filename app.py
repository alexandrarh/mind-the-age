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

st.title("MindTheAge")
st.markdown('Bridging the gap between older folks and mental healthcare.')

st.header("Login with your email")
email = st.text_input("Email", placeholder='Type your email here')
login_button = st.button("Login", type='primary')

# Need to add email in order to get through
if email == "" and login_button:
    st.error("Please enter a valid email address.")
elif login_button:
    if email in st.secrets["registered_users"]:
        st.success("Login successful!")
        st.write("Welcome, " + email + "!")
    else:
        st.error("Email not found. Please register first.")

# Wonder if we could have an account option to save the data? -> probably use a dataframe object and .csv sheet?
# Would want to preload some account information? -> probably use a .csv sheet