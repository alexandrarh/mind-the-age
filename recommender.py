import pandas as pd
import numpy as np
from fuzzywuzzy import process # pip install fuzzywuzzy , pip install python-Levenshtein

# Load datasets

class theRecommender():
     
    def __init__(self):
        self.paceData = pd.read_csv('data/PACE_2022_cleaned.csv')  
        self.resourceLinks = pd.read_csv('data/resource_link.csv')
        
        self.mappingCondition = {
            'Anxiety': 'anxiety,mental,health,wellness',
            'Depression': 'depression,suicidal,mental',
            'Bipolar': 'bipolar,disorder,health',
            'BPD':'',
            'Schizophrenia' : '',
            'Other' : '',
        }

        self.mappingGender = {
            'Male' : 'male,men,man,boy', 
            'Female': 'female,women,woman,girl'
            # include non binary
        }
        
        self.mappingRace = {
            'African American' : 'Black',
            'White' : 'people,community'
        }

    # include Filtering by income for pace!!
    # need to think of what the logic for filtering based on income would be 

    # Match PACE facility based on County

    # conduct more testing , think or edge and corner cases

    # manually standardized some matching words:
    # how do I take into account race&gender specific websites?
    # string inputs must be standarized!! lowercase and offical title to match the map!
        

    def match_pace_facility(self, county):

        # Filter by county
        matchedRow = self.paceData[self.paceData['County'] == county]
        
        # Within the county, find rows with the "full dual"
        full_dual_rows = matchedRow[matchedRow['Category of Aid'] == 'Full-Dual']
        
        # If no full dual rows, return no matching facility?
        
        # Find the row with the lowest upper bound cost
        min_cost_row = full_dual_rows.loc[full_dual_rows['Upper Bound'].idxmin()]
        
        return min_cost_row['PACE Organization']

    # match resource link using fuzzy matching
    # matching algorithm not very accurate
    def match_resource_link(self, category, usedLinks):
        set = True 
        threshold = 80
        # function perfroms fuzzy string matching by compairing strings and returing the one that is most similar
        # and a score that indicates how similar the match is to the input string tuple ("string", 90)
        # just separate extract function by the 3 criteria
        while threshold > 0:
            bestMatch = process.extractOne(category, self.resourceLinks['Description']) 
            if bestMatch:  # threshold for match confidence
                matchedRow = self.resourceLinks[self.resourceLinks['Description'] == bestMatch[0]]
                # we also want to return the description
                title = matchedRow['Title'].values[0]
                descript = matchedRow['Description'].values[0]
                link = matchedRow['Link'].values[0]
                #check if it is a link we used OR add it to the used list
                if link not in usedLinks:
                    usedLinks.append(link)
                    return link, descript, title
                else: 
                    threshold -= 10
                # else: find another link  
            else: 
                return "No matching resource"

    # in the app we import the file and functions
    # we can call this function and pass the user profile as a dictionary
    # the returning value is another dictionary mapping the links to their respective category
    def get_all_links(self, user_input):
        # user input is a key value
        # we standarize and retrieve the according value 
        condition = self.mappingCondition.get(user_input.get('Condition'),user_input.get('Condition'))
        race = self.mappingRace.get(user_input.get('Race'), user_input.get('Race'))
        gender = self.mappingGender.get(user_input.get('Gender'),user_input.get('Gender'))

        # initialize new list and map
        usedLinks = []
        theUsedLinks = {}
        allDescriptions = {}
        allTitles = {}

        # fill the key value pair with the matching link
        theUsedLinks['Race'], allDescriptions['Race'], allTitles['Race'] = self.match_resource_link(race, usedLinks)
        theUsedLinks['Gender'], allDescriptions['Gender'], allTitles['Gender'] = self.match_resource_link(gender, usedLinks)
        theUsedLinks['Condition'], allDescriptions['Condition'], allTitles['Condition'] = self.match_resource_link(condition, usedLinks)
        return theUsedLinks, allDescriptions, allTitles

# Example user input
# fuzzy matching maps white -> black
user_input = {
    'Condition': 'Bipolar Disorder',
    'County': 'San Francisco',
    'Race': 'Black',
    'Gender': 'Women'
}
recClass = theRecommender()
paceFacility = recClass.match_pace_facility(user_input['County'])
resourceLinks, descript, titles = recClass.get_all_links(user_input)

print(f"recommended PACE Facility: {paceFacility}")
print(f"Tailored resource Links: {resourceLinks}")
print("descriptions: ", descript)
print("titles: ", titles)

