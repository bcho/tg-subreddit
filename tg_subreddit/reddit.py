from contextlib import contextmanager
from datetime import datetime
from loguru import logger as loguru_logger
import sqlite3
import praw
import requests
from requests.adapters import HTTPAdapter, Retry

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

            
class RedditPostStorageSqliteRest(RedditPostStorageBase):
    
    def __init__(self, base: str, table_name: str, auth_token: str):
        self.base = base
        self.table_name = table_name
        self.auth_token = auth_token

    def _request_headers(self, headers=None, **kwargs) -> dict:
        headers = headers or {}

        return {
            **kwargs,
            **headers,
            'authorization': f'Bearer {self.auth_token}',
        }

    @contextmanager
    def retry_session(self):
        sess = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
        sess.mount('https://', HTTPAdapter(max_retries=retries))

        yield sess

    def save_post(self, post: RedditPost):
        with self.retry_session() as sess:
            resp = sess.post(
                f'{self.base}/{self.table_name}',
                headers=self._request_headers(
                    headers={'Content-Type': 'application/json'},
                    prefer='resolution=merge-duplicates',
                ),
                json=dict(id=post.id, content=post.to_json()),
            )
            resp.raise_for_status()

    def has_post(self, post: RedditPost) -> bool:
        with self.retry_session() as sess:
            resp = sess.get(
                f'{self.base}/{self.table_name}',
                headers=self._request_headers(
                    headers={'range-unit': 'items', 'range': '0-'},
                    prefer='count=exact',
                ),
                params=dict(id=f'eq.{post.id}'),
            )

        content_range = resp.headers.get('content-range')
        if content_range is None:
            return False
        ps = content_range.split('/')
        if len(ps) != 2:
            return False
        try:
            return int(ps[1]) > 0
        except ValueError:
            return False


def submission_as_reddit_post(p, subreddit: str) -> RedditPost:
    author_id = '__unknown__'
    try:
        author_id = p.author_fullname
    except Exception:
        pass

    return RedditPost(
        id=p.id,
        title=p.title,
        url=p.url,
        subreddit=subreddit,
        author_id=author_id,
        score_at_save=p.score,
        upvote_ratio_at_save=p.upvote_ratio,
        saved_at=datetime.utcnow(),
    )


class RedditPostPoller:

    def __init__(self, reddit_client: praw.Reddit, storage: RedditPostStorageBase):
        self.reddit_client = reddit_client
        self.storage = storage
        self.logger = loguru_logger.bind(service='RedditPostPoller')

    def poll_posts(self, settings: RedditPostPollSettings):
        logger = self.logger.bind(subreddit=settings.subreddit)

        subreddit = self.reddit_client.subreddit(settings.subreddit)
        for submission in subreddit.hot(limit=settings.limit):
            post = submission_as_reddit_post(submission, subreddit=settings.subreddit)

            if post.score_at_save < settings.threshold_score:
                logger.debug(f'Post {post.id} score does not match requirements')
                continue

            if self.storage.has_post(post):
                logger.debug(f'Post {post.id} already saved before')
                continue

            logger.info(f'Found new post [{post.id}] [{post.title}, {post.url}] [{post.score_at_save}]')
            yield post

            self.storage.save_post(post)