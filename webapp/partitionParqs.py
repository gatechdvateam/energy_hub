
#import Libraries
from importlib_metadata import files
import pandas as pd

# Setup file name
files = ['electricity.parq', 'chilledwater.parq', 'gas.parq','steam.parq',
         'hotwater.parq', 'irrigation.parq', 'solar.parq', 'water.parq', ]

for name in files:
    # Read the file
    df = pd.read_parquet(name)

    # Print
    print(df.head())
    print(df.dtypes)

    # Save with the repartitions
    df.to_parquet('PartitionedParquets\\'+name, partition_cols=["building_id"])

    print('done')

name = 'weather.parq'
df = pd.read_parquet(name)
# Print
print(df.head())
print(df.dtypes)

# Save with the repartitions
df.to_parquet('PartitionedParquets\\'+name, partition_cols=["site_id"])

print('done')