from resources.defaults import (
    DEFAULT_SEARCH_TITLE,
    DEFAULT_PROVIDERS,
)
from scraper.config import ScraperConfig
from scraper.indeed import IndeedScraper

if __name__ == "__main__":
    cfg = ScraperConfig(
        "Junior Python Developer", DEFAULT_PROVIDERS, "München", max_listing_count=200
    )
    s = IndeedScraper(cfg)
    s.scrape()
    print(s)
