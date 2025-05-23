import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import ruptures as rpt

# 1. Генерація штучного ряду споживання енергії
np.random.seed(0)
n = 200
trend = np.concatenate([np.linspace(10, 20, 100), np.linspace(25, 35, 100)])
seasonal = 2 * np.sin(np.linspace(0, 10 * np.pi, n))
noise = np.random.normal(0, 1, n)
energy = trend + seasonal + noise
dates = pd.date_range(start="2020-01-01", periods=n)
df = pd.DataFrame({'Date': dates, 'Energy': energy}).set_index('Date')

# 2. CUSUM через ruptures
model = rpt.Pelt(model="rbf").fit(df['Energy'].values)
change_points = model.predict(pen=10)

# 3. Seasonal Decompose
decomposition = seasonal_decompose(df['Energy'], model='additive', period=20)
trend_sd = decomposition.trend

# 4. Moving Average
rolling = df['Energy'].rolling(window=10).mean()

# 5. Візуалізація
plt.figure(figsize=(14, 8))

plt.subplot(4,1,1)
plt.plot(df['Energy'], label='Energy Consumption')
plt.title("Original Time Series")
plt.legend()

plt.subplot(4,1,2)
plt.plot(df['Energy'], label='Energy')
for cp in change_points:
    plt.axvline(df.index[cp-1], color='red', linestyle='--', label='Change Point' if cp == change_points[0] else "")
plt.title("CUSUM Change Point Detection")
plt.legend()

plt.subplot(4,1,3)
plt.plot(trend_sd, label='Trend from Seasonal Decompose', color='orange')
plt.title("Trend (Seasonal Decompose)")
plt.legend()

plt.subplot(4,1,4)
plt.plot(rolling, label='Rolling Mean (window=10)', color='green')
plt.title("Moving Average")
plt.legend()

plt.tight_layout()
plt.show()
