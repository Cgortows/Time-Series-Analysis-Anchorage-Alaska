import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv')

# Convert the 'Date' column to a datetime object and set it as the index
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Plot the time series data for TMAX_F
plt.figure(figsize=(15, 6))
plt.plot(df['Temperature_Max'], label='Temperature_Max (°F)', color='b')

# Add horizontal lines at intervals of 20 degrees
for temp in range(-20, 100, 20):
    plt.axhline(y=temp, color='gray', linestyle='--', linewidth=0.5)

# Add vertical lines at intervals of 5 years
for year in range(2018, 2022 + 1, 5):
    plt.axvline(pd.Timestamp(f'{year}-01-01'), color='gray', linestyle='--', linewidth=0.5)

plt.title('Five years of Maximum Temperature in Anchorage')
plt.xlabel('Date')
plt.ylabel('Temperature (°F)')
plt.legend()
plt.savefig('Anchorage_weather_5_years_weekly.jpg')
plt.show()