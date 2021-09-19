import dataclasses as dc
from datetime import datetime
import json


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

    def searlize_to_json(self) -> str:
        d = dc.asdict(self)
        d['saved_at'] = d['saved_at'].isoformat()
        return json.dumps(d)


@dc.dataclass
class RedditPostPollSettings:
    """Model for post poll settings"""

    subreddit: str
    limit: int
    threshold_score: int