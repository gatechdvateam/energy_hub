from utils.azure_utils import KeyVault, DataLake

def get_dask_data(path, filename):

    """_loads the data from Azure Data lake_
    Args:
        path (_string_): _path in Azure storage_
        filename (_string_): _Name of the file_
        ext (_string_): _extention of the file_

    Returns:
        _dataset_: _a file.ext_
    """
  
    # Specify the key vault we need to connect to
    vault = KeyVault(keyVaultName="keyvaultdva2022")
    
    # Get the secret to access the storage
    storage_credential = vault.get_secret(secretName="storagePrimaryKey")
    
    # Specify the storage we need to connect to
    storage = DataLake(account_name="storageaccountdva", credential=storage_credential)
    
    # read the file
    dataset = storage.dask_read(file_system = "energyhub", directory=path, file_name=filename)

    return dataset

def get_data(path, filename):

    """_loads the data from Azure Data lake_
    Args:
        path (_string_): _path in Azure storage_
        filename (_string_): _Name of the file_
        ext (_string_): _extention of the file_

    Returns:
        _dataset_: _a file.ext_
    """
  
    # Specify the key vault we need to connect to
    vault = KeyVault(keyVaultName="keyvaultdva2022")
    
    # Get the secret to access the storage
    storage_credential = vault.get_secret(secretName="storagePrimaryKey")
    
    # Specify the storage we need to connect to
    storage = DataLake(account_name="storageaccountdva", credential=storage_credential)
    
    # read the file
    dataset = storage.pandas_read(file_system = "energyhub", directory=path, file_name=filename)

    return dataset


def get_buidling_by_space_usage(metadata, space_usage, selected_site):
    """_takes metadata and a selected site, then return dadaset for sites,
        count of building it has and spage usage_

    Args:
        metadata (_dataFrame_): _description_
        selected_site (_string_): _description_

    Returns:
        _buildings_: _dataFrame_
    """

    # get datafarme
    buildings = metadata[['site_id','building_id', space_usage]]


    if (selected_site != None) and (len(selected_site)!=0):
        
        # get builidings from the selected sites
        buildings = buildings.loc[buildings['site_id'].isin(selected_site)]

    # filter buildings that have primary usage listed
    buildings = buildings[buildings[space_usage].notnull()]

    # Aggregate
    buildings = buildings.groupby(['site_id', space_usage], as_index=False).count()

    # rename the columns
    buildings = buildings.rename(columns={'site_id': 'Sites',
                                        'building_id': 'Number of Buildings',
                                        space_usage: 'Space Usage'})
    buildings = buildings.sort_values(by=['Number of Buildings', 'Space Usage'],ascending=False)

    # get builings that have 10  or more buildings
    buildings = buildings[buildings['Number of Buildings'] >= 10]


    return buildings


def get_meter_data_for_building(MeterName,BuildingName):
    """
    Returns a dask dataframe from the folder of the partitioned parqs on Azure Storage.
    """
    location = "PartitionedParqs/"+MeterName+'.parq/building_id='+BuildingName
    meterdata = get_dask_data(location, "*.parquet")
    return meterdata


# Preload Small Datasets here.
BuildingMetadata = get_data("/data_parq/metadata/", "metadata.parq").reset_index().copy()
weatherDate = get_data("/data_parq/weather/", "weather.parq").reset_index().copy()