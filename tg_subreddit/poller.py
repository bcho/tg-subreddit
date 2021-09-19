from loguru import logger
import praw
import time
from typing import Callable

from . import config
from .models import RedditPostPollSettingsGroup
from .reddit import RedditPostPoller
from .reddit import RedditPostStorageSqlite


logger = logger.bind(service='poller')


def main(get_settings: Callable[[], RedditPostPollSettingsGroup]):
    reddit_client = praw.Reddit(
        client_id=config.reddit_client_id(),
        client_secret=config.reddit_client_secret(),
        user_agent=config.reddit_client_user_agent(),
    )

    storage = RedditPostStorageSqlite(db_path=config.database_path())

    poller = RedditPostPoller(
        reddit_client=reddit_client,
        storage=storage,
    )

    while True:
        logger.debug('start polling')
        start_at = time.time()

        settings = get_settings()

        for subreddit_settings in settings.subreddits:
            for post in poller.poll_posts(subreddit_settings):
                print(post)
            time.sleep(settings.subreddit_poll_interval_in_seconds)

        execute_duration = time.time() - start_at
        backoff = max(30, settings.poll_interval_in_seconds - execute_duration)
        logger.info(f'polling finished, sleep {backoff}s')
        time.sleep(backoff)