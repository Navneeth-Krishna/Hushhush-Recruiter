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

# Commit the changes to the database and close the connection
conn.commit()
conn.close()