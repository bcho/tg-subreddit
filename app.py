import click

from tg_subreddit import config
from tg_subreddit import db
from tg_subreddit import poller


@click.group()
def main():
    pass


@main.command()
def prepare_db():
    """Prepare database."""
    database_path = config.database_path()
    db.prepare_db(database_path)


@main.command()
@click.option('--poll-interval-seconds', default=180, help='Poll interval in seconds')
def poll(poll_interval_seconds):
    """Start reddit post poller."""
    poller.main(poll_interval_seconds=poll_interval_seconds)


if __name__ == '__main__':
    main()