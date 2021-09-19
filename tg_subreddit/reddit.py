from contextlib import contextmanager
from datetime import datetime
from loguru import logger
import sqlite3
import praw

from .config import database_table_name_reddit_post
from .models import RedditPost
from .models import RedditPostPollSettings


class RedditPostStorageBase:

    def save_post(self, post: RedditPost):
        raise NotImplementedError

    def has_post(self, post: RedditPost) -> bool:
        raise NotImplementedError


class RedditPostStorageSqlite(RedditPostStorageBase):

    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def open_cursor(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        yield cur
        conn.commit()
        conn.close()

    def save_post(self, post: RedditPost):
        post_content = post.to_json()
        with self.open_cursor() as cur:
            cur.execute(f'''
            INSERT INTO {database_table_name_reddit_post}
            VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET content = ?
            ''',
            (post.id, post_content, post_content),
            )

    def has_post(self, post: RedditPost) -> bool:
        with self.open_cursor() as cur:
            cur.execute(f'''
            SELECT count(1) FROM {database_table_name_reddit_post} WHERE id = ?
            ''',
            (post.id,),
            )
            return cur.fetchone()[0] > 0


def submission_as_reddit_post(p) -> RedditPost: 
    return RedditPost(
        id=p.id,
        title=p.title,
        url=p.url,
        author_id=p.author_fullname,
        score_at_save=p.score,
        upvote_ratio_at_save=p.upvote_ratio,
        saved_at=datetime.utcnow(),
    )


class RedditPostPoller:

    def __init__(self, reddit_client: praw.Reddit, storage: RedditPostStorageBase):
        self.reddit_client = reddit_client
        self.storage = storage
        self.logger = logger.bind(service='RedditPostPoller')

    def poll_posts(self, settings: RedditPostPollSettings):
        logger = self.logger.bind(subreddit=settings.subreddit)

        subreddit = self.reddit_client.subreddit(settings.subreddit)
        for submission in subreddit.hot(limit=settings.limit):
            post = submission_as_reddit_post(submission)

            if post.score_at_save < settings.threshold_score:
                logger.debug(f'Post {post.id} score does not match requirements')
                continue

            if self.storage.has_post(post):
                logger.debug(f'Post {post.id} already saved before')
                continue

            logger.info(f'Found new post [{post.id}] [{post.title}, {post.url}] [{post.score_at_save}]')
            yield post

            self.storage.save_post(post)