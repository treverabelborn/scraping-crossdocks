import requests
from parsel import Selector
from .models import CrossDockListing
from .strings import clean_str


BASE_URL = 'https://www.crossdockbuddy.com'
SEARCH_URI = '/search_results?page=1'


def get_email_end(js):
    email_locator_end_1 = '.com`'
    if email_locator_end_1 in js:
        return js.index(email_locator_end_1) + len(email_locator_end_1)
    
    email_locator_end_2 = '.net`'
    if email_locator_end_2 in js:
        return js.index(email_locator_end_2) + len(email_locator_end_2)
    
    email_locator_end_3 = '.COM`'
    if email_locator_end_3 in js:
        return js.index(email_locator_end_3) + len(email_locator_end_3)
    
    email_locator_end_4 = '.us`'
    if email_locator_end_4 in js:
        return js.index(email_locator_end_4) + len(email_locator_end_4)
    
    email_locator_end_5 = '.site`'
    # TODO refactor this
    
    print(js)
    raise Exception('Failed to get email')

def extract_email(js):
    email_locator_start = 'Email Has Been Sent to '
    email_start = js.index(email_locator_start) + len(email_locator_start)
    email_end = get_email_end(js)
    return js[email_start:email_end]

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

    for l in listings:
        name = l.xpath('div[contains(@class, "mid_section")]/a/@title').get()
        desc = l.xpath('div[contains(@class, "mid_section")]/p[contains(@class, "member-search-description")]//text()').get()
        address = l.xpath('div[contains(@class, "mid_section")]/span[contains(@class, "member-search-location")]/small//text()').get()
        phone = l.xpath('div[contains(@class, "info_section")]/div/span[contains(@class, "member-search-phone")]/i/following-sibling::text()').get()
        href = l.xpath('div[contains(@class, "mid_section")]/a/@href').get()
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
        print(result)