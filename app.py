# Package imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import anthropic
import time
from recommender import theRecommender

# Loading classifier model
with open('mental_health_classifier.pkl', 'rb') as f:
    mental_health_classifier = pickle.load(f)

# Loading Claude AI
anthropic_key = st.secrets["anthropic_key"]
anthropic = anthropic.Anthropic(api_key=anthropic_key)

# Loading data
sample_data = pd.read_csv('database_sample.csv')
sample_data['patient_comment'] = sample_data['patient_comment'].fillna('').astype('object')

# Loading recommender
class_recommender = theRecommender()

# Headers for all pages
st.title("MindTheAge")
st.markdown('Bridging the gap between older folks and mental healthcare.')

# Initialization of session states
if 'email' not in st.session_state:
    st.session_state['email'] = ''
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = ''
if 'last_name' not in st.session_state:
    st.session_state['last_name'] = ''
if 'birthday' not in st.session_state:
    st.session_state['birthday'] = ''
if 'on_medicare' not in st.session_state:
    st.session_state['on_medicare'] = ''
if 'city' not in st.session_state:
    st.session_state['city'] = ''
if 'county' not in st.session_state:
    st.session_state['county'] = ''
if 'patient_comment' not in st.session_state:    
    st.session_state['patient_comment'] = ''
if 'medical_input' not in st.session_state:
    st.session_state['medical_input'] = ''
if 'Race' not in st.session_state:
    st.session_state['Race'] = ''
if 'Gender' not in st.session_state:
    st.session_state['Gender'] = ''

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

        st.subheader("Race",divider='blue')
        st.write(f"{sample_data['race'][index]}")
    else:
        st.error("Email not found in the database.")

# Function for mental health page (only accessible if logged in)
def mental_health_page():
    email = st.session_state['email']  # Access the email from session state

    # Check if the email exists in the sample_data
    matched_rows = sample_data[sample_data['email'] == email]

    if not matched_rows.empty:
        index = matched_rows.index[0]
        st.header("Get Mental Health Resources")

        st.markdown("Want to begin your mental health journey? We can help you find the right resources. Answer a few questions to get started.")

        if st.button("Start Evaluation"):
            st.session_state['active_page'] = "Mental Health Evaluation"
            st.rerun()
    else:
        st.error("Email not found in the database.")

# Function for mental health evaluation to get resources
def mental_health_evaluation():
    st.header("Mental Health Evaluation")
    st.write("Please review and/or edit the following responses before proceeding.")
    sample_data['birthday'] = pd.to_datetime(sample_data['birthday'], errors='coerce')

    email = st.session_state['email']  # Access the email from session state

    # Check if the email exists in the sample_data
    matched_rows = sample_data[sample_data['email'] == email]
    index = matched_rows.index[0]

    # Reviewing the user's information
    first_name = st.text_input("First Name", value=sample_data['first_name'][index])
    last_name = st.text_input("Last Name", value=sample_data['last_name'][index])
    
    birthday = st.date_input("Birthday", value=sample_data['birthday'][index], format="MM/DD/YYYY")
    
    on_medicare = st.selectbox("Are you on Medicare?", ["Yes", "No"], index=0 if sample_data['on_medicare'][index] == "Yes" else 1)
    city = st.text_input("City", value=sample_data['city'][index])
    county = st.text_input("County", value=sample_data['county'][index])

    patient_input = st.text_area("Patient comment", placeholder="Type your comment here")

    # Manage confirmation state
    if 'confirmation_pending' not in st.session_state:
        st.session_state.confirmation_pending = False

    # Handle Save Information button click
    if st.button("Save Information"):
        st.session_state.confirmation_pending = True  # Set the confirmation flag

    # Show confirmation dialog if needed
    if st.session_state.confirmation_pending:
        st.write("Are you sure you want to proceed?")
        if st.button("Yes"):
            # Updating provided data
            sample_data.loc[index, 'first_name'] = first_name
            st.session_state['first_name'] = first_name

            sample_data.loc[index, 'last_name'] = last_name
            st.session_state['last_name'] = last_name

            sample_data.loc[index, 'birthday'] = pd.to_datetime(birthday)
            st.session_state['birthday'] = birthday

            sample_data.loc[index, 'on_medicare'] = on_medicare
            st.session_state['on_medicare'] = on_medicare

            sample_data.loc[index, 'city'] = city
            st.session_state['city'] = city

            sample_data.loc[index, 'county'] = county
            st.session_state['county'] = county

            sample_data.loc[index, 'patient_comment'] = str(patient_input)
            st.session_state['patient_comment'] = str(patient_input)

            st.session_state['medical_input'] = str(sample_data.loc[index, 'medical_input'])

            st.session_state.show_progress = True
            
            st.session_state['active_page'] = "Recommendations"  # Switch page
            st.session_state.confirmation_pending = False  
            st.success("Information saved successfully!")  
            st.rerun()  # Rerun to reflect changes
        elif st.button("No"):
            st.session_state.confirmation_pending = False 
            st.success("Action canceled.")
            
# Get mental health leaning based on input (from medical and patient comment)
def get_mental_leanings(patient_comment):
    if patient_comment == '' or patient_comment is None:
        if st.session_state['medical_input'] == '' or st.session_state['medical_input'] is None:
            return "Can't determine"
        else:
            # Wrap the input in a list to avoid the string object error
            predicted_label = mental_health_classifier.predict([st.session_state['medical_input']])
    else:
        if st.session_state['medical_input'] == '' or st.session_state['medical_input'] is None:
            predicted_label = mental_health_classifier.predict([patient_comment])
        else:
            full_input = st.session_state['medical_input'] + '\n' + patient_comment
            # Again, wrap the combined input in a list
            predicted_label = mental_health_classifier.predict([full_input])

    return predicted_label[0]

# Receiving resources -> NEED TO FINISH THIS PART WITH FILTERING AND CLAUDE
def get_mental_health_resources():
    st.header("Mental Health Resources")

    # access the correct user row
    matched_rows = sample_data[sample_data['email'] == st.session_state['email']]
    index = matched_rows.index[0]

    # Get mental health leanings based on input
    mental_leanings = get_mental_leanings(st.session_state['patient_comment'])

    # retrive county, race, conditon (mental leanings) and gender from pandas data frame
    # save all of that into a dictionary user input
    userInput = {
    'Condition': mental_leanings,
    'County': sample_data['county'][index],
    'Race': sample_data['race'][index],
    'Gender': sample_data['gender'][index]
   }
    paceFacility = class_recommender.match_pace_facility(sample_data['county'][index])
    links, descriptions, resourceTitles = class_recommender.get_all_links(userInput)
    # import recommender and and match_pace_facility() get_all_links() function
    # return and st.write pace facility
    # return save and parse the returned dictionary 
    # st.write all the links accordingly 

    # Show progress
    if 'show_progress' in st.session_state and st.session_state.show_progress:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        total_steps = 100  
        sleep_duration = 0.05 

        for percent_complete in range(total_steps):
            time.sleep(sleep_duration)
            my_bar.progress(percent_complete + 1, text=progress_text)
        
        time.sleep(1)  # Additional delay at the end
        my_bar.empty()

        # Function to display mental health resources
        st.markdown("**:blue[Based on your responses and information, here are some mental health resources:]**")
        
        # Test part -> remove when fixed
        # st.write(st.session_state['county'])
        # st.write(st.session_state['patient_comment'])
        # st.write(mental_leanings)

        st.write("**:green[Pace Facility]**")
        st.write(paceFacility)

        # resourceTitles
        st.write("**:orange[Other resources]**")
        st.write(f"**{resourceTitles['Race']}**")
        st.write(f"{descriptions['Race']} You can access it here: {links['Race']}")

        st.write(f"**{resourceTitles['Gender']}**")
        st.write(f"{descriptions['Gender']} You can access it here: {links['Gender']}")

        st.write(f"**{resourceTitles['Condition']}**")
        st.write(f"{descriptions['Condition']} You can access it here: {links['Condition']}")

        # Reset the progress flag after completion
        st.session_state.show_progress = False
    else:
        st.write("No resources to process.")

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
        if st.sidebar.button("Mental Health Resources"):
            st.session_state['active_page'] = "Mental Health Resources"
        
        # Add Logout button to sidebar
        if st.sidebar.button("Logout", type='primary'):
            st.session_state['logged_in'] = False
            st.rerun()

        # Render the selected page based on session state
        if st.session_state['active_page'] == "Home":
            home()
        elif st.session_state['active_page'] == "Mental Health Resources":
            mental_health_page()
        elif st.session_state['active_page'] == "Mental Health Evaluation":
            mental_health_evaluation()
        elif st.session_state['active_page'] == "Recommendations":
            get_mental_health_resources()
    else:
        # Show login page if not logged in
        login()

if __name__ == "__main__":
    main()