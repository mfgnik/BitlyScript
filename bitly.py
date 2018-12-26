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


def main():
    dotenv.load_dotenv()
    api_token = os.getenv('API_TOKEN')
    parser = ArgumentParser()
    parser.add_argument('link', help='name of site', type=str)
    args = parser.parse_args()
    clicks = get_clicks(args.link, api_token)
    if clicks:
        print(clicks)
        return
    bitlink = get_short_link(args.link, api_token)
    if bitlink:
        print(bitlink)
        return
    print('Mistake, try again')


if __name__ == '__main__':
    main()
