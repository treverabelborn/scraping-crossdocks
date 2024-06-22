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
        location_selector = mid_section.xpath('span[contains(@class, "member-search-location")]')
        location_city = location_selector.xpath('small//text()').get()
        location_zip = location_selector.xpath('small/span[1]//text()').get()
        location_country = location_selector.xpath('small/span[2]//text()').get()
        location = ''

        if (location_city or location_zip or location_country):
            location = '{}{}, {}'.format(location_city, location_zip, location_country)
        href = mid_section.xpath('a/@href').get()
        phone = listing.xpath('div[contains(@class, "info_section")]/div/span[contains(@class, "member-search-phone")]/i/following-sibling::text()').get()

        results.append(CrossdockSearchData(
            name=name,
            description=clean_str(desc),
            location=clean_str(location),
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