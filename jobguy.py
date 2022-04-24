# standardt imports
import logging

# 3rd party imports
import click
from rich.console import Console
from rich.logging import RichHandler

# custom files
from scraper.jobsearch import Jobsearch

# configure logger
logger = logging.getLogger("jobguy_logger")
logger.setLevel(logging.INFO)


@click.command()
@click.option("-l", "--location", default="Deutschland", help="job location")
@click.option("-r", "--radius", default=25, help="radius of jobsearch in km")
@click.option("-n", "--nums", default=100, help="number of jobs to gather")
@click.option("-o", "--output", default="", help="output filename.csv")
@click.option("-pl", "--p_language", default="", help="filter by programming language")
@click.argument("title")
def cli(radius, title, location, output, nums, p_language):
    console = Console()
    # add console to logging handler
    logger.addHandler(RichHandler(console=console))
    with console.status("[bold cyan]Doing internet magic..."):
        console.log(
            f"[cyan]Searching Title: {title}, Location: {location}, Radius: {radius}km"
        )
        search = Jobsearch(title, location, radius, nums, p_language, console)
        search.scrape_indeed()
        search.to_console(console)
        if output:
            search.to_csv(output)
        console.log("[bold cyan]DONE")


if __name__ == "__main__":
    cli()
