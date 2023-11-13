import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


# Read the last 5 years of weather data from the CSV file
df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv', parse_dates=['Date'], index_col='Date')
df.index.freq = 'W-SUN'
last_5_years_data = df['Temperature_Max']  # Assuming you want to drop NA values

# Set initial SARIMA parameters based on ACF and PACF
p, d, q = 1, 0, 0  # Non-seasonal parameters
P, D, Q, S = 0, 1, 1, 52  # Seasonal parameters

# Manually set initial parameters
initial_parameters = [0.5,  # AR term
                      0.3,  # Seasonal MA term
                      1.0]  # Variance of the error term

# Fit the SARIMA model
model = SARIMAX(last_5_years_data, order=(p, d, q), seasonal_order=(P, D, Q, S))
results = model.fit(start_params=initial_parameters, disp=False)

# Show the model summary
print(results.summary())
