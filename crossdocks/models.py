from typing import TypedDict


class CrossdockListing(TypedDict):
    name: str
    description: str
    address: str
    phone: str
    email: str


class CrossdockSearchData(TypedDict):
    name: str
    description: str
    location: str
    phone: str
    href: str


class CrossdockInfoPageData(TypedDict):
    email: str