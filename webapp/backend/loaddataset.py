from utils.azure_utils import KeyVault, DataLake
import pandas as pd
import json

def LoadBasicVisualsData():
    #Specify the key vault we need to connect to
    vault = KeyVault(keyVaultName = "keyvaultdva2022")
    #Get the secret to access the storage
    storage_credential = vault.get_secret(secretName = "storagePrimaryKey")
    #Specify the storage we need to connect to
    storage = DataLake(account_name = "storageaccountdva", credential = storage_credential)
    #Load the file!
    datafile = storage.read(file_system = "energyhub", directory = "/", file_name = "HassanTest.csv", extension = "csv")
    #Convert the dataframe to a json string.
    #Orient = records changes the json slighlty so that it can be read by d3.js
    jsondata = json.loads(datafile.to_json(orient='records'))
    #Return the data.
    return jsondata













