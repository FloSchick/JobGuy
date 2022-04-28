# standardt imports
from email.policy import default
import logging

# 3rd party imports
import click
from rich.console import Console
from rich.logging import RichHandler

# custom files
from jobguy.scraper.indeed import IndeedScraper
from jobguy.scraper.config import ScraperConfig
from jobguy.resources.defaults import (
    DEFAULT_SEARCH_TITLE,
    DEFAULT_PROVIDERS,
    DEFAULT_RADIUS,
    DEFAULT_LOCATION,
    DEFAULT_NUMS,
)

# configure logger
logger = logging.getLogger("jobguy_logger")
logger.setLevel(logging.INFO)


@click.command()
@click.option("-d", "--desc", default=DEFAULT_SEARCH_TITLE, help="job description")
@click.option("-l", "--loc", default=DEFAULT_LOCATION, help="job location")
@click.option("-r", "--rad", default=DEFAULT_RADIUS, help="radius in km")
@click.option("-n", "--max_nums", default=DEFAULT_NUMS, help="number of jobs to gather")
@click.option("-o", "--output", help="output filename (.csv|.xlsx)")
@click.option(
    "-t",
    "--tags",
    multiple=True,
    help="tags like cpp or python",
)
def cli(radius, desc, location, output, nums, tags):
    """Commandline tool to scrape jobs from different websites"""
    console = Console()
    # add console to logging handler
    logger.addHandler(RichHandler(console=console))
    with console.status("[bold cyan]Doing internet magic..."):
        tags_string = ", ".join(tags)
        console.log(
            f"[cyan]Searching Title: {desc}, Location: {location}, Radius: {radius}km, Tags: {tags_string}"
        )
        cfg = ScraperConfig(
            title=desc,
            providers=DEFAULT_PROVIDERS,
            location=location,
            max_listing_count=nums,
            tags=tags,
        )
        search = IndeedScraper(cfg, console)
        search.scrape()
        search.to_console(console)
        if output:
            search.to_csv(output)
        console.log("[bold cyan]DONE")


if __name__ == "__main__":
    cli()
