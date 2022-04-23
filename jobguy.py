from pydoc import cli
import logging
import time
import csv
from rich.table import Table

from rich.console import Console
from rich.logging import RichHandler

import click
from scraper.scraper import Jobsearch

# configure logger
logger = logging.getLogger("jobgy_logger")
logger.addHandler(RichHandler())
logger.setLevel(logging.INFO)


@click.command()
@click.option("-l", "--location", default="Deutschland", help="job location")
@click.option("-r", "--radius", default=25, help="radius of jobsearch in km")
@click.option("-o", "--output", default="", help="output filename.csv")
@click.argument("title")
def cli(radius, title, location, output):
    console = Console()
    with console.status(
        "[bold green]Doing internet magic...", spinner="earth"
    ) as status:
        console.log(
            f"Searching Jobs with -> Title: {title}, Location: {location} Radius: {radius}km",
            style="cyan",
        )

        search = Jobsearch(title, location, radius, console)
        search.get_jobs()
        search.to_console(console)
        if output:
            search.to_csv(output)


if __name__ == "__main__":
    cli()
