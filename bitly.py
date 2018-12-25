import requests
import os
import dotenv
from argparse import ArgumentParser


def get_short_link(long_link, api_token):
    json_dict = {'long_url': long_link}
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks',
                             json=json_dict,
                             headers={'Authorization': 'Bearer {}'.format(api_token)})
    if not response.ok:
        return None
    return response.json()['link']


def get_clicks(bitlink, api_token):
    response = \
        requests.get('https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(bitlink),
                     headers={'Authorization': 'Bearer {}'.format(api_token)})
    if not response.ok:
        return None
    return response.json()['total_clicks']


def get_and_check_link(link, api_token):
    clicks = get_clicks(link, api_token)
    if clicks:
        return clicks
    bitlink = get_short_link(link, api_token)
    if bitlink:
        return bitlink
    return None


if __name__ == '__main__':
    dotenv.load_dotenv()
    API_TOKEN = os.getenv('API_TOKEN')
    parser = ArgumentParser()
    parser.add_argument('site', help='name of site', type=str)
    args = parser.parse_args()
    result = get_and_check_link(args.site, API_TOKEN)
    if result:
        print(result)
    else:
        print('Mistake, try again')
