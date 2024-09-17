import requests
import numpy as np
import pandas as pd
import time

# Defne the parameters
Repos_Data = []
User_Data = []
completed_user_id = 0
user_url =[]
Starred_Repos_Data =[]

#function to get user's basic details
def userdetails(id , user):
   Git_users_dict = {}
   Git_users_dict['user_id'] =id
   Git_users_dict['Email'] = user['email']
   Git_users_dict['Name']=  user['name'] 
   Git_users_dict['Followers Count']= user['followers']
   Git_users_dict['Following Count']= user['following']
   Git_users_dict['Public Reposcount']= user['public_repos']
   Git_users_dict['Public Gistscount']= user['public_gists']
   return Git_users_dict

def UserRepoDetails (id , repos_data):
   Repo_dict = {}
   for repos in repos_data:
    if repos['language']:
        Repo_dict['user_id'] = id
        Repo_dict['stargazers_count'] = repos['stargazers_count']
        Repo_dict['watchers_count'] = repos['watchers_count']
        Repo_dict['repo_id'] = repos['id']
        Repo_dict['language'] = repos['language']
        Repo_dict['forks_count'] = repos['forks_count']
        Repo_dict['open_issues'] = repos['open_issues']
   return Repo_dict

# Logic for getting the data
headers = {
    "Authorization": "token  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"
}
for j in range (0,1000,30):
   link = f"https://api.github.com/users?since={j}"
   try:

      response = requests.get(link, headers=headers, timeout=5)
      response.raise_for_status()
      results = response.json()
      for i in range(len(results)):
         Git_users_dict = {}
         data=(results[i])
         if(data['id'] > completed_user_id):

            usr = requests.get(results[i]['url']).json()
            user_url.append(usr)
            repos_url = requests.get(data['repos_url'], headers= headers, timeout=5)
            repos_url.raise_for_status
            reposdata = repos_url.json()

      # Get the basic user details and get the inner urls
            if(user_url[i]['name']):
               print(f"Getting data for user id:{data['id']}")
               Git_users_dict = userdetails(data['id'],user_url[i])
               User_Data.append(Git_users_dict)
               time.sleep(1)
         
         # Gets the data from the repositories for the user
               Repo_dict = UserRepoDetails(data['id'], reposdata)
               Repos_Data.append(Repo_dict)
               time.sleep(1)
      completed_user_id = data['id']

   except requests.exceptions.RequestException as e:
       print(f"Error fetching data for {j} with error {e}")

users_df = pd.DataFrame(User_Data)
users_df['Email'].fillna(users_df['Name'].str.replace(r'[^a-zA-Z0-9]', '', regex=True).str.lower() + '@gmail.com', inplace=True)
repos_df = pd.DataFrame(Repos_Data)
 
users_df.to_csv('Github_Users.csv', index=False)
repos_df.to_csv('Github_Users_Repos.csv', index=False)