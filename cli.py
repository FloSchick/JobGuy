from pydoc import cli
import click
from scraper.scraper import Jobsearch


@click.command()
@click.option("-r", "--radius", default=25, help="radius of jobsearch in km")
@click.option("-o", "--output", default="", help="output filename .csv|")
@click.argument("description")
@click.argument("location")
def cli(radius, description, location, output):
    click.echo(
        f"Initilized scraping with -> desc: {description}, location: {location} radius: {radius}km"
    )
    search = Jobsearch(description, location, radius)
    search.get_jobs()
    if output:
        search.to_csv(output)


if __name__ == "__main__":
    cli()
