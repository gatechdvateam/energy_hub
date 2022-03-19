from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from data import *
from content import *


def createLayout():
    # Specify the key vault we need to connect to
    vault = KeyVault(keyVaultName="keyvaultdva2022")
    # Get the secret to access the storage
    storage_credential = vault.get_secret(secretName="storagePrimaryKey")
    # Specify the storage we need to connect to
    storage = DataLake(account_name="storageaccountdva", credential=storage_credential)
    # read the file
    dataset = storage.read(file_system = "energyhub", directory="/data_parq_partitioned/", file_name="electricity.parq", extension="parq")
    ddf_1 = dd.read_parquet("ParitionedParquets/electricity.parq", filters=[("building_id", "==", "Panther_education_Misty")])
    ddf_1.groupby(ddf_1.timestamp.dt.year).sum().compute().reset_index()
    return ""