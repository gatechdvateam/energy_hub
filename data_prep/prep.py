import dask.dataframe as dd
from dask.dataframe.core import DataFrame as DataFrame_dask
from webapp.utils.azure_utils import KeyVault, DataLake
import sys
import os
sys.path.append("..")

# Imports used for method return definitions:

# Connect to Storage Account
vault = KeyVault(keyVaultName="keyvaultdva2022")
storage_credential = vault.get_secret(secretName="storagePrimaryKey")
storage = DataLake(account_name="storageaccountdva",
                   credential=storage_credential)
file_system = "energyhub"


class MeterDataSet:
    """ Read weather, metadata and a select meter, combine features and select which features to use as dask dataframe"""

    def __init__(self, meter: str, metadata_cols: list, weather_cols: list) -> None:
        self.metadata_cols = metadata_cols
        self.weather_cols = weather_cols
        self.metadata = storage.dask_read(
            file_system, directory="data_parq/metadata", file_name="metadata.parq")
        self.weather = storage.dask_read(
            file_system, directory="data_parq/weather", file_name="weather.parq")
        self.meter = storage.dask_read(
            file_system, directory="data_parq/meters", file_name=f"{meter}.parq")
        self.column_filter()  # Filter columns
        self.drop_na()  # drop >24 hour gaps and outliers from meter readings
        self.df = None

    def column_filter(self):
        self.metadata = self.metadata[self.metadata_cols]
        self.weather = self.weather[self.weather_cols]

    def return_data(self) -> DataFrame_dask:
        return self.df

    def select_sites(self, site_ids: list) -> DataFrame_dask:
        return self.df[self.df.site_id.isin(site_ids)]

    def filter_buildings(self, building_ids: list) -> DataFrame_dask:
        return self.df[self.df.building_id.isin(building_ids)]

    def fill_weather_na(self, w_cols: list, fill_method: str) -> DataFrame_dask:
        """
        Fill missing weather data for each site
        """
        sites = self.weather.site_id.unique().compute()
        weather = self.weather.compute()
        dfs = []
        for site in sites:
            df = weather.loc[weather.site_id == site, :]
            df = df.set_index("timestamp")
            for col in w_cols:
                if col == "cloud_coverage":
                    df.loc[:, col] = df.loc[:, col].fillna(method="bfill")
                else:
                    df.loc[:, col] = df.loc[:, col].interpolate(
                        method=fill_method)
            df = df.reset_index()
            dfs.append(df)

        self.weather = dd.concat(dfs)
        return self.weather

    def fill_meter_na(self, meter_col: str, fill_method: str) -> DataFrame_dask:
        """
        Fill missing (Nan) meter readings for each building.
        """
        buildings = self.meter.building_id.unique().compute()
        meter = self.meter.compute()
        dfs = []
        for building in buildings:
            df = meter.loc[meter.building_id == building, :]
            df = df.set_index("timestamp")

            df.loc[:, meter_col] = df.loc[:, meter_col].interpolate(
                method=fill_method)
            df = df.reset_index()
            dfs.append(df)

        self.meter = dd.concat(dfs)
        return self.meter

    def drop_na(self) -> DataFrame_dask:
        self.meter = self.meter.dropna()

    def merge(self):
        self.df = self.meter.merge(self.metadata, how="left", left_on="building_id", right_on="building_id").merge(
            self.weather, how="right", left_on=["site_id", "timestamp"], right_on=["site_id", "timestamp"])
