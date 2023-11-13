import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from math import sqrt

# Data Preprocessing
df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv', parse_dates=['Date'], index_col='Date')

# Filter data to train on data up to the end of 2021 and test on 2022
train_df = df[df.index.year < 2022]
test_df = df[df.index.year == 2022]

X_train = train_df.drop('Temperature_Max', axis=1)
y_train = train_df['Temperature_Max']
X_test = test_df.drop('Temperature_Max', axis=1)
y_test = test_df['Temperature_Max']

# Model Fitting
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Prediction and Evaluation
y_pred = model.predict(X_test)
mse = round(mean_squared_error(y_test, y_pred), 2)
rmse = round(sqrt(mse), 2)
print(f'Mean Squared Error: {mse}')

# Create a DataFrame to hold the actual and predicted values, indexed by date
result_df = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred
}, index=y_test.index)

# Plotting
plt.figure(figsize=(15, 6))
plt.plot(result_df.index, result_df['Actual'], label='Actual')
plt.plot(result_df.index, result_df['Predicted'], label='Predicted', linestyle='--')
plt.xlabel('Date')
plt.ylabel('Max Temperature')
plt.title(f'Random Forest: Actual vs Predicted Max Temperature for 2022, Root Mean Squared Error: {rmse} degrees Fahrenheit')
plt.legend()
plt.savefig('random_forest_predicted_2022.jpg')
plt.show()



