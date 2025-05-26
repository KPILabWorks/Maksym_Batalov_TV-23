import dask.dataframe as dd
import time

start = time.time()
df = dd.read_csv('bigdata.csv')
result = df.groupby('category')['value'].mean().compute()
print(result)
print("Time with Dask:", time.time() - start)
