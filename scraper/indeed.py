import time
import logging
from bs4 import BeautifulSoup
from base_class import Scraper, Job

# get logger
logger = logging.getLogger("jobguy_logger")


class IndeedScraper(Scraper):
    def __init__(self, title, location, radius, nums, console=None) -> None:
        Scraper.__init__(self, title, location, radius, console)

    def scrape_indeed(self) -> list:
        pos = self.pos.replace(" ", "%20")
        url = f"https://de.indeed.com/Jobs?q={pos}&l={self.loc}&radius={self.rad}"
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

                

                self.add_result(title, self.loc, company,summary, job_url, date))
                # exit if job number is reached
                if len(self.jobs) >= self.nums:
                    return self.close_connection()
            #  if "Weiter" button is missing last page is reached
            try:
                url = "https://de.indeed.com" + soup.find(
                    "a", {"aria-label": "Weiter"}
                ).get("href")
            except AttributeError:
                return self.close_connection()


if __name__ == "__main__":
    search = Jobsearch("Python", "München", "25", 2, None)
    search.scrape_indeed()
    search.to_csv("jobsearch.csv")
