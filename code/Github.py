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

#function to get user's Repo details
def UserRepoDetails (id , repos_data):
   Repos_list = []
   for repos in repos_data:
    if repos['language']:
        
        Repo_dict ={
        'user_id' : id,
        'stargazers_count' : repos['stargazers_count'],
        'watchers_count':  repos['watchers_count'],
        'repo_id' : repos['id'],
        'language' : repos['language'],
        'forks_count': repos['forks_count'],
        'open_issues': repos['open_issues']
        }
        Repos_list.append(Repo_dict)
   return Repos_list

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
         #  To avoid duplicate fetching of same user data
         if(data['id'] > completed_user_id):  
            usr = requests.get(results[i]['url']).json()
            user_url.append(usr)
            repos_url = requests.get(data['repos_url'], headers= headers, timeout=5)
            repos_url.raise_for_status
            reposdata = repos_url.json()
            starred_url = data['starred_url'].split('{')[0]
            starred_repo = requests.get(starred_url, headers= headers, timeout=5)
            starred_repo.raise_for_status()
            stareddata = starred_repo.json()
            
         # Get the basic user details and get the repo url
         if(user_url[i]['name']):
            print(f"Getting data for user id:{data['id']}")
            Git_users_dict = userdetails(data['id'],user_url[i])
            User_Data.append(Git_users_dict)
            time.sleep(1)

            # Gets the Repo data of user
            Repo_dict = UserRepoDetails(data['id'], reposdata)
            Repos_Data.extend(Repo_dict)
            time.sleep(1)
      completed_user_id = data['id']

   except Exception as e:
      print(f"failed to get data of user{j} with status code{e}")


users_df = pd.DataFrame(User_Data)
users_df['Email'].fillna(users_df['Name'].str.replace(r'[^a-zA-Z0-9]', '', regex=True).str.lower() + '@gmail.com', inplace=True)
repos_df = pd.DataFrame(Repos_Data)
 
users_df.to_csv('Github_Users.csv', index=False)
repos_df.to_csv('Github_Users_Repos.csv', index=False)