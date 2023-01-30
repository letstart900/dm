import pandas as pd
from itertools import combinations

df2 = pd.read_csv(r'Z:\datam\trans.csv')
df2 = df2.drop(df2[df2.Item == "NONE"].index)
df2['Datetime'] = pd.to_datetime(df2["Date"]+' '+df2["Time"])
main_df = df2[['Datetime','Item']].groupby(['Datetime'])['Item'].apply(list)
transactions = list(main_df)
transactions
