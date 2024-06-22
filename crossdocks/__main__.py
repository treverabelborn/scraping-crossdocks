import requests
from parsel import Selector
from .models import CrossDockListing
from .strings import clean_str, extract_email


BASE_URL = 'https://www.crossdockbuddy.com'
SEARCH_URI = '/search_results?page=1'


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
    html = session.get('{}{}'.format(BASE_URL, SEARCH_URI), cookies=cookies).text
    selector = Selector(text=html)
    listings = selector.xpath('//div[@class="grid_element"]')

    for i in range(0, len(listings)):
        listing = listings[i]
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
        connect_html = session \
            .get('{}{}/connect'.format(BASE_URL, href), cookies=cookies) \
            .text
        connect_selector = Selector(connect_html)
        js = connect_selector.xpath('//script[contains(text(),"resend_verification_email")]//text()').get()
        email = extract_email(js)
        
        result = CrossDockListing(
            name=name,
            description=clean_str(desc),
            address=clean_str(address),
            phone=clean_str(phone),
            email=email
        )
        print('index: ' + str(i))
        print(result)