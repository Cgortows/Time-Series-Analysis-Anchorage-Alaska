import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Data Preprocessing
df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv', parse_dates=['Date'], index_col='Date')

# Uncomment each engineered feature one at a time to evaluate its effectiveness
# df['Temp_Precip'] = df['Temperature_Max'] * df['Precipitation']
# df['Temp_Snowfall'] = df['Temperature_Max'] * df['Snowfall']
# df['Temp_Windspeed'] = df['Temperature_Max'] * df['Windspeed']
df['Temp_Max_Min'] = df['Temperature_Max'] * df['Temperature_Min']

# Data Splitting
X = df.drop('Temperature_Max', axis=1)
y = df['Temperature_Max']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Fitting
# model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Prediction and Evaluation
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Feature Importance
feature_importances = model.feature_importances_
feature_names = X_train.columns
feature_dict = dict(zip(feature_names, feature_importances))
sorted_features = {k: v for k, v in sorted(feature_dict.items(), key=lambda item: item[1], reverse=True)}

print("Feature importances:")
for feature, importance in sorted_features.items():
    print(f"{feature}: {importance}")