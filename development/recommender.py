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
# how do I take into account race&gender specific websites?
mappingCondition = {
    'Anxiety': 'anxiety,mental,health,wellness'
}
mappingGender = {
    'Male' : 'male,men,man,boy', 
    'Female': 'female,women,woman,girl'
    # include non binary
}
mappingRace = {
    'African American' : 'Black',
    'White' : 'group,people,community'
}

def match_pace_facility(county):

    # Filter by county
    matchedRow = paceData[paceData['County'] == county]
    
    # Within the county, find rows with the "full dual"
    full_dual_rows = matchedRow[matchedRow['Category of Aid'] == 'Full-Dual']
    
    # If no full dual rows, return no matching facility?
    
    # Find the row with the lowest upper bound cost
    min_cost_row = full_dual_rows.loc[full_dual_rows['Upper Bound'].idxmin()]
    
    return min_cost_row['PACE Organization']

# match resource link using fuzzy matching
# matching algorithm not very accurate
def match_resource_link(category, usedLinks):

    # function perfroms fuzzy string matching by compairing strings and returing the one that is most similar
    # and a score that indicates how similar the match is to the input string tuple ("string", 90)
    # just separate extract function by the 3 criteria 
    bestMatch = process.extractOne(category, resourceLinks['Description']) 
    if bestMatch and bestMatch[1] > 10:  # threshold for match confidence
        matchedRow = resourceLinks[resourceLinks['Description'] == bestMatch[0]]
        link = matchedRow['Link'].values[0]
        #check if it is a link we used OR add it to the used list
        if link not in usedLinks:
            usedLinks.append(link)
            return matchedRow['Link'].values[0]
        # else: find another link  
    else:
        return "No matching resource link found"
    

def get_all_links(user_input):
    # user input is a key value
    # we standarize and retrieve the according value 
    condition = mappingCondition.get(user_input.get('Condition'),user_input.get('Race'))
    race = mappingRace.get(user_input.get('Race'), user_input.get('Race'))
    gender = mappingGender.get(user_input.get('Gender'),user_input.get('Gender'))

    # initialize new list and map
    usedLinks = []
    resourceLinks = {}

    # fill the key value pair with the matching link
    resourceLinks['Race'] = match_resource_link(race, usedLinks)
    resourceLinks['Gender'] = match_resource_link(gender, usedLinks)
    resourceLinks['Condition'] = match_resource_link(condition, usedLinks)
    return resourceLinks

# Example user input
# fuzzy matching maps white -> black
user_input = {
    'Condition': 'depression',
    'County': 'Alameda',
    'Race': 'Asian',
    'Gender': 'Women'
}

paceFacility = match_pace_facility(user_input['County'])
resourceLinks = get_all_links(user_input)

print(f"recommended PACE Facility: {paceFacility}")
print(f"Tailored resource Links: {resourceLinks}")


