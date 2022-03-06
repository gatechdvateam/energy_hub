from utils.azure_utils import KeyVault, DataLake

def LoadData(dirc, fname, ext):
    #Specify the key vault we need to connect to
    vault = KeyVault(keyVaultName = "keyvaultdva2022")
    #Get the secret to access the storage
    storage_credential = vault.get_secret(secretName = "storagePrimaryKey")
    #Specify the storage we need to connect to
    storage = DataLake(account_name = "storageaccountdva", credential = storage_credential)
    #Load the file!
    datafile = storage.read(file_system = "energyhub", directory = dirc, file_name = fname, extension = ext)
    #Return the data.
    return datafile


MetaData = LoadData("/data/metadata/", "metadata.csv", "csv")
