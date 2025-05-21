import pandas as pd
import numpy as np
import hashlib
import time
from joblib import Memory

memory = Memory(location='cache_dir', verbose=0)

# Hash dataframe
def hash_df(df):
    df_bytes = pd.util.hash_pandas_object(df, index=True).values
    return hashlib.md5(df_bytes).hexdigest()

@memory.cache
def heavy_processing_cached(df_hash):
    print("Heavy processing at time:", time.strftime("%H:%M:%S", time.localtime()))
    time.sleep(5)  # Уявна довга обробка
    result = df.copy()
    result['new_col'] = np.sqrt(result['value'])
    return result

df = pd.DataFrame({
    'id': np.arange(1, 1_000_001),
    'value': np.random.rand(1_000_000) * 100
})

df_hash = hash_df(df)
processed_df = heavy_processing_cached(df_hash)
processed_df2 = heavy_processing_cached(df_hash)

print(processed_df2.head())