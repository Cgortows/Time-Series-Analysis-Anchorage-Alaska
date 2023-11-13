import pandas as pd
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm

# Read the last 5 years of weather data from the CSV file
df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv', parse_dates=['Date'], index_col='Date')
df.index.freq = 'W-SUN'

# Focus on the 'Temperature_Max' column
last_5_years_data = df['Temperature_Max']

# Create a validation set
train = last_5_years_data[:-52]
test = last_5_years_data[-52:]

# Align the exog_data with the train and test sets
exog_train = df['Windspeed'][:-52]
exog_test = df['Windspeed'][-52:]

# Parameter grid for SARIMA model
p_values = [0, 1]
d_values = [0, 1]
q_values = [0, 1]
P_values = [0, 1]
D_values = [0, 1]
Q_values = [0, 1]
S_values = [52]

best_score = float('inf')

# Grid Search
for p in p_values:
    for d in d_values:
        for q in q_values:
            for P in P_values:
                for D in D_values:
                    for Q in Q_values:
                        for S in S_values:
                            try:
                                model = sm.tsa.statespace.SARIMAX(train, exog=exog_train, order=(p,d,q), seasonal_order=(P,D,Q,S))
                                # model = SARIMAX(train, order=(p,d,q), seasonal_order=(P,D,Q,S))
                                fit_model = model.fit(disp=False)
                                predictions = fit_model.get_forecast(steps=len(test), exog=exog_test).predicted_mean
                                # predictions = fit_model.predict(start=len(train), end=len(train) + len(test) - 1)
                                mse = mean_squared_error(test, predictions)
                                if mse < best_score:
                                    best_score = mse
                                    best_params = ((p,d,q), (P,D,Q,S))
                            except:
                                continue

print('Best MSE:', best_score)
print('Best Params:', best_params)