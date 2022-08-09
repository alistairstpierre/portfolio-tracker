import os
from sqlite3 import Cursor
import requests
import urllib.parse
import json

session = requests.Session()
page_count = 0
api_key = os.environ.get("API_PORTFOLIO_TRACKER")
wallet_address = '0x73CD457e12f5fa160261FEf96C63CA4cA0478b2F'     

def get_jobs():
    url = f'https://deep-index.moralis.io/api/v2/{wallet_address}/nft?chain=eth&format=decimal'
    headers = {'x-api-key':'IakxMY1LaiPnZiKt0kNOdfXGuf2JjAm2GvtYu88JRn7kCCXI8bAy4qtYMhYEE0Ce'}
    current_page = session.get(url, headers=headers).json()
    yield current_page
    cursor = current_page['cursor']
    print(cursor)
    # more_pages = current_page['data']['pagination']['has_more']
    # page_count = 1

    while cursor is not None:
        next_page = session.get(f'{url}&cursor={cursor}', headers=headers).json()
        yield next_page
        cursor = next_page['cursor']
        print(cursor)

def lookup():
    nfts = { 'nfts' : [] }
    for page in get_jobs():
        for nft in page["result"]:
                nfts["nfts"].append(nft)

    with open('json_data.json', 'a') as outfile:
        json.dump(nfts, outfile, indent=4, sort_keys=True)
    
            
# def lookup():
#     """Look up quote for symbol."""

#     # Contact API
#     try:
#         api_key = os.environ.get("API_PORTFOLIO_TRACKER")
#         wallet_address = '0x43a33125418B0dE5Bda8E4f30277e3cD31dc8A80'     
#     #url = f"https://api.covalenthq.com/v1/1/address/{wallet_address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&page-size=1&key={api_key}" 
#         #url = f"https://api.covalenthq.com/v1/1/address/{wallet_address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&key={api_key}"
#         url = f"https://api.covalenthq.com/v1/1/address/{wallet_address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&page-size=1&key={api_key}"
#         response = requests.get(url)
#         response.raise_for_status()
#         print(response)
#     except requests.exceptions.HTTPError as error:
#         print(error)
#         return None
#     except requests.exceptions.TooManyRedirects as error:
#         print(error)
#         return None
#     except requests.ConnectionError as error:
#         print(error)
#         return None

#     # Parse response
#     try:
#         quote = response.json()
#         more_pages = quote['data']['pagination']['has_more']
#         print(json.dumps(quote, indent=4, sort_keys=True))
#         # return {
#         #     "name": quote["companyName"],
#         #     "price": float(quote["latestPrice"]),
#         #     "symbol": quote["symbol"]
#         # }
#     except (KeyError, TypeError, ValueError):
#         return None