import pandas as pd
import numpy as np
from fuzzywuzzy import process # pip install fuzzywuzzy , pip install python-Levenshtein

# Load datasets
paceData = pd.read_csv('data/PACE_2022_cleaned.csv')  
resourceLinks = pd.read_csv('data/resource_link.csv')  

# include Filtering by income for pace!!
# need to think of what the logic for filtering based on income would be 

# Match PACE facility based on County

# conduct more testing , think or edge and corner cases

# manually standardized some matching words:
mappingGender = {
    'Male' : 'male,men,man,boy', 
    'Female': 'female,women,woman,girl'
}

mappingRace = {
    'African American' : 'Black'
}

# will probably have to do fuzzy matching in this function as well based on user app data
def match_pace_facility(county):

    matchedRow = paceData[paceData['County'] == county]
    if not matchedRow.empty:
        return matchedRow['PACE Organization'].values[0]  
    else:
        return "No matching PACE facility"

# match resource link using fuzzy matching
def match_resource_link(condition, race, gender):

    standardizeGender = mappingGender.get(gender, gender)

    # function perfroms fuzzy string matching by compairing strings and returing the one that is most similar
    # and a score that indicates how similar the match is to the input string tuple ("string", 90)
    bestMatch = process.extractOne(condition + ' ' + race + ' ' + standardizeGender, resourceLinks['Description']) 
   
    if bestMatch and bestMatch[1] > 60:  # threshold for match confidence
        matchedRow = resourceLinks[resourceLinks['Description'] == bestMatch[0]]
        return matchedRow['Link'].values[0]  
    else: 
        return "No matching resource link found"

# Example user input
user_input = {
    'Condition': 'depression',
    'County': 'Sacramento',
    'Race': 'Black',
    'Gender': 'Male'
}

# results
pace_facility = match_pace_facility(user_input['County'])
resource_link = match_resource_link(user_input['Condition'], user_input['Race'], user_input['Gender'])

print(f"Recommended PACE Facility: {pace_facility}")
print(f"Relevant Resource Link: {resource_link}")
