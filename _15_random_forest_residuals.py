import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import shapiro
from _14_rolling_forcaast_forest_anchorage import y_test
from _14_rolling_forcaast_forest_anchorage import y_pred

predictions = y_pred
residuals = y_test - predictions

# Graphical Methods
plt.figure(figsize=(12, 6))
train_size = len(df) - 52

# Residuals vs Predicted values
plt.subplot(1, 3, 1)
plt.scatter(predictions, residuals)
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted Values')

# Histogram of Residuals
plt.subplot(1, 3, 2)
plt.hist(residuals, bins=30)
plt.xlabel('Residuals')
plt.title('Histogram of Residuals')

# Time Series plot of Residuals
plt.subplot(1, 3, 3)
plt.plot(residuals)
plt.xlabel('Time')
plt.ylabel('Residuals')
plt.title('Time Series Plot of Residuals')

plt.tight_layout()
plt.savefig('Residual_Graphs.jpg')
plt.show()

# Numerical Methods
print(f"Mean of residuals: {np.mean(residuals)}")
print(f"Standard Deviation of residuals: {np.std(residuals)}")

# Shapiro-Wilk Test for normality
stat, p_value = shapiro(residuals)
print(f"Shapiro-Wilk Test P-value: {p_value}")