import requests
import urllib.parse
import csv
from .models import CrossdockListing, CrossdockSearchData
from .scrapers import scrape_crossdocks, scrape_email_cb, scrape_email_google


BASE_URL = 'https://www.crossdockbuddy.com'
SEARCH_URIS = ['/search_results?page=1', '/search_results?page=2']


if __name__ == '__main__':
    session = requests.Session()
    cookies: dict = {
        'token': '588f83e6d914be13e05b4c4e0841aa10',
        'loggedin': '6dcc664f0b4e00d3b7a01ca2944a0a27',
        'userid': 'SFdmV1RaMktiUHVLaHhpbnNvUk5LdmRCTmxaL0dpd2oyTGtKY1JHU1M2RT0%3D%7C%7C832095414609cec90efaadd7d3e991a019aa4b5d64b50a96cbcf8846954cbb86',
        'useractive': '2',
        'subscription_id': '2',
        'profession_id': '0'
    }

    results_search: list[CrossdockSearchData] = []
    try:
        for search_page in SEARCH_URIS:
            search_page_html: str = session.get('{}{}'.format(BASE_URL, search_page), cookies=cookies).text
            search_page_data: list[CrossdockSearchData] = scrape_crossdocks(search_page_html)
            results_search = results_search + search_page_data

        results_full: list[CrossdockListing] = []
        for result in results_search:
            info_page_url = '{}{}'.format(BASE_URL, result['href'])
            connect_page_html: str = session.get('{}/connect'.format(info_page_url), cookies=cookies).text

            email = scrape_email_cb(connect_page_html)
            if ('@crossdockbuddy.com' in email):
                google_search_url = 'https://www.google.com/search?{}'.format(urllib.parse.urlencode({ 'q': result['name'] + ' contact email'}))
                google_search_html = session.get(google_search_url).text
                email = scrape_email_google(google_search_html)


            results_full.append(CrossdockListing(
                name=result['name'],
                description=result['description'],
                location=result['location'],
                phone=result['phone'],
                info_page_url=info_page_url,
                email=email
            ))
    finally:
        with open('output.csv', 'w', newline='') as out_file:
            writer = csv.DictWriter(out_file, results_full[0].keys())
            writer.writeheader()
            writer.writerows(results_full)