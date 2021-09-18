from datetime import datetime
import praw

from .models import RedditPost
from .models import RedditPostPollSettings


class RedditPostStorageBase:

    def save_post(self, post: RedditPost):
        raise NotImplementedError

    def has_post(self, post: RedditPost) -> bool:
        raise NotImplementedError


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

    def poll_post(self, settings: RedditPostPollSettings):
        subreddit = self.reddit_client.subreddit(settings.subreddit)
        for submission in subreddit.hot(limit=settings.limit):
            post = submission_as_reddit_post(submission)
            print(post)