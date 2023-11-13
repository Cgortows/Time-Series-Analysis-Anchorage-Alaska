from statsmodels.tsa.stattools import adfuller
import pandas as pd

df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv')

# Function to perform Augmented Dickey-Fuller test
def adf_test(series, title=''):
    print(f'Augmented Dickey-Fuller Test: {title}')
    result = adfuller(series.dropna(), autolag='AIC')

    # Create labels and a pandas series to store test results
    labels = ['ADF Test Statistic', 'p-value', 'Number of lags used', 'Number of observations']
    out = pd.Series(result[0:4], index=labels)

    # Append critical values to the output Series
    for key, val in result[4].items():
        out[f'Critical Value ({key})'] = val
    print(out.to_string())

    if result[1] <= 0.05:
        print("Data has no unit root and is stationary")
    else:
        print("Time series has a unit root, indicating it is non-stationary")


# Check stationarity for Maximum Temperature
adf_test(df['Temperature_Max'], title='Temperature_Max')