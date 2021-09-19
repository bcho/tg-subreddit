import os


database_table_name_reddit_post = "reddit_post"


def database_path() -> str:
    """Database file path to use."""
    value = os.getenv("DATABASE_PATH")
    if not value:
        raise ValueError("DATABASE_PATH environment variable not set")
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
