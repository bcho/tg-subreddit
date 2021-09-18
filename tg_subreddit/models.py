import dataclasses as dc
from datetime import datetime


@dc.dataclass
class RedditPost:
    """Model for reddit post"""

    id: str
    title: str
    url: str
    author_id: str
    score_at_save: int
    upvote_ratio_at_save: float
    saved_at: datetime


@dc.dataclass
class RedditPostPollSettings:
    """Model for post poll settings"""

    subreddit: str
    limit: int
    threshold_score: int