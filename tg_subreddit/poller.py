from tg_subreddit.models import RedditPostPollSettings
import praw
import time

from . import config
from .reddit import RedditPostPoller
from .reddit import RedditPostStorageSqlite


def main(poll_interval_seconds: float):
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

    poll_settings = RedditPostPollSettings(
        subreddit='investing',
        limit=20,
        threshold_score=10,
    )

    while True:
        for post in poller.poll_posts(poll_settings):
            print(post)

        time.sleep(poll_interval_seconds)