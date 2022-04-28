"""Object to abstract serach query settings"""
from typing import List, Optional
from enum import Enum


class Provider(Enum):
    """Job source providers"""

    INDEED = 1


class ScraperConfig:
    def __init__(
        self,
        title: str,
        providers: List[Provider],
        location: Optional[str] = None,
        radius: Optional[int] = None,
        tags: List[str] = [],
        max_listing_count: Optional[int] = None,
    ) -> None:
        """This object stores all search configurations

        Args:
            title (str): jobtitle to search
            providers (List[Provider]): selected provider sites to search
            location (Optional[str], optional): location fpr search. Defaults to None.
            radius (Optional[int], optional): radius to search in km. Defaults to None.
            tags (List[str], optional): tags to search for like programming languages and other skills. Defaults to None.
            max_listing_count (Optional[int], optional): max number of jobs to scrape. Defaults to None.
        """
        self.title = title
        self.providers = providers
        self.location = location
        self.radius = radius
        self.tags = tags
        self.max_listing_count = max_listing_count

    def __str__(self) -> str:

        return f"Title: {self.title}, Location: {self.location}, Radius: {self.radius}km, Tags: {self.tags}"
