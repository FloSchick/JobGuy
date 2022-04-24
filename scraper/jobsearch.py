import time
import logging
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
import csv
from rich.table import Table

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

# get logger
logger = logging.getLogger("jobguy_logger")


@dataclass
class Job:
    title: str
    location: str
    company: str
    summary: str
    url: str

    def set_description(self, text) -> None:
        self.description = text

    def __str__(self) -> str:
        return f"Title={self.title} Location={self.location} Company={self.company}"

    def __eq__(self, other: object) -> bool:
        return self.title == other.title and self.company == other.company

    def to_dict(self):
        return dict(
            title=self.title,
            location=self.location,
            company=self.company,
            summary=self.summary,
            url=self.url,
        )


class Jobsearch:
    def __init__(self, position, location, radius, nums, console=None) -> None:
        self.pos = position
        self.loc = location
        self.rad = radius
        self.jobs = list()
        self.console = console
        self.nums = nums
        self.driver = self.establish_connection()

    def establish_connection(self) -> webdriver:
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")
        options.add_argument("--headless")
        driver = webdriver.Chrome(
            ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
            chrome_options=options,
        )
        return driver

    def scrape_indeed(self) -> list:
        pos = self.pos.replace(" ", "%20")
        url = f"https://de.indeed.com/Jobs?q={pos}&l={self.loc}&radius={self.rad}"
        # iterate over all pages
        while True:
            # wait delay to pervent blacklisting
            time.sleep(2)
            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            # check if response was Captcha
            if soup.title.text == "hCaptcha solve page":
                logger.error("Server responded with Captcha retry later")
            # extract all joblistings
            cards = soup.find_all("a", "tapItem")
            for card in cards:
                try:
                    title = card.find("h2", "jobTitle").getText().strip()
                except AttributeError:
                    continue
                try:
                    company = card.find("span", "companyName").getText().strip()
                except AttributeError:
                    company = ""
                try:
                    summary = card.find("div", "job-snippet").getText().strip()
                except AttributeError:
                    summary = ""
                try:
                    job_url = "https://de.indeed.com" + card["href"]
                except AttributeError:
                    job_url = ""

                job = Job(
                    title=title,
                    location=self.loc,
                    company=company,
                    summary=summary,
                    url=job_url,
                )

                self.jobs.append(job)
                # exit if job number is reached
                if len(self.jobs) >= self.nums:
                    return
            #  if "Weiter" button is missing last page is reached
            try:
                url = "https://de.indeed.com" + soup.find(
                    "a", {"aria-label": "Weiter"}
                ).get("href")
            except AttributeError:
                return

    def to_csv(self, filename):
        """Prints detected jobs to filepath csv"""
        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "title",
                "location",
                "company",
                "summary",
                "url",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.jobs:
                writer.writerow(item.to_dict())

    def to_console(self, console):
        """Prints detected jobs as table to console"""
        table = Table()
        for fieldname in ["Title", "Location", "Company", "Summary", "URL"]:
            table.add_column(fieldname)
        for item in self.jobs:
            table.add_row(
                item.title, item.location, item.company, item.summary, item.url
            )
        console.print(table)


if __name__ == "__main__":
    search = Jobsearch("Python", "München", "25")
    search.get_jobs()
    search.to_csv("jobsearch.csv")
