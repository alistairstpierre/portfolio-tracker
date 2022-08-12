from gc import collect
import os
from typing import KeysView
import requests
from imagefetcher import format_urls
from collectionpricefetcher import get_collection_prices

session = requests.Session()
api_key = os.environ.get("API_PORTFOLIO_TRACKER")

def get_jobs(wallet_address):
    url = f'https://deep-index.moralis.io/api/v2/{wallet_address}/nft?chain=eth&format=decimal'
    headers = {'x-api-key':'IakxMY1LaiPnZiKt0kNOdfXGuf2JjAm2GvtYu88JRn7kCCXI8bAy4qtYMhYEE0Ce'}
    current_page = session.get(url, headers=headers).json()
    yield current_page
    cursor = current_page['cursor']

    while cursor is not None:
        next_page = session.get(f'{url}&cursor={cursor}', headers=headers).json()
        yield next_page
        cursor = next_page['cursor']

def lookup(wallet_address):
    nfts = { 'nfts' : [] }
    for page in get_jobs(wallet_address):
        for nft in page["result"]:
            nfts["nfts"].append(nft)

    nfts = format_urls(nfts['nfts'])
    # with open('json_data.json', 'a') as outfile:
    #     json.dump(nfts, outfile, indent=4, sort_keys=True)

    return rebuild_nfts(nfts)

def rebuild_nfts(nfts):
    # rebuild the data so that its organised by collection
    # schema nfts -> collection_name -> collections

    collection_data = []
    collections = set(())
    for nft in nfts:
        if nft['name'] not in collections and nft['name'] != None:
            collections.add(nft['name'])
            collection_data.append({'name':nft['name'], 'contract':nft['token_address']})

    collection_data = get_collection_prices(collection_data)

    collection_data = get_total_prices(collection_data, nfts)

    return { 'collections' : collection_data, 'nfts' : nfts }

def get_total_prices(collection_data, nfts):
    for collection in collection_data:
        count = 0
        total = 0
        for nft in nfts:
            if nft['name'] == collection['name']:
                count += 1
        if 'onedayprice' in collection:
            total = collection['onedayprice'] * count
        else:
            total = collection['sevendayprice'] * count
        collection['totalprice'] = total
        collection['owned'] = count
    return collection_data