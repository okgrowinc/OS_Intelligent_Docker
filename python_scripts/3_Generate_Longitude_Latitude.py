import pandas as pd
from geopy.geocoders import Nominatim
import time
import logging

# Configure logging
logging.basicConfig(filename='error_logs/geospatial_errors.txt', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Function to get latitude and longitude using Geopy
def get_latitude_longitude(city_and_country):
    geolocator = Nominatim(user_agent="my-custom-user-agent", timeout=10)
    try:
        location = geolocator.geocode(city_and_country)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        logging.error(f"Error: {e} - Could not find coordinates for {city_and_country}")
    return None, None

# Read the Excel file
input_file = 'input_data/input_Generate_Long_Lat.xlsx'
df = pd.read_excel(input_file)

# Initialize longitude and latitude columns with None
df['longitude'] = None
df['latitude'] = None

# Iterate over the DataFrame, updating the longitude and latitude columns
for index, row in df.iterrows():
    city_and_country = row['city_and_country']
    lat, lon = get_latitude_longitude(city_and_country)
    df.at[index, 'latitude'] = lat
    df.at[index, 'longitude'] = lon

    # Sleep for 1 second to avoid overloading the geocoding service
    time.sleep(1)

# Save the updated DataFrame to a new Excel file
output_file = 'output.xlsx'
df.to_excel(output_file, index=False)
