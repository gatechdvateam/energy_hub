from utils.azure_utils import KeyVault, DataLake

def get_data(path, filename, ext):

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
    dataset = storage.read(file_system = "energyhub", directory=path, file_name=filename, extension=ext)

    return dataset


def get_buidling_by_primary_usage(metadata, selected_site):
    """_takes metadata and a selcted site, then return dadaset for sites,
        count of building it has and spage usage_

    Args:
        metadata (_dataFrame_): _description_
        selected_site (_string_): _description_

    Returns:
        _buildings_: _dataFrame_
    """

    # get datafarme
    buildings = metadata[['site_id','building_id', 'primary_space_usage']]


    if (selected_site != None) and (len(selected_site)!=0):
        
        # get builidings from the selected sites
        buildings = buildings.loc[buildings['site_id'].isin(selected_site)]

    # filter buildings that have primary usage listed
    buildings = buildings[buildings['primary_space_usage'].notnull()]

    # Aggregate
    buildings = buildings.groupby(['site_id', 'primary_space_usage'], as_index=False).count()

    # rename the columns
    buildings = buildings.rename(columns={'site_id': 'Site Name',
                                        'building_id': 'Number of Buildings',
                                        'primary_space_usage': 'Space Usage'})
    buildings = buildings.sort_values(by=['Number of Buildings', 'Space Usage'],ascending=False)

    # get builings that have more than 15 sub buildings
    buildings = buildings[buildings['Number of Buildings'] > 15]


    return buildings


def get_buidling_by_secondary_usage(metadata, selected_site):
    """_takes metadata and a selcted site, then return dadaset for sites,
        count of building it has and spage usage_

    Args:
        metadata (_dataFrame_): _description_
        selected_site (_string_): _description_

    Returns:
        _buildings_: _dataFrame_
    """

    # get datafarme
    buildings = metadata[['site_id','building_id', 'sub_primary_space_usage']]


    if (selected_site != None) and (len(selected_site)!=0):
        
        # get builidings from the selected sites
        buildings = buildings.loc[buildings['site_id'].isin(selected_site)]

    # filter buildings that have primary usage listed
    buildings = buildings[buildings['sub_primary_space_usage'].notnull()]

    # Aggregate
    buildings = buildings.groupby(['site_id', 'sub_primary_space_usage'], as_index=False).count()

    # rename the columns
    buildings = buildings.rename(columns={'site_id': 'Site Name',
                                        'building_id': 'Number of Buildings',
                                        'sub_primary_space_usage': 'Space Usage'})
    buildings = buildings.sort_values(by=['Number of Buildings', 'Space Usage'],ascending=False)

    # get builings that have more than 15 sub buildings
    buildings = buildings[buildings['Number of Buildings'] > 15]


    return buildings


# I still dont think this one should be here. Hassan will fight me over this  lol for sure 
metadata = get_data("/data/metadata/", "metadata.csv", "csv")

#TO-DO: we need to turn this to a class