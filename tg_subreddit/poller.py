from loguru import logger
import praw
import random
import time
from typing import Callable

from . import config
from .models import RedditPostPollSettingsGroup
from .reddit import RedditPostPoller
from .reddit import RedditPostStorageSqlite
from .reddit import RedditPostStorageSqliteRest
from .telegram import TelegramBot


logger = logger.bind(service="poller")


def main(get_settings: Callable[[], RedditPostPollSettingsGroup]):
    reddit_client = praw.Reddit(
        client_id=config.reddit_client_id(),
        client_secret=config.reddit_client_secret(),
        user_agent=config.reddit_client_user_agent(),
    )

    db_driver =  config.database_driver()
    if db_driver == config.database_driver_sqlite_rest:
        storage = RedditPostStorageSqliteRest(
            base=config.database_sqlite_rest_url(),
            table_name=config.database_sqlite_rest_table_name(),
            auth_token=config.database_sqlite_rest_token(),
        )
    else:
        storage = RedditPostStorageSqlite(db_path=config.database_path())

    poller = RedditPostPoller(
        reddit_client=reddit_client,
        storage=storage,
    )

    telegram_bot = TelegramBot(config.telegram_bot_token())

    while True:
        logger.debug("start polling")
        start_at = time.time()

        settings = get_settings()

        for subreddit_settings in settings.subreddits:
            for post in poller.poll_posts(subreddit_settings):
                for chat_id in subreddit_settings.telegram_chat_ids:
                    telegram_bot.post_reddit_post(chat_id, post)

                    # FIXME: I am too lazy to implement a proper rate limiting
                    send_post_jitter = round(random.random(), 3)
                    time.sleep(send_post_jitter)

            time.sleep(settings.subreddit_poll_interval_in_seconds)

        execute_duration = time.time() - start_at
        backoff = max(30, settings.poll_interval_in_seconds - execute_duration)
        logger.info(f"polling finished, sleep {backoff}s")
        time.sleep(backoff)
