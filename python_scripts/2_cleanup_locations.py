import pandas as pd
import re
import logging

# Configure logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Load Excel spreadsheet into a pandas DataFrame
df = pd.read_excel('input_data/input_cleanup_locations.xlsx')

# Define function to format location names
def format_location(location, country):
    if pd.isna(location):
        return ''
    
    location = location.strip()
    location = location.replace(country, '')
    location = location.lower()
    location = re.sub(r'[^a-zA-Z0-9\s\-\'"]+', '', location)
    location = ' '.join(word.capitalize() for word in location.split())
    
    return location

# Apply the format_location function to the 'location' column of the DataFrame
df['location'] = df.apply(lambda row: format_location(row['location'], row['Country']), axis=1)
df['location2'] = df.apply(lambda row: format_location(row['location2'], row['Country']), axis=1)

# Define function to create city_and_country column
def create_city_and_country(row):
    if not row['location'] and not row['location2']:
        return None
    if row['Country'] in row['location']:
        return row['location']
    elif row['Country'] in row['location2']:
        return row['location2']
    else:
        return row['location2'] + ', ' + row['Country']

# Apply the create_city_and_country function to each row of the DataFrame
df['city_and_country'] = df.apply(create_city_and_country, axis=1)

# Save the updated DataFrame to a new Excel spreadsheet
df.to_excel('input_data/input_Generate_Long_Lat.xlsx', index=False)
