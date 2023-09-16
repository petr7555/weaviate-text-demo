import pandas as pd

from constants import DATA_PATH

df = pd.read_csv(DATA_PATH, converters={'title_vector': lambda x: eval(x)})
print(df.head())
print(f'Number or rows: {len(df)}')
print(f'Length of title_vector: {len(df["title_vector"][0])}')
