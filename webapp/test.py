import pandas as pd

df = pd.read_csv('C:\\Users\\mousa\\Desktop\\metadata.csv')

p = df[['site_id','building_id']].groupby(['site_id'],as_index=False).count().rename( \
     columns={'site_id':'Site Name','building_id':'Number of Buildings'})
print(p)