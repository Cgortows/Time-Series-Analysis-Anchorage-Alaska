import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm
from scipy.stats import jarque_bera
from _9_fit_sarima_original_anchorage import best_model_refit

# Get the residuals
model = best_model_refit
residuals = model.resid

# Calculate mean and variance, Jarque-Bera Test for Normality
mean_residual = np.mean(residuals)
variance_residual = np.var(residuals)
jb_stat, jb_pvalue = jarque_bera(residuals)

print(f"Mean of Residuals: {mean_residual}")
print(f"Variance of Residuals: {variance_residual}")
print(f"Jarque-Bera statistic: {jb_stat}")
print(f"Jarque-Bera p-value: {jb_pvalue}")


# Plot the residuals
plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
plt.plot(residuals.index, residuals, label='Residuals')
plt.axhline(0, color='r', linestyle='--', label='Zero Line')
plt.xlabel('Date')
plt.ylabel('Residuals')
plt.title('Time Series of Residuals')
plt.legend()

# Plot histogram of residuals
plt.subplot(1, 2, 2)
plt.hist(residuals, bins=20, edgecolor='black')
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('sarima_residuals__anchorage_5_years.jpg')
plt.show()