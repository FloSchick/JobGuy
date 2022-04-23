import time
import logging
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
import requests
import csv
from rich.table import Table

# get logger
logger = logging.getLogger("jobgy_logger")


@dataclass
class Job:
    title: str
    location: str
    company: str
    summary: str
    site_url: str
    description: str
    original_url: str

    def __str__(self) -> str:
        return f"Title={self.title} Location={self.location} Company={self.company}"

    def to_dict(self):
        return dict(
            title=self.title,
            location=self.location,
            company=self.company,
            site_url=self.site_url,
            description=self.description,
            original_url=self.original_url,
        )


class Jobsearch:
    def __init__(self, position, location, radius, console=None) -> None:
        self.pos = position
        self.loc = location
        self.rad = radius
        self.jobs = list()
        self.console = console
        self.session = requests.Session()
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "referer": "https://www.google.com/",
        }

    def __extract_meta(self, url) -> str:
        response = self.session.get(url, headers=self.header)
        soup = BeautifulSoup(response.content, "html.parser")
        description = soup.find("div", {"id": "jobDescriptionText"}).getText()
        try:
            original_link = soup.find("div", {"id": "originalJobLinkContainer"}).a.get(
                "href"
            )
        except AttributeError:
            original_link = ""
        return description, original_link

    def get_jobs(self) -> list:
        pos = self.pos.replace(" ", "%20")
        url = f"https://de.indeed.com/Jobs?q={pos}&l={self.loc}&radius={self.rad}"

        while True:
            time.sleep(1)
            response = self.session.get(url, headers=self.header)
            time.sleep(1)
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.title.text == "hCaptcha solve page":
                self.console.log(
                    "Server responded with Captcha retry later.", style="red"
                )
            cards = soup.find_all("a", "tapItem")

            for card in cards:
                try:
                    title = card.find("h2", "jobTitle").getText()
                except AttributeError:
                    continue
                try:
                    company = card.find("span", "companyName").getText()
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

                # extract job description from url
                if job_url:
                    description, original_url = self.extract_meta(job_url)
                else:
                    description = ""
                    original_url = ""

                self.jobs.append(
                    Job(
                        title=title,
                        location=self.location,
                        company=company,
                        summary=summary,
                        site_url=job_url,
                        description=description,
                        original_url=original_url,
                    )
                )

            try:
                url = "https://de.indeed.com" + soup.find(
                    "a", {"aria-label": "Weiter"}
                ).get("href")
            except AttributeError:
                break

        self.session.close()

    def to_csv(self, filename):
        with open(filename, "w", newline="") as csvfile:
            fieldnames = [
                "jobtitle",
                "location",
                "company",
                "summary",
                "site_url",
                "original_url",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in self.jobs:
                writer.writerow(item.to_dict())

    def to_console(self, console):
        table = Table()
        for fieldname in ["Title", "Location", "Company", "URL"]:
            table.add_column(fieldname)
        for item in self.jobs:
            table.add_row(item.title, item.location, item.company, item.original_url)
        console.print(table)


if __name__ == "__main__":
    search = Jobsearch("Junior Python Developer", "München", "25")
    search.get_jobs()
    search.to_csv("jobsearch.csv")
