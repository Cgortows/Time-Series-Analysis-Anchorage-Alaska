import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from math import sqrt

# Data Preprocessing
df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv', parse_dates=['Date'], index_col='Date')
df['Temp_Max_Min'] = df['Temperature_Max'] * df['Temperature_Min']

# Prepare training and test data
train_size = len(df) - 52  # last 52 weeks as test set, for example
X_train = df.iloc[:train_size].drop('Temperature_Max', axis=1).values
X_test = df.iloc[train_size:].drop('Temperature_Max', axis=1).values
y_train = df.iloc[:train_size]['Temperature_Max'].values
y_test = df.iloc[train_size:]['Temperature_Max'].values

# Initialize predictions list
y_pred = []

# Walk-forward validation: refit model for each new observation
for i in range(len(X_test)):
    model = RandomForestRegressor(n_estimators=200, max_depth=20, min_samples_leaf=2, min_samples_split=2,
                                  random_state=42)
    model.fit(X_train, y_train)
    single_pred = model.predict([X_test[i]])
    y_pred.append(single_pred[0])

    # Update the training set
    X_train = np.vstack([X_train, [X_test[i]]])
    y_train = np.append(y_train, y_test[i])

# Calculate MSE
mse = round(mean_squared_error(y_test, y_pred), 2)
rmse = round(sqrt(mse), 2)
print(f'Mean Squared Error: {mse}')

# Convert predictions to a pandas Series for plotting
y_pred_series = pd.Series(y_pred, index=df.iloc[train_size:].index)

# Plot
plt.figure(figsize=(15, 6))
plt.plot(df.iloc[train_size:].index, y_test, label='Actual in 2022', color='green')
plt.plot(df.iloc[train_size:].index, y_pred_series, label='Predicted for 2022', color='red')
plt.title(f'Random Forest: Actual vs Predicted Max Temperature for 2022, Root Mean Squared Error: {rmse} degrees Fahrenheit')
plt.xlabel('Date')
plt.ylabel('Max Temperature')
plt.legend()
plt.savefig('rolling_forecast_anchorage_5_years.jpg')
plt.show()