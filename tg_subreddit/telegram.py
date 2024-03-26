from loguru import logger
import telegram

from .models import RedditPost


def format_reddit_post(post: RedditPost) -> str:
    return f'<b>/r/{post.subreddit}</b> <a href="{post.url}">{post.title}</a> ({post.score_at_save})'


class TelegramBot:
    def __init__(self, bot_token: str):
        self.bot = telegram.Bot(token=bot_token)
        self.logger = logger.bind(service="telegram-bot")

    def post_reddit_post(self, chat_id: str, post: RedditPost):
        self.logger.info(f"posting post {post.id} to {chat_id}")

        post_text = format_reddit_post(post)
        self.bot.send_message(
            chat_id=chat_id,
            text=post_text,
            parse_mode="HTML",
        )
