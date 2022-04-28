"""This module implements default scraper class"""
import csv
from dataclasses import dataclass, fields
from rich.console import Console
from rich.table import Table
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# custom imports
from jobguy.scraper.config import ScraperConfig


@dataclass(eq=True, order=True, frozen=True)
class Job:
    title: str
    location: str
    company: str
    summary: str
    url: str

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

    @staticmethod
    def get_fields():
        return [field.name for field in fields(Job)]


class Scraper:
    def __init__(self, config: ScraperConfig) -> None:
        # super().__init__(level=config.log_level, file_path=config.log_file)
        self.driver = self.__establish_connection()
        self.config = config
        self.jobs = set()

    def __establish_connection(self) -> webdriver:
        """connect to chrome session for scraping"""
        options = webdriver.ChromeOptions()
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--incognito")
        # options.add_argument("--headless")
        driver = driver = webdriver.Chrome(
            service=Service(ChromeDriverManager(log_level=0).install()), options=options
        )
        driver.implicitly_wait(10)
        return driver

    def close_connection(self) -> None:
        """close chrome session"""
        self.driver.quit()

    def add_result(self, title, location, company, summary, url) -> None:
        "adds result to scraper"
        job = Job(
            title=title,
            location=location,
            company=company,
            summary=summary,
            url=url,
        )
        self.jobs.add(job)

    def to_csv(self, filename: str) -> None:
        """prints detected jobs to csv"""
        with open(
            filename,
            "w",
        ) as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=Job.get_fields(), dialect="excel"
            )
            writer.writeheader()
            for item in self.jobs:
                writer.writerow(item.to_dict())

    def to_console(self, console: Console) -> None:
        """prints detected jobs as table to console"""
        table = Table()
        for fieldname in Job.get_fields():
            table.add_column(fieldname)
        for item in self.jobs:
            table.add_row(
                item.title, item.location, item.company, item.summary, item.url
            )
        console.print(table)
