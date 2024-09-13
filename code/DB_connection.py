import sqlite3
import pandas as pd

# Establish a connection to the SQLite database
conn = sqlite3.connect('hushhushDB.db')
c = conn.cursor()

# Create the table if it does not exist
c.execute('''
    CREATE TABLE IF NOT EXISTS stackoverflow_data (
        UserID INT PRIMARY KEY,
        DisplayName TEXT,
        Reputation INT,
        ProfileURL TEXT,
        Location TEXT,
        CreationDate BIGINT,
        LastAccessDate BIGINT,
        TotalVotes INT,
        GoldBadges INT,
        SilverBadges INT,
        BronzeBadges INT,
        TopTags TEXT
    )
''')

# Commit the changes to the database
conn.commit()

# Read the CSV file into a DataFrame
stackoverflow_data_df = pd.read_csv('/Users/vedanth/Desktop/HushHush/stackoverflow_data.csv')

# Print DataFrame columns and the first few rows for debugging
print("DataFrame columns:", stackoverflow_data_df.columns)
print(stackoverflow_data_df.head())

# Define the insert query with the correct number of placeholders
insert_query = '''
    INSERT INTO stackoverflow_data (
        UserID, DisplayName, Reputation, ProfileURL, Location, 
        CreationDate, LastAccessDate, TotalVotes, GoldBadges, 
        SilverBadges, BronzeBadges, TopTags
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
'''

# Insert data into the stackoverflow_data table
for row in stackoverflow_data_df.itertuples(index=False, name=None):
    if len(row) == 12:  # Ensure the row has exactly 12 values
        c.execute(insert_query, row)
    else:
        print(f"Skipping row with incorrect number of values: {row}")


# Create the GitUsers table
c.execute('''
    CREATE TABLE IF NOT EXISTS GitUsers (
        user_id INT PRIMARY KEY,        
        Email VARCHAR(150),               
        Name TEXT,                 
        Followers_Count INT,            
        Following_Count INT,            
        Public_Reposcount INT,          
        Public_Gistscount INT
    )
''')

# Create the Repo_dict table
c.execute('''
    CREATE TABLE IF NOT EXISTS Repo_dict (
        repo_id INT PRIMARY KEY,        
        user_id INT,                    
        stargazers_count INT,           
        watchers_count INT,             
        language TEXT,                      
        forks_count INT,                
        open_issues INT,                
        FOREIGN KEY (user_id) REFERENCES GitUsers(user_id)
    )
''')

# Create the Stared_repo_dict table
c.execute('''
    CREATE TABLE IF NOT EXISTS Stared_repo_dict (
        repo_id INT,                    
        user_id INT,                    
        stargazers_count INT,           
        watchers_count INT,             
        language TEXT,                      
        forks_count INT,                
        open_issues INT,                
        PRIMARY KEY (repo_id, user_id),     
        FOREIGN KEY (user_id) REFERENCES GitUsers(user_id),
        FOREIGN KEY (repo_id) REFERENCES Repo_dict(repo_id)
    )
''')

conn.commit()

# --- Insert Data for GitUsers Table ---

# Read the CSV file into a DataFrame
gitusers_df = pd.read_csv('/Users/vedanth/Desktop/HushHush/GitUsers.csv')

# Print DataFrame columns and the first few rows for debugging
print("GitUsers DataFrame columns:", gitusers_df.columns)
print(gitusers_df.head())

# Define the insert query for GitUsers table
insert_gitusers_query = '''
    INSERT OR IGNORE INTO GitUsers (
        user_id, Email, Name, Followers_Count, Following_Count, 
        Public_Reposcount, Public_Gistscount
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?
    )
'''

# Insert data into the GitUsers table
for row in gitusers_df.itertuples(index=False, name=None):
    if len(row) == 7:  # Ensure the row has exactly 7 values
        c.execute(insert_gitusers_query, row)
    else:
        print(f"Skipping row with incorrect number of values: {row}")

conn.commit()

# --- Insert Data for Repo_dict Table ---

# Read the CSV file into a DataFrame
repodict_df = pd.read_csv('/Users/vedanth/Desktop/HushHush/Repo_dict.csv')

# Print DataFrame columns and the first few rows for debugging
print("Repo_dict DataFrame columns:", repodict_df.columns)
print(repodict_df.head())

# Define the insert query for Repo_dict table
insert_repodict_query = '''
    INSERT OR IGNORE INTO Repo_dict (
        repo_id, user_id, stargazers_count, watchers_count, language, forks_count, open_issues
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?
    )
'''

# Insert data into the Repo_dict table
for row in repodict_df.itertuples(index=False, name=None):
    if len(row) == 7:  # Ensure the row has exactly 7 values
        c.execute(insert_repodict_query, row)
    else:
        print(f"Skipping row with incorrect number of values: {row}")

conn.commit()

# --- Insert Data for Stared_repo_dict Table ---

# Read the CSV file into a DataFrame
staredrepo_df = pd.read_csv('/Users/vedanth/Desktop/HushHush/Stared_repo_dict.csv')

# Print DataFrame columns and the first few rows for debugging
print("Stared_repo_dict DataFrame columns:", staredrepo_df.columns)
print(staredrepo_df.head())

# Define the insert query for Stared_repo_dict table
insert_staredrepo_query = '''
    INSERT OR IGNORE INTO Stared_repo_dict (
        repo_id, user_id, stargazers_count, watchers_count, language, forks_count, open_issues
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?
    )
'''

# Insert data into the Stared_repo_dict table
for row in staredrepo_df.itertuples(index=False, name=None):
    if len(row) == 7:  # Ensure the row has exactly 7 values
        c.execute(insert_staredrepo_query, row)
    else:
        print(f"Skipping row with incorrect number of values: {row}")

# Create a new table for Repo_dict without the 'name' and 'description' columns
c.execute('''
    CREATE TABLE IF NOT EXISTS Repo_dict_temp (
        repo_id INT PRIMARY KEY,        
        user_id INT,                    
        stargazers_count INT,           
        watchers_count INT,             
        language TEXT,                      
        forks_count INT,                
        open_issues INT,                
        FOREIGN KEY (user_id) REFERENCES GitUsers(user_id)
    )
''')

# Create a new table for Stared_repo_dict without the 'name' and 'description' columns
c.execute('''
    CREATE TABLE IF NOT EXISTS Stared_repo_dict_temp (
        repo_id INT,                    
        user_id INT,                    
        stargazers_count INT,           
        watchers_count INT,             
        language TEXT,                      
        forks_count INT,                
        open_issues INT,                
        PRIMARY KEY (repo_id, user_id),     
        FOREIGN KEY (user_id) REFERENCES GitUsers(user_id),
        FOREIGN KEY (repo_id) REFERENCES Repo_dict(repo_id)
    )
''')

# Copy data from old Repo_dict to new Repo_dict_temp
c.execute('''
    INSERT INTO Repo_dict_temp (repo_id, user_id, stargazers_count, watchers_count, language, forks_count, open_issues)
    SELECT repo_id, user_id, stargazers_count, watchers_count, language, forks_count, open_issues
    FROM Repo_dict
''')

# Copy data from old Stared_repo_dict to new Stared_repo_dict_temp
c.execute('''
    INSERT INTO Stared_repo_dict_temp (repo_id, user_id, stargazers_count, watchers_count, language, forks_count, open_issues)
    SELECT repo_id, user_id, stargazers_count, watchers_count, language, forks_count, open_issues
    FROM Stared_repo_dict
''')

# Drop the old tables
c.execute('DROP TABLE IF EXISTS Repo_dict')
c.execute('DROP TABLE IF EXISTS Stared_repo_dict')

# Rename the new tables to the original table names
c.execute('ALTER TABLE Repo_dict_temp RENAME TO Repo_dict')
c.execute('ALTER TABLE Stared_repo_dict_temp RENAME TO Stared_repo_dict')

conn.commit()
conn.close()