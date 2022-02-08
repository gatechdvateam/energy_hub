#This file is a copy from the main file mert created.
#Please keep it here because when we upload the app to azure this file gets uploaded with it.
from io import StringIO
from numpy import iterable, object_
import pandas as pd
import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.filedatalake import DataLakeServiceClient
from zmq import PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_UNSPECIFIED


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

    def get_secret(self, secretName: str) -> str:
        """Get KeyVault secret"""

        secret = self.client.get_secret(secretName).value

        return secret

    def set_secret(self, secretName: str, secretValue: str) -> None:
        """Set KeyVault secret"""

        self.client.set_secret(secretName, secretValue)
        print("Credential set")


class DataLake:
    """ Read/write/delete operations to Azure Data Lake"""

    def __init__(self, account_name: str, credential: str) -> None:
        """ Initialize storage account"""
        self.service_client = DataLakeServiceClient(
            account_url=f"https://{account_name}.dfs.core.windows.net", credential=credential)

    def _directory_client(self, file_system: str, directory: str) -> "DataLakeDirectoryClient":
        """ Initialize ADLS directory"""
        file_system_client = self.service_client.get_file_system_client(
            file_system=file_system)
        self.directory_client = file_system_client.get_directory_client(
            directory=directory)

        return self.directory_client

    def read(self, file_system: str, directory: str, file_name: str, extension="csv") -> pd.DataFrame:
        """ Read csv file from ADLS and return as pd.DataFrame"""
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        if extension == "csv":
            s = str(downloaded_bytes, 'utf-8')
            data = StringIO(s)
            df = pd.read_csv(data)
        else:
            pass
            # TODO: Add support for other read operations

        return df

    def write(self, file_system: str, directory: str, file: pd.DataFrame, file_name: str, extension="csv", overwrite=True) -> None:
        """ Write csv file to ADLS"""
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)
        if extension == "csv":
            file_contents = file.to_csv(index=False)
            file_client.upload_data(file_contents, overwrite=overwrite)
            print(f"{file_name} write complete")
        else:
            pass
            # TODO: Add support for other write operations

    def upload(self, file_system: str, directory: str, file_name: str, file_path: str, overwrite=True) -> None:
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)
        with open(file_path, "rb") as data:
            file_client.upload_data(data, overwrite=overwrite)
            print(f"{file_name} write complete")

    def delete(self, file_system: str, directory: str, file_name: str) -> None:
        """ Delete file from ADLS"""
        directory_client = self._directory_client(file_system, directory)
        file_client = directory_client.get_file_client(file=file_name)
        file_client.delete_file()
        print(f"{file_name} deleted")

    def list_directory_contents(self, file_system: str, directory: str, print_paths=False):
        """
        Get the count of directory contents. Optionally, print out the contents
        """
        file_system_client = self.get_file_system_client(file_system)
        paths = file_system_client.get_paths(path=directory)
        print(len(paths))

        if print_paths:
            for path in paths:
                print(path.name + '\n')
