import time
import re
import logging
from bs4 import BeautifulSoup
from rich.console import Console
from typing import Optional
from jobguy.scraper.base_class import Scraper

# custom imports
from jobguy.scraper.config import ScraperConfig

# get logger
logger = logging.getLogger("jobguy_logger")


class IndeedScraper(Scraper):
    def __init__(
        self, config: ScraperConfig, console: Optional[Console] = None
    ) -> None:
        Scraper.__init__(self, config)

        self.supported_tags = {
            "cpp": "sc=0kf%3Aattr(GJUK3)%3B",
            "python": "sc=0kf%3Aattr(X62BT)%3B",
        }

    def __build_url(self) -> str:
        """Get the indeed search url
        TODO: Add other countries setting to config (.com/.uk/...)
        """
        valid_tags = []
        for t in self.config.tags:
            try:
                valid_tags.append(self.supported_tags[t])
            except KeyError:
                logger.warning(f"Tag not supported by indeed: {t}")
                continue
        if valid_tags:
            tag_string = "&".join(valid_tags)
        else:
            tag_string = None
        url = "https://www.indeed.de/jobs?q={}&l={}&radius={}&limit=1000&{}".format(
            self.config.title.replace(" ", "%20"),
            self.config.location,
            self.config.radius,
            tag_string,
        )
        logger.debug(f"generated search url: [link={url}]Link[/link]")
        return url

    def scrape(self) -> list:
        url = self.__build_url()

        # iterate over all pages
        while True:
            # wait delay to pervent blacklisting
            self.driver.get(url)
            time.sleep(3)
            self.driver.find_elements_by_class_name("tapItem")
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            # check if response was Captcha
            if soup.title.text == "hCaptcha solve page":
                logger.error("Server responded with Captcha retry later")
            # extract all joblistings
            # cards = soup.find_all("div", {"class": "tapItem"})
            # cards = soup.find_all("div", {"class": "job_seen_beacon"})
            cards = soup.find_all("div", {"class": "slider_container"})
            # cards = soup.findAll("a", {"data-jk": re.compile(".*")})
            ids = [
                id["data-jk"] for id in soup.findAll("a", {"data-jk": re.compile(".*")})
            ]

            for id_, card in zip(ids, cards):
                try:
                    title = card.find("h2", "jobTitle").getText().strip()
                    # title = card.find("span").getText()
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
                    # job_url = "https://de.indeed.com" + card.previous["href"]
                    job_url = "https://de.indeed.com/viewjob?jk=" + id_

                except TypeError:
                    job_url = ""

                self.add_result(title, self.config.location, company, summary, job_url)
                # exit if job number is reached
                if len(self.jobs) >= self.config.max_listing_count:
                    return self.close_connection()
            #  if "Weiter" button is missing last page is reached
            try:
                url = "https://de.indeed.com" + soup.find(
                    "a", {"aria-label": "Weiter"}
                ).get("href")
            except AttributeError:
                logger.debug(
                    "Early exit, because no further jobs where found to scrape"
                )
                return self.close_connection()
