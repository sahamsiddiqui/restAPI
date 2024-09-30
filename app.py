# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:19:19 2024

@author: ssiddiqui
"""


from flask import Flask, request, jsonify
import pandas as pd
import os


app = Flask(__name__)


# Function to clean and normalize text values for csv and user input
def normalize(text):
    return text.strip().lower()


# Loading the csv data
try:
    # Get the directory path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')

    # Load the data into pandas DataFrames
    countries_df = pd.read_csv(os.path.join(data_dir, 'countries.csv'))
    platform_df = pd.read_csv(os.path.join(data_dir, 'platformname.csv'))
    vertical_df = pd.read_csv(os.path.join(data_dir, 'vertical.csv'))
    browsername_df = pd.read_csv(os.path.join(data_dir, 'browsername.csv'))

    print("DataFrames loaded successfully via Dynamic Upload.")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("One or more files were not found. Please check the file paths.")
except pd.errors.EmptyDataError as e:
    print(f"Error: {e}")
    print("One or more files are empty. Please check the files.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")



# Cleaning and processing steps:

# Rename columns for clarity
countries_df.columns = ['country', 'average_opportunities']
platform_df.columns = ['platform', 'average_opportunities']
vertical_df.columns = ['vertical', 'average_opportunities']
browsername_df.columns = ['browser', 'average_opportunities']

# Remove duplicates, NA, and null values
countries_df = countries_df.drop_duplicates().dropna()
platform_df = platform_df.drop_duplicates().dropna()
vertical_df = vertical_df.drop_duplicates().dropna()
browsername_df = browsername_df.drop_duplicates().dropna()

# Convert columns with names to strings
countries_df['country'] = countries_df['country'].astype(str)
platform_df['platform'] = platform_df['platform'].astype(str)
vertical_df['vertical'] = vertical_df['vertical'].astype(str)
browsername_df['browser'] = browsername_df['browser'].astype(str)

# Normalize the attribute values
countries_df['country'] = countries_df['country'].apply(normalize)
platform_df['platform'] = platform_df['platform'].apply(normalize)
vertical_df['vertical'] = vertical_df['vertical'].apply(normalize)
browsername_df['browser'] = browsername_df['browser'].apply(normalize)

# Function to calculate probability
def process_dataframe(df):

    # Calculate the probability column
    total_opportunities = df['average_opportunities'].sum()
    df['probability'] = df['average_opportunities'] / total_opportunities
    
    return df
    
# Applying function to each DataFrame
countries_df = process_dataframe(countries_df)
platform_df = process_dataframe(platform_df)
vertical_df = process_dataframe(vertical_df)
browsername_df = process_dataframe(browsername_df)

# Print final dataframes
print('########  Cleaned and processed dataframes :  ############\n')
print(f'platform: {platform_df.head()}\n')
print(f'browser : {browsername_df.head()}\n')
print(f'vertical : {vertical_df.head()}\n')
print(f'country : {countries_df.head()}\n')
print('\n ###########################################################\n')



# Function to calculate expected total count
def calculate_expected_count(countries, platforms, verticals, browsers, total_requests):
    print("Countries input:", countries)
    print("Platforms input:", platforms)
    print("Verticals input:", verticals)
    print("Browsers input:", browsers)
    print("Total requests:", total_requests)
    
    country_prob = countries_df[countries_df['country'].isin(countries)]['probability'].sum() if countries else 1
    print("Country Probability:", country_prob)
    
    platform_prob = platform_df[platform_df['platform'].isin(platforms)]['probability'].sum() if platforms else 1
    print("Platform Probability:", platform_prob)
    
    vertical_prob = vertical_df[vertical_df['vertical'].isin(verticals)]['probability'].sum() if verticals else 1
    print("Vertical Probability:", vertical_prob)
    
    browser_prob = browsername_df[browsername_df['browser'].isin(browsers)]['probability'].sum() if browsers else 1
    print("Browser Probability:", browser_prob)

    combined_prob = country_prob * platform_prob * vertical_prob * browser_prob
    print("Combined Probability:", combined_prob)
    
    expected_count = combined_prob * total_requests
    print("Expected Count:", expected_count)

    return expected_count

@app.route('/calculate/<countries>/<platforms>/<verticals>/<browsers>/<total_requests>', methods=['GET'])
def calculate(countries, platforms, verticals, browsers, total_requests):
    # Normalize and clean the input values
    def normalize_and_clean(input_value):
        return [normalize(v) for v in input_value.split(',') if v.strip()] if input_value != 'all' else []

    countries = normalize_and_clean(countries)
    platforms = normalize_and_clean(platforms)
    verticals = normalize_and_clean(verticals)
    browsers = normalize_and_clean(browsers)
    total_requests = int(total_requests) if total_requests else 100000000

    expected_count = calculate_expected_count(countries, platforms, verticals, browsers, total_requests)

    return jsonify({'expected_total_count': expected_count})


if __name__ == "__main__":
    app.run(debug=True)
