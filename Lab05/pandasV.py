import pandas as pd
import time

start = time.time()
df = pd.read_csv('bigdata.csv')
result = df.groupby('category')['value'].mean()
print(result)
print("Time with pandas:", time.time() - start)
