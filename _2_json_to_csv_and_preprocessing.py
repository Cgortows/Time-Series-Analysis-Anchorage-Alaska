import json
import pandas as pd
from pathlib import Path
import numpy as np

# Function to convert temperature from tenths of degrees C to F
def convert_temp_to_fahrenheit(temp_in_tenths_c):
    temp_in_c = temp_in_tenths_c / 10
    return int((temp_in_c * 9/5) + 32) if not np.isnan(temp_in_tenths_c) else 0

# Function to convert precipitation and snowfall from tenths of mm to inches
def convert_precip_and_snow_to_inches(precip_in_tenths_mm):
    precip_in_mm = precip_in_tenths_mm / 10
    return int(precip_in_mm * 0.0393701) if not np.isnan(precip_in_tenths_mm) else 0

# Function to convert wind speed from m/s to mph
def convert_wind_speed_to_mph(wind_speed_in_ms):
    return int(wind_speed_in_ms * 2.23694) if not np.isnan(wind_speed_in_ms) else 0


# Function to process and clean a single JSON file
def process_json_files_in_folder(folder_path):
    folder = Path(folder_path)
    json_files = [f for f in folder.glob("*.json")]
    all_data_frames = []

    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df.drop(columns=['attributes', 'station'], inplace=True)

        df.rename(columns={
            'datatype': 'DataType',
            'date': 'Date',
            'value': 'Value'
        }, inplace=True)

        all_data_frames.append(df)

    return all_data_frames


# Function to post-process the pivoted DataFrame
def post_process_pivoted_df(df):
    new_column_names = {
        'TMAX': 'Temperature_Max',
        'TMIN': 'Temperature_Min',
        'PRCP': 'Precipitation',
        'SNOW': 'Snowfall',
        'AWND': 'Windspeed'
    }
    df.rename(columns=new_column_names, inplace=True)

    df['Temperature_Max'] = df['Temperature_Max'].apply(convert_temp_to_fahrenheit)
    df['Temperature_Min'] = df['Temperature_Min'].apply(convert_temp_to_fahrenheit)
    df['Precipitation'] = df['Precipitation'].apply(convert_precip_and_snow_to_inches)
    df['Snowfall'] = df['Snowfall'].apply(convert_precip_and_snow_to_inches)
    df['Windspeed'] = df['Windspeed'].apply(convert_wind_speed_to_mph)


# Function to combine JSON files to a single CSV
def combine_json_to_csv(folder_path, output_csv_path):
    all_data_frames = process_json_files_in_folder(folder_path)

    if isinstance(all_data_frames, list) and all_data_frames:
        combined_df = pd.concat(all_data_frames)
        pivot_df = combined_df.pivot(index='Date', columns='DataType', values='Value')
        pivot_df.reset_index(inplace=True)

        post_process_pivoted_df(pivot_df)

        pivot_df.to_csv(output_csv_path, index=False)
    else:
        print("No DataFrames to combine or an error occurred.")

folder_path = 'json_file_set_38_years'
output_csv_path = "Anchorage_weather_38_years.csv"
combine_json_to_csv(folder_path, output_csv_path)
