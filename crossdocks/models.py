from typing import TypedDict


class CrossdockListing(TypedDict):
    name: str
    description: str
    location: str
    phone: str
    info_page_url: str
    email: str


class CrossdockSearchData(TypedDict):
    name: str
    description: str
    location: str
    phone: str
    info_page_url: str
