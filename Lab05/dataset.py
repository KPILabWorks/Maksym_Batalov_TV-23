import pandas as pd
import numpy as np

n_rows = 10**6  # 1 мільйон рядків
df = pd.DataFrame({
    'id': np.arange(n_rows),
    'value': np.random.rand(n_rows) * 1000,
    'category': np.random.choice(['A', 'B', 'C', 'D'], size=n_rows)
})
df.to_csv('bigdata.csv', index=False)
