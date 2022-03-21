import os
from io import StringIO, BytesIO

import dask.dataframe as dd
import pandas as pd
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.filedatalake import DataLakeServiceClient

# Imports used for method return definitions:
from azure.storage.filedatalake._file_system_client import FileSystemClient
from azure.storage.filedatalake._data_lake_directory_client import DataLakeDirectoryClient
from pandas.core.frame import DataFrame as DataFrame_pandas
from dask.dataframe.core import DataFrame as DataFrame_dask
from _io import BytesIO

class _AzureCredential:
    """
    Initializes Azure Credential.
    """

    def __init__(self) -> None:
        """Initialize Azure credential."""
        self.credential = DefaultAzureCredential()

class KeyVault(_AzureCredential):
    """
    Get/Set KeyVault secrets.
    """

    def __init__(self, keyVaultName: str) -> None:
        """Initizalize secret client"""

        super().__init__()
        self.keyVaultName = keyVaultName
        KVUri = f"https://{self.keyVaultName}.vault.azure.net"
        self.client = SecretClient(vault_url=KVUri, credential=self.credential)

    def set_secret(self, secretName: str, secretValue: str) -> None:
        """Set KeyVault secret"""

        self.client.set_secret(secretName, secretValue)
        print("Credential set")

    def get_secret(self, secretName: str) -> str:
        """Get KeyVault secret"""

        secret = self.client.get_secret(secretName).value

        return secret

    def delete_secret(self, secretName: str) -> None:
        poller = self.client.begin_delete_secret(secretName)
        deleted_secret = poller.result()

        print("Secret deleted")
    
class DataLake:
    """ Read/write/delete operations to Azure Data Lake"""

    def __init__(self, account_name: str, credential: str) -> None:
        """ Initialize storage account"""
        self.account_name = account_name
        self.credential = credential
        self.service_client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net", credential=credential)

    def _file_system_client(self, file_system: str) -> FileSystemClient:
        """ Initialize ADLS container"""
        file_system_client = self.service_client.get_file_system_client(
            file_system=file_system)
        
        return file_system_client

    def _directory_client(self, file_system: str, directory: str) -> DataLakeDirectoryClient:
        """ Initialize ADLS directory"""
        file_system_client = self._file_system_client(file_system)
        self.directory_client = file_system_client.get_directory_client(
            directory=directory)

        return self.directory_client
    
    def create_container(self, file_system: str) -> None:
        """ Create container"""
        file_system_client = self.service_client.create_file_system(file_system)
        print(f"Container {file_system} created")

    def delete_container(self, file_system: str) -> None:
        """ Delete container"""
        file_system_client = self.service_client.delete_file_system(file_system)
        print(f"Container {file_system} deleted")

    def create_directory(self, file_system: str, directory: str) -> None:
        """ Create directory"""
        file_system_client = self._file_system_client(file_system)
        file_system_client.create_directory(directory)
        print(f"Directory {directory} created")

    def rename_directory(self, file_system: str, directory: str, new_directory: str) -> None:
        """ Rename directory"""
        directory_client = self._directory_client(file_system, directory)
        directory_client.rename_directory(new_name=directory_client.file_system_name + '/' + new_directory)
        print(f"{directory} renamed to {new_directory}")

    def delete_directory(self, file_system: str, directory: str) -> None:
        """ Delete directory"""
        directory_client = self._directory_client(file_system, directory)
        directory_client.delete_directory()
        print(f"{directory} deleted")

    def list_directory_contents(self, file_system: str, directory: str) -> list:
        """ Get list of directory contents"""
        file_system_client = self.service_client.get_file_system_client(file_system)
        paths = file_system_client.get_paths(path=directory)
        paths = [path.name for path in paths]

        return paths

    def upload(self, file_system: str, directory: str, file_name: str, file_path: str, overwrite=True) -> None:
        """ Upload a file to ADLS"""
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)
        with open(file_path, "rb") as data:
            file_client.upload_data(data, overwrite=overwrite)
            print(f"{file_name} write complete")

    def delete_file(self, file_system: str, directory: str, file_name: str) -> None:
        """ Delete file from ADLS"""
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)
        file_client.delete_file()
        print(f"{file_name} deleted")
    
    def download(self, file_system: str, directory: str, file_name: str, path: str) -> None:
        """ Download file to a given path from ADLS"""
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)

        with open(os.path.join(path, file_name), "wb") as data:
            download = file_client.download_file()
            downloaded_bytes = download.readall()
            data.write(downloaded_bytes)
            print(f"{file_name} download complete")

    def read(self, file_system: str, directory: str, file_name: str) -> BytesIO:
        """ Read from ADLS as ByteIO. Returned data can be read directly with pandas read methods"""
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        data = BytesIO(downloaded_bytes)

        return data

    def dask_read(self, file_system: str, directory: str, file_name: str) -> DataFrame_dask:
        """ Read from ADLS using Dask"""
        storage_options = {'account_name': self.account_name, 'account_key': self.credential}
        extension = file_name.split(".")[1]

        if extension == "csv":
            ddf = dd.read_csv(f'abfs://{file_system}/{directory}/{file_name}', storage_options=storage_options)
        elif extension == "parq":
            ddf = dd.read_parquet(f'abfs://{file_system}/{directory}/{file_name}', storage_options=storage_options)
        else:
            pass
            # TODO: Add support for other read operations.

        return ddf

    def pandas_read(self, file_system: str, directory: str, file_name: str) -> DataFrame_pandas:
        """ Read from ADLS using Pandas"""
        extension = file_name.split(".")[1]
        data = self.read(file_system, directory, file_name)

        if extension == "csv":
            df = pd.read_csv(data)
        elif extension == "parq":
            df = pd.read_parquet(data)
        else:
            pass
            # TODO: Add support for other read operations.

        return df