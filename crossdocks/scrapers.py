from parsel import Selector
from .models import CrossdockSearchData, CrossdockInfoPageData
from .strings import clean_str, extract_email


def scrape_crossdocks(search_page_html) -> list[CrossdockSearchData]:
    selector = Selector(text=search_page_html)
    listings = selector.xpath('//div[@class="grid_element"]')
    results = []

    for listing in listings:
        mid_section = listing.xpath('div[contains(@class, "mid_section")]')
        name = mid_section.xpath('a/@title').get()
        desc = mid_section.xpath('p[contains(@class, "member-search-description")]//text()').get()
        location = mid_section.xpath('span[contains(@class, "member-search-location")]')
        address_city = location.xpath('small//text()').get()
        address_zip = location.xpath('small/span[1]//text()').get()
        address_country = location.xpath('small/span[2]//text()').get()
        address = '{}{}, {}'.format(address_city, address_zip, address_country)
        href = mid_section.xpath('a/@href').get()
        phone = listing.xpath('div[contains(@class, "info_section")]/div/span[contains(@class, "member-search-phone")]/i/following-sibling::text()').get()

        results.append(CrossdockSearchData(
            name=name,
            description=clean_str(desc),
            address=clean_str(address),
            phone=clean_str(phone),
            href=href
        ))
    return results


def scrape_emails(connect_page_html):
    connect_selector = Selector(connect_page_html)
    js = connect_selector.xpath('//script[contains(text(),"resend_verification_email")]//text()').get()

    return CrossdockInfoPageData(
        email=extract_email(js)
    )