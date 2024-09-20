import pandas as pd
from difflib import SequenceMatcher
import json

# Git_Users_df = pd.read_csv("D:\\git\\bdp-apr24-exam-bdp_apr24_group1\\code\\Github_Users.csv")
# Repos_df = pd.read_csv('D:\\git\\bdp-apr24-exam-bdp_apr24_group1\\code\\Github_Users_Repos.csv' )
# Stack_Users_df = pd.read_csv("D:\\git\\bdp-apr24-exam-bdp_apr24_group1\\code\\stackoverflow.csv")

Git_Users_df = pd.read_csv('Github_Users.csv')
Repos_df = pd.read_csv('Github_Users_Repos.csv')
Stack_Users_df = pd.read_csv('stackoverflow.csv')

names_1 = Git_Users_df['Name']
names_2 = Stack_Users_df['display_name']

def is_similar(name1, name2, threshold=0.70):
    similarity_ratio = SequenceMatcher(None, name1, name2).ratio()
    return similarity_ratio >= threshold 

matches = []

user_counts = Repos_df['user_id'].value_counts().reset_index()
user_counts.columns = ['user_id', 'Repo_count'] 

for name1 in names_1:
    for name2 in names_2:
        if is_similar(name1, name2):  
            matches.append((name1, name2))

matches_df = pd.DataFrame(matches, columns=['Name in File Git', 'Name in File Stack'])

x = matches_df.drop_duplicates()

merged1_df = pd.merge(x, Git_Users_df, left_on='Name in File Git', right_on= 'Name', how='inner')  

merged2_df = pd.merge(merged1_df, Stack_Users_df, left_on='Name in File Stack', right_on= 'display_name', how='inner')  
merged =merged2_df.drop_duplicates()

mergeduser = merged.drop(columns=['Name in File Git','Name in File Stack'])

merge = pd.merge(mergeduser,user_counts , how='inner', on ='user_id')
# df = merge.rename(columns={'user_id': 'id'})

final = merge.drop_duplicates()
Final = final.drop(columns=['display_name','reputation_change_quarter','link','Unnamed: 9','Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13','User_id'])

# Step 2: Extract the JSON data from the 'badge' column (replace 'badge' with the actual column name)
def parse_badges(badge):
    try:
        # Step 3: Convert the JSON-like string into a dictionary
        badge_dict = json.loads(badge.replace("'", '"'))  # Convert single quotes to double quotes
        return badge_dict
    except:
        return {'bronze': 0, 'silver': 0, 'gold': 0}  # Handle missing or malformed data

# Apply the function to the 'badge' column
badge_parsed = Final['badge_counts'].apply(parse_badges)

# Step 4: Create new columns for bronze, silver, and gold
Final['bronze'] = badge_parsed.apply(lambda x: x.get('bronze', 0))
Final['silver'] = badge_parsed.apply(lambda x: x.get('silver', 0))
Final['gold'] = badge_parsed.apply(lambda x: x.get('gold', 0))

# Step 5: Drop the original 'badge' column if no longer needed
Final = Final.drop('badge_counts', axis=1)

Clean_df =pd.DataFrame(Final)
Clean_df.to_csv('dataclean.csv', index=False)
print("completed")