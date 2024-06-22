from dataclasses import dataclass


@dataclass
class CrossdockListing:
    name: str
    description: str
    address: str
    phone: str
    email: str


@dataclass
class CrossdockSearchData:
    name: str
    description: str
    address: str
    phone: str
    href: str


@dataclass
class CrossdockInfoPageData:
    email: str