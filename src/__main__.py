import requests
from parsel import Selector
from .models import CrossDockListing


URL = 'https://www.crossdockbuddy.com/search_results?page=1'


def clean_str(str):
    if str is None:
        return str
    return str.replace('\r', '') \
        .replace('\n', '') \
        .replace('\t', '') \
        .trim()


if __name__ == '__main__':
    session = requests.Session()
    cookies = {
        'token': '588f83e6d914be13e05b4c4e0841aa10',
        'loggedin': '6dcc664f0b4e00d3b7a01ca2944a0a27',
        'userid': 'SFdmV1RaMktiUHVLaHhpbnNvUk5LdmRCTmxaL0dpd2oyTGtKY1JHU1M2RT0%3D%7C%7C832095414609cec90efaadd7d3e991a019aa4b5d64b50a96cbcf8846954cbb86',
        'useractive': '2',
        'subscription_id': '2',
        'profession_id': '0'
    }
    html = session.get(URL, cookies=cookies).text
    selector = Selector(text=html)
    listings = selector.xpath('//div[@class="grid_element"]')
    listings_hrefs = []

    for l in listings:
        name = l.xpath('div[contains(@class, "mid_section")]/a/@title').get()
        desc = l.xpath('div[contains(@class, "mid_section")]/p[contains(@class, "member-search-description")]//text()').get()
        address = l.xpath('div[contains(@class, "mid_section")]/span[contains(@class, "member-search-location")]/small//text()').get()
        phone = l.xpath('div[contains(@class, "info_section")]/div/span[contains(@class, "member-search-phone")]/i/following-sibling::text()').get()

        result = CrossDockListing(
            name=name,
            description=clean_str(desc),
            address=clean_str(address),
            phone=clean_str(phone)
        )
        print(result)

        l_page = l.xpath('div[contains(@class, "mid_section")]/a/@href').get()
        # print(l_page)
        listings_hrefs.append(l_page)