# HushHush Recruiter

An intelligent recruitment automation system that leverages candidate data from GitHub and Stack Overflow to streamline the technical hiring process.

## What It Does

HushHush Recruiter is a comprehensive recruitment automation platform that:
- Collects and analyzes candidate data from GitHub and Stack Overflow profiles
- Uses machine learning (K-means clustering) to evaluate and select potential candidates
- Automates the entire recruitment workflow including:
  - Candidate selection
  - Email communications
  - Coding challenge distribution
  - Application status updates

## Key Features

- **Data Collection & Analysis**
  - GitHub profile analysis (followers, repositories, contributions)
  - Stack Overflow profile evaluation (reputation, badges, activity)
  - Automated data cleaning and processing
  
- **Smart Candidate Selection**
  - Machine learning-based candidate clustering
  - Automated shortlisting based on technical metrics
  - Standardized evaluation criteria

- **Automated Communication**
  - Personalized email notifications
  - Google Form integration for candidate information
  - Automated coding challenge distribution via Google Colab
  - Application status updates

- **Web Interface**
  - Dashboard for managing selected candidates
  - Email trigger functionality
  - Candidate status tracking


## Prerequisites

- Python 3.x
- SQLite
- Flask
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Navneeth-Krishna/Hushhush-Recruiter.git
   cd Hushhush-Recruiter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the `code` folder with:
   ```
   EMAIL="The email id from which you want to send the initial mail"
   PASSWORD="App Password which is generated for the above email id"
   GITHUB_TOKEN="The Github Personal Access Token"
   ```

4. Initialize the database:
   ```bash
   python code/DB_connection.py
   ```

## Usage

1. Data Collection and Processing:
   ```bash
   python code/datafetch/Github.py
   python code/datafetch/stackoverflow.py
   python code/DataCleaning.py
   ```

2. Run Selection Model:
   ```bash
   python code/Selection_Model_Training.py
   python code/Main_Selection.py
   ```

3. Start the Web Interface:
   ```bash
   cd code/backend
   python app.py
   ```


## Authors

- [Navneeth Krishna Aravind](https://github.com/Navneeth-Krishna)
- [Vedanth](https://github.com/vedanth09)
- [Terry Poonacha](https://github.com/Terrypoonacha)
- [Dharshan](https://github.com/Dharshan110701)
- [Aparnna Dash](https://github.com/Aparnna07)