import requests
import csv
from .models import CrossdockListing, CrossdockSearchData, CrossdockInfoPageData
from .scrapers import scrape_crossdocks, scrape_emails


BASE_URL = 'https://www.crossdockbuddy.com'
SEARCH_URIS = ['/search_results?page=1', '/search_results?page=2']


if __name__ == '__main__':
    session: requests.Session = requests.Session()
    cookies: dict = {
        'token': '588f83e6d914be13e05b4c4e0841aa10',
        'loggedin': '6dcc664f0b4e00d3b7a01ca2944a0a27',
        'userid': 'SFdmV1RaMktiUHVLaHhpbnNvUk5LdmRCTmxaL0dpd2oyTGtKY1JHU1M2RT0%3D%7C%7C832095414609cec90efaadd7d3e991a019aa4b5d64b50a96cbcf8846954cbb86',
        'useractive': '2',
        'subscription_id': '2',
        'profession_id': '0'
    }

    results_search: list[CrossdockSearchData] = []
    for search_page in SEARCH_URIS:
        search_page_html: str = session.get('{}{}'.format(BASE_URL, search_page), cookies=cookies).text
        search_page_data: list[CrossdockSearchData] = scrape_crossdocks(search_page_html)
        results_search = results_search + search_page_data

    results_full: list[CrossdockListing] = []
    for s in results_search:
        connect_page_html: str = session.get('{}{}/connect'.format(BASE_URL, s['href']), cookies=cookies).text
        connect_page_data: CrossdockInfoPageData = scrape_emails(connect_page_html)
        results_full.append(CrossdockListing(
            name=s['name'],
            description=s['description'],
            location=s['location'],
            phone=s['phone'],
            email=connect_page_data['email']
        ))

    with open('output.csv', 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, results_full[0].keys())
        writer.writeheader()
        writer.writerows(results_full)