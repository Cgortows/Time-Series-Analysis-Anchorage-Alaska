import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox
from math import sqrt

# Read the last 5 years of weather data from the CSV file
df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv', parse_dates=['Date'], index_col='Date')
df.index.freq = 'W-SUN'

# Set initial SARIMA parameters based Grid Test
best_params_5y = (1, 1, 0)
best_seasonal_params_5y = (0, 1, 1, 52)

# Create a validation set
train = df['Temperature_Max'][:-52]
test = df['Temperature_Max'][-52:]

# Manually set initial parameters
initial_parameters = [0.5,  # AR term
                      0.3,  # Seasonal MA term
                      1.0]  # Variance of the error term

# Refit the model on the training set and forecast the validation set
best_model_refit = SARIMAX(train,
                           order=best_params_5y,
                           seasonal_order=best_seasonal_params_5y)
best_model_refit = best_model_refit.fit(start_params=initial_parameters, disp=False)
forecast = best_model_refit.get_forecast(steps=52).predicted_mean

# Calculate Mean Squared Error on the validation set
mse = round(mean_squared_error(test, forecast), 2)
rmse = round(sqrt(mse), 2)
print(f"Root Mean Square Error: {rmse} degrees Fahrenheit, Mean Square Error: {mse}")

# Show the model summary
print(best_model_refit.summary())

# Plot actual vs predicted values
plt.figure(figsize=(16, 6))
plt.plot(test.index, test, label='Test')
plt.plot(test.index, forecast, label='Forecast')
plt.legend()
plt.title(f"SARIMA Forecast - RMSE: {rmse} degrees Fahrenheit ")
plt.xlabel('Date')
plt.ylabel('Max Temperature')
plt.savefig('refit_sarima_anchorage_5_years.jpg')
plt.show()