import time
import logging
from bs4 import BeautifulSoup
from rich.console import Console
from typing import Optional
from scraper.base_class import Scraper

# custom imports
from scraper.config import ScraperConfig

# get logger
logger = logging.getLogger("jobguy_logger")


class IndeedScraper(Scraper):
    def __init__(
        self, config: ScraperConfig, console: Optional[Console] = None
    ) -> None:
        Scraper.__init__(self, config)

        # self.mapping = {
        #     "title": f"q={title}",
        #     "location": f"l={self.loc}",
        #     "radius": f"radius={self.rad}",
        #     "cpp": "sc=0kf%3Aattr(GJUK3)%3B",
        #     "python": "sc=0kf%3Aattr(X62BT)%3B",
        # }
        # self.tags = [self.tag_mapping[t] for t in tags]

    def __build_url(self) -> str:
        """Get the indeed search url
        TODO: Add other countries setting to config (.com/.uk/...)
        """
        return "https://www.indeed.de/jobs?q={}&l={}&radius={}&limit={}".format(
            self.config.title.replace(" ", "%20"),
            self.config.location,
            self.config.radius,
            self.config.max_listing_count,
        )

    def scrape(self) -> list:
        url = self.__build_url()

        # iterate over all pages
        while True:
            # wait delay to pervent blacklisting
            time.sleep(2)
            self.driver.get(url)
            self.driver.find_elements_by_class_name("tapItem")
            html = self.driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            # check if response was Captcha
            if soup.title.text == "hCaptcha solve page":
                logger.error("Server responded with Captcha retry later")
            # extract all joblistings
            cards = soup.find_all("div", {"class": "tapItem"})
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
                    job_url = "https://de.indeed.com" + card.find("a")["href"]
                except AttributeError:
                    job_url = ""

                self.add_result(title, self.loc, company, summary, job_url)
                # exit if job number is reached
                if len(self.jobs) >= self.max_count:
                    return self.close_connection()
            #  if "Weiter" button is missing last page is reached
            try:
                url = "https://de.indeed.com" + soup.find(
                    "a", {"aria-label": "Weiter"}
                ).get("href")
            except AttributeError:
                return self.close_connection()


if __name__ == "__main__":
    conf = ScraperConfig()
    search = IndeedScraper("Python", "München", "25", 2, ["python", "cpp"], None)
    search.scrape_indeed()
    search.to_csv("jobsearch.csv")
