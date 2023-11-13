import pandas as pd
from statsmodels.graphics.tsaplots import plot_pacf
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('CSV/Anchorage_weather_5_years_weekly.csv', parse_dates=['Date'], index_col='Date')
temp_max_series = df['Temperature_Max']

# PACF plot
plot_pacf(temp_max_series, lags=104)
plt.title('Partial AutoCorrelation Function (PACF)')
plt.savefig('pacf_test.jpg')

plt.show()
