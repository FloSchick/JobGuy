# standardt imports
from email.policy import default
import logging

# 3rd party imports
import click
from rich.console import Console
from rich.logging import RichHandler

# custom files
from scraper.indeed import IndeedScraper

# configure logger
logger = logging.getLogger("jobguy_logger")
logger.setLevel(logging.INFO)


@click.command()
@click.option("-l", "--location", default="Deutschland", help="job location")
@click.option("-r", "--radius", default=25, help="radius of jobsearch in km")
@click.option(
    "-t", "--tags", multiple=True, help="search for specific tags like python or cpp"
)
@click.option("-n", "--nums", default=100, help="number of jobs to gather")
@click.option("-o", "--output", default="", help="output filename.csv")
@click.argument("title")
def cli(radius, title, location, output, nums, tags):
    """Commandline tool to scrape jobs from different websites"""
    console = Console()
    # add console to logging handler
    logger.addHandler(RichHandler(console=console))
    with console.status("[bold cyan]Doing internet magic..."):
        tags_string = ", ".join(tags)
        console.log(
            f"[cyan]Searching Title: {title}, Location: {location}, Radius: {radius}km, Tags: {tags_string}"
        )
        search = IndeedScraper(title, location, radius, nums, tags, console)
        # search.scrape_indeed()
        search.to_console(console)
        if output:
            search.to_csv(output)
        console.log("[bold cyan]DONE")


if __name__ == "__main__":
    cli()
