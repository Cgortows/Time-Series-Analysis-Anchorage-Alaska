import pandas as pd

# Load the dataset
df = pd.read_csv('Anchorage_weather_38_years.csv')

# Convert the 'Date' column to datetime format and set it as the index
df = pd.read_csv('Anchorage_weather_38_years.csv')

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Resample the data to weekly frequency, taking the mean for each week
df_weekly = df.resample('W').mean().round(2)

# Save the weekly data to a new CSV file
df_weekly.to_csv('Anchorage_weather_38_years_weekly.csv')