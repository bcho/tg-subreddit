import click

from tg_subreddit import config
from tg_subreddit import db
from tg_subreddit import poller
from tg_subreddit.models import RedditPostPollSettingsGroup


@click.group()
def main():
    pass


@main.command()
def prepare_db():
    """Prepare database."""
    database_path = config.database_path()
    db.prepare_db(database_path)


@main.command()
@click.option('--poll-settings-json', type=click.Path(exists=True), help='poll settings JSON', required=True)
def poll(poll_settings_json):
    """Start reddit post poller."""

    def get_settings() -> RedditPostPollSettingsGroup:
        with open(poll_settings_json) as f:
            content = f.read()
            return RedditPostPollSettingsGroup.from_json(content)

    poller.main(get_settings=get_settings)


if __name__ == '__main__':
    main()