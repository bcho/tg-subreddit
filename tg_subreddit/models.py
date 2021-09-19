import dataclasses as dc
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import List


@dataclass_json
@dc.dataclass
class RedditPost:
    """Model for reddit post"""

    id: str
    title: str
    url: str
    subreddit: str
    author_id: str
    score_at_save: int
    upvote_ratio_at_save: float
    saved_at: datetime


@dataclass_json
@dc.dataclass
class RedditPostPollSettings:
    """Model for subreddit posts polling settings"""

    subreddit: str
    limit: int
    threshold_score: int
    telegram_chat_ids: List[str]


@dataclass_json
@dc.dataclass
class RedditPostPollSettingsGroup:
    """Model for reddit posts polling settings"""

    poll_interval_in_seconds: float
    subreddit_poll_interval_in_seconds: float
    subreddits: List[RedditPostPollSettings]
