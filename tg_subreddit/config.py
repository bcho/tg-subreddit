import os


database_table_name_reddit_post = "reddit_post"

database_driver_sqlite = 'sqlite'
database_driver_sqlite_rest = 'sqlite-rest'
_supported_database_drivers = (database_driver_sqlite, database_driver_sqlite_rest)


def database_driver() -> str:
    """Database driver to use."""
    value = os.getenv("DATABASE_DRIVER") or database_driver_sqlite
    if value not in _supported_database_drivers:
        raise ValueError("DATABASE_DRIVER environment variable not set to 'sqlite' or 'sqlite-rest'")
    return value


def database_path() -> str:
    """Database file path to use."""
    value = os.getenv("DATABASE_PATH")
    if not value:
        raise ValueError("DATABASE_PATH environment variable not set")
    return value

    
def database_sqlite_rest_url() -> str:
    """Sqlite-rest base url to use."""
    value = os.getenv("DATABASE_SQLITE_REST_BASE_URL")
    if not value:
        raise ValueError("DATABASE_SQLITE_REST_BASE_URL environment variable not set")
    return value


def database_sqlite_rest_table_name() -> str:
    """Sqlite-rest table name to use."""
    value = os.getenv("DATABASE_SQLITE_REST_TABLE_NAME")
    if not value:
        raise ValueError("DATABASE_SQLITE_REST_TABLE_NAME environment variable not set")
    return value


def database_sqlite_rest_token() -> str:
    """Sqlite-rest token to use."""
    value = os.getenv("DATABASE_SQLITE_REST_TOKEN")
    if not value:
        raise ValueError("DATABASE_SQLITE_REST_TOKEN environment variable not set")
    return value


def reddit_client_id() -> str:
    """Client id of the reddit app."""
    value = os.getenv("REDDIT_CLIENT_ID")
    if not value:
        raise ValueError("REDDIT_CLIENT_ID environment variable not set")
    return value


def reddit_client_secret() -> str:
    """Client secret of the reddit app."""
    value = os.getenv("REDDIT_CLIENT_SECRET")
    if not value:
        raise ValueError("REDDIT_CLIENT_SECRET environment variable not set")
    return value


def reddit_client_user_agent() -> str:
    """Client user agent of the reddit app."""
    value = os.getenv("REDDIT_CLIENT_USER_AGENT")
    if not value:
        value = "b4fun/tg-subreddit"
    return value


def telegram_bot_token() -> str:
    """Token of the telegram bot."""
    value = os.getenv("TELEGRAM_BOT_TOKEN")
    if not value:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    return value
