import os

import hvac

VAULT_HOST = 'https://vault.entrydsm.hs.kr'
VAULT_DB_CONFIG_STORAGE = 'database/creds/louis-vuitton'
VAULT_SECRET_CONFIG_STORAGE = 'service-secret/{0}/louis-vuitton'


def create_vault_client() -> hvac.Client:
    client = hvac.Client(url=VAULT_HOST)
    client.auth.github.login(
        token=os.getenv(
            'VAULT_TOKEN'
        )
    )

    return client


def get_db_credential_url(env: str) -> str:
    if env == 'production':

        return VAULT_DB_CONFIG_STORAGE + 'prod'

    return VAULT_DB_CONFIG_STORAGE + '-test'


def get_secret_value_url(env: str) -> str:
    env = 'prod' if env == 'production' else 'test'
    return VAULT_SECRET_CONFIG_STORAGE.format(env)


def get_config(env: str) -> dict:
    client = create_vault_client()

    database_credential = client.read(get_db_credential_url(env=env))['data']

    imported_config = {
        'env': env,
        'DATABASE_USERNAME': database_credential.pop('username'),
        'DATABASE_PASSWORD': database_credential.pop('password'),
        **client.read(get_secret_value_url(env=env))['data'],
    }

    return imported_config
