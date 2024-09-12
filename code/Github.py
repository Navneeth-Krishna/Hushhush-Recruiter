import requests
import numpy as np
import pandas as pd
import time

# Defne the parameters

ID = []
Repos_Data = []
User_Data = []
user_url =[]
Starred_Repos_Data =[]
email = []
name = []
public_reposcount = []
public_gistscount = []
Followers_Count = []
Following_Count = []

# Logic for getting the data
headers = {
    "Authorization": "token  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"
}
for j in range (0,500,30):
   link = f"https://api.github.com/users?since={j}"
   response = requests.get(link, headers=headers, timeout=5)
   if (response.status_code == 200):
      results = response.json()
      for i in range(len(results)):
        Git_users_dict = {}
        data=(results[i])
        Git_users_dict['user_id'] = data['id']
        usr = requests.get(results[i]['url']).json()
        user_url.append(usr)
        if(user_url[i]['name']):
            print(f"Getting data for user id:{data['id']}")
            Git_users_dict['Email'] = user_url[i]['email']
            Git_users_dict['Name']=  user_url[i]['name'] 
            Git_users_dict['Followers Count']= user_url[i]['followers']
            Git_users_dict['Following Count']= user_url[i]['following']
            Git_users_dict['Public Reposcount']= user_url[i]['public_repos']
            Git_users_dict['Public Gistscount']= user_url[i]['public_repos']
            User_Data.append(Git_users_dict)
            repos_url = requests.get(user_url[i]['repos_url']).json() #need a for loop to interatae each repo details#
            starred_url= user_url[i]['starred_url']
            starred_url = starred_url.split('{')
            starred_repo = requests.get(starred_url[0]).json() #need a for loop to interatae each starred repo details#
            time.sleep(1)

            for j in range(len(repos_url)):
                Repo_dict = {}
                each_repo = (repos_url[j])
                if(each_repo['language']):
                    Repo_dict['user_id'] = data['id']
                    Repo_dict['stargazers_count'] = each_repo['stargazers_count']
                    Repo_dict['watchers_count'] = each_repo['watchers_count']
                    Repo_dict['repo_id'] = each_repo['id']
                    Repo_dict['language'] = each_repo['language']
                    Repo_dict['forks_count'] = each_repo['forks_count']
                    Repo_dict['open_issues'] = each_repo['open_issues']
                    Repos_Data.append(Repo_dict)
                    time.sleep(1)

            for k in range(len(starred_repo)):
                Stared_repo_dict = {}
                starredrepo = (starred_repo[k])
                if(starredrepo['language']):
                    Stared_repo_dict['user_id'] = data['id']
                    Stared_repo_dict['stargazers_count'] = starredrepo['stargazers_count']
                    Stared_repo_dict['watchers_count'] = starredrepo['watchers_count']
                    Stared_repo_dict['repo_id'] = starredrepo['id']
                    Stared_repo_dict['language'] = starredrepo['language']
                    Stared_repo_dict['forks_count'] = starredrepo['forks_count']
                    Stared_repo_dict['open_issues'] = starredrepo['open_issues']
                    Starred_Repos_Data.append(Stared_repo_dict)
                    time.sleep(1)
   else:
      print(f"API failed in {i} for the error {response.status_code}")
      

