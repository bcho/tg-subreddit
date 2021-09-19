import os


def database_path() -> str:
    """Return database file path."""
    value = os.getenv('DATABASE_PATH')
    if not value:
        raise ValueError('DATABASE_PATH environment variable not set')
    return value