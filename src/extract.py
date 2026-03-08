'''
PART 1: EXTRACT WEATHER AND TRANSIT DATA

Pull in data from two dataset
1. Weather data from visualcrossing's weather API (https://www.visualcrossing.com/weather-api)
- You will need to sign up for a free account to get an API key
-- You only get 1000 rows free per day, so be careful to build your query correctly up front
-- Though not best practice, include your API key directly in your code for this assignment
- Write code below to get weather data for Chicago, IL for the date range 10/1/2024 - 10/31/2025
- The default data fields should be sufficient
2. Daily transit ridership data for the Chicago Transit Authority (CTA)
- Here is the URL: https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"

Load both as CSVs into /data
- Make sure your code is line with the standards we're using in this class 
'''

#Write your code below

import urllib.request
import urllib.error
import csv
import pandas as pd
import sys

def extract_weather_data():
    # Define the API endpoint and query parameters
    base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'
    location = 'Chicago,IL'
    start_date = '2024-10-01'
    end_date = '2025-10-31'
    api_key = 'FWG5VWAYLJK8NMY6Q44SXSHL2'
    unit_group = 'us'
    content_type = 'csv'
    include = 'days'

    # Construct the URL
    timeline_url = f"{base_url}{location}/{start_date}/{end_date}?unitGroup={unit_group}&include={include}&contentType={content_type}&key={api_key}"

    try:
        # Make the HTTP request
        with urllib.request.urlopen(timeline_url) as response:
            # Read and decode the response content
            csv_data = response.read().decode('utf-8')

        # Split the CSV data into lines and parse it with pandas
        data_lines = csv_data.splitlines()
        reader = csv.reader(data_lines)
        headers = next(reader)
        data = list(reader)
        weather_data = pd.DataFrame(data, columns=headers)
        return weather_data

    except urllib.error.HTTPError as e:
        print(f'HTTP error: {e.code} - {e.reason}')
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f'URL error: {e.reason}')
        sys.exit(1)
    except Exception as e:
        print(f'General error: {str(e)}')
        sys.exit(1)

# Extract CTA transit ridership data
def extract_transit_data():
    url="https://data.cityofchicago.org/api/views/6iiy-9s97/rows.csv?accessType=DOWNLOAD"
    df=pd.read_csv(url)
    return df

