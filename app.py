# Package imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import dotenv   # This is for if we use Claude and need to put in environment variables

# Loading model
mental_disorder_classifier = joblib.load('mental_disorder_classifier.joblib')

st.title("Streamlit App Title")
st.markdown('Meow meow this is the text')

# Wonder if we could have an account option to save the data? -> probably use a dataframe object and .csv sheet?
# Would want to preload some account information? -> probably use a .csv sheet