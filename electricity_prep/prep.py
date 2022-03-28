import sys
import os
sys.path.append("..")
from webapp.utils.azure_utils import KeyVault, DataLake

# Connect to Storage Account
vault = KeyVault(keyVaultName = "keyvaultdva2022")
storage_credential = vault.get_secret(secretName = "storagePrimaryKey")
storage = DataLake(account_name = "storageaccountdva", credential = storage_credential)
file_system = "energyhub"


class MeterDataSet:
    def __init__(self, site_id: str, meter: str, metadata_cols: list, weather_cols: list) -> None:
        self.site_id = site_id
        self.metadata_cols = metadata_cols
        self.weather_cols = weather_cols
        self.metadata = storage.dask_read(file_system, directory = "data_parq/metadata", file_name = "metadata.parq")
        self.weather = storage.dask_read(file_system, directory = "data_parq/weather", file_name = "weather.parq")
        self.meter = storage.dask_read(file_system, directory = "data_parq/meters", file_name = f"{meter}.parq")
        self.prep_metadata()
        self.prep_weather()

    def prep_metadata(self):
        df = self.metadata
        cols = self.metadata_cols
        # Filter site_id and columns
        df = df[df.site_id == self.site_id][cols]

        self.metadata = df

    def prep_weather(self):
        df = self.weather
        cols = self.weather_cols
        # Filter site_id and columns
        df = df[df.site_id == self.site_id][cols]

        self.weather = df


# Read meta
# Read electricity
# Read weather
# Merge datasets for a select building
# Select features to use
# Change datatypes
# Filter
# Outlier removal
# Fill missing data
# Save