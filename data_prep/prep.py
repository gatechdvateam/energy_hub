import sys
import os
sys.path.append("..")
from webapp.utils.azure_utils import KeyVault, DataLake

# Imports used for method return definitions:
from dask.dataframe.core import DataFrame as DataFrame_dask

# Connect to Storage Account
vault = KeyVault(keyVaultName = "keyvaultdva2022")
storage_credential = vault.get_secret(secretName = "storagePrimaryKey")
storage = DataLake(account_name = "storageaccountdva", credential = storage_credential)
file_system = "energyhub"


class MeterDataSet:
    """ Read weather, metadata and a select meter, combine features and select which features to use as dask dataframe"""
    def __init__(self, meter: str, metadata_cols: list, weather_cols: list) -> None:
        self.metadata_cols = metadata_cols
        self.weather_cols = weather_cols
        self.metadata = storage.dask_read(file_system, directory = "data_parq/metadata", file_name = "metadata.parq")
        self.weather = storage.dask_read(file_system, directory = "data_parq/weather", file_name = "weather.parq")
        self.meter = storage.dask_read(file_system, directory = "data_parq/meters", file_name = f"{meter}.parq")
        self.column_filter() # Filter columns
        self.df = None
    
    def column_filter(self):
        self.metadata = self.metadata[self.metadata_cols]
        self.weather = self.weather[self.weather_cols]

    def return_data(self) -> DataFrame_dask:
        return self.df

    def filter_sites(self, site_ids: list) -> DataFrame_dask:
        return self.df[self.df.site_id.isin(site_ids)]

    def filter_buildings(self, building_ids: list) -> DataFrame_dask:
        return self.df[self.df.building_id.isin(building_ids)]

    def merge(self):
        self.df = self.meter.merge(self.metadata, how = "left", left_on = "building_id", right_on = "building_id").merge(self.weather, how = "right", left_on = ["site_id", "timestamp"], right_on = ["site_id", "timestamp"])
