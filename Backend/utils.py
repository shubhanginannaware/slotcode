import os
import psycopg2

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Replace with actual values if not using environment variables
KEY_VAULT_URI = "https://shubhangi-key-vault.vault.azure.net/"


def connect_to_db():
    """Connects to the PostgreSQL database using environment variables and Key Vault.

    Retrieves database connection details from environment variables and fetches
    the password from Azure Key Vault using a client credential.

    Returns:
        psycopg2.connection object on successful connection, None otherwise.
    """

    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    dbname = os.getenv("POSTGRES_DBNAME")
    user = os.getenv("POSTGRES_USER")

    # Get Key Vault details from environment variables (preferred)
    key_vault_uri = os.getenv("KEY_VAULT_URI")
    client_id = os.getenv("CLIENT_ID")

    # Use provided values if environment variables aren't set (optional)
    if not key_vault_uri:
        key_vault_uri = KEY_VAULT_URI  # Correct indentation here

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)

    try:
        secret = client.get_secret("POSTGRES_PASSWORD")  # Replace with your secret name
        password = secret.value
    except Exception as error:
        print(f"Error retrieving secret from Key Vault: {error}")
        return None

    sslmode = "require"

    connection_string = f"host={host} port={port} dbname={dbname} user={user} password={password} sslmode={sslmode}"

    try:
        connection = psycopg2.connect(connection_string)
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL database:", error)
        return None
