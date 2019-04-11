import os

import hvac

VAULT_HOST = 'https://vault.entrydsm.hs.kr'
VAULT_DB_CONFIG_STORAGE = 'database/creds/louis-vuitton-test'
VAULT_SECRET_CONFIG_STORAGE = 'service-secret/test/louis-vuitton'


def create_vault_client() -> hvac.Client:
    client = hvac.Client(url=VAULT_HOST)
    client.auth.github.login(token=os.getenv('VAULT_TOKEN', '009cbcecbc5238dcccb43e60a806fe98c88c59c6'))

    return client


def get_config(env: str) -> dict:
    client = create_vault_client()

    database_credential = client.read(VAULT_DB_CONFIG_STORAGE)['data']

    imported_config = {
        'env': env,
        'DATABASE_USERNAME': database_credential.pop('username'),
        'DATABASE_PASSWORD': database_credential.pop('password'),
        **client.read(VAULT_SECRET_CONFIG_STORAGE)['data'],
    }

    return imported_config
