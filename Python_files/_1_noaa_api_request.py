import requests
import json
from time import sleep
import us

# Define the station, years, data types, and header
station_id = 'GHCND:USW00026451'
years = range(1985, 2023)
data_types = 'TMAX,TMIN,PRCP,SNOW,AWND'
headers = {'token': 'token'}

def get_all_fips():
    fips_codes = {}
    for state in us.STATES:
        fips_codes[state.name] = state.fips
    for state, fips in fips_codes.items():
        print(f"{state}: {fips}")


def fetch_station_ids(city, state, token):
    url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/stations"
    headers = {"token": token}
    params = {"locationid": f"FIPS:{state}", "limit": 1000}  # You can adjust the limit as needed
    response = requests.get(url, headers=headers, params=params)

    # In case of error
    if response.status_code != 200:
        print(f"Failed to get data: {response.status_code}")
        return

    data = response.json()
    city_stations = []
    for station in data.get('results', []):
        if city.lower() in station.get('name', '').lower():
            station_info = {'id': station['id'], 'name': station['name']}
            city_stations.append(station_info)
    for station_info in city_stations:
        print(f"ID: {station_info['id']}, Location: {station_info['name']}")


# Split the data so as to not hit the max pull rate for NOAA of 1000
first_half = [(f"{year}-01-01", f"{year}-06-30") for year in years]
second_half = [(f"{year}-07-01", f"{year}-12-31") for year in years]
all_ranges = list(zip(first_half, second_half))

# Fetch data for each year, divided into two parts
def pull_weather_data():
    for (start1, end1), (start2, end2) in all_ranges:
        all_data = []

        for start, end in [(start1, end1), (start2, end2)]:
            base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/data"
            params = {
                'stationid': station_id,
                'datasetid': 'GHCND',
                'startdate': start,
                'enddate': end,
                'datatypeid': data_types,
                'limit': 1000
            }
            response = requests.get(base_url, headers=headers, params=params)

            # In case of error
            if response.status_code == 200:
                data = response.json().get('results', [])
                all_data.extend(data)
            else:
                print(f"Failed to get data for {start} to {end}")

            # Wait for a second before the next API request to avoid rate-limiting
            sleep(1)

        # Save the data to a separate JSON file for each year
        year = start1.split("-")[0]
        filename = f'anchorage_weather_data_{year}.json'
        with open(filename, 'w') as f:
            json.dump(all_data, f)
        print(f"Saved data to {filename}")


get_all_fips()
fetch_station_ids('Anchorage', '02', 'token')
pull_weather_data()


