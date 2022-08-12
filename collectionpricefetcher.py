import asyncio
from asyncio.windows_events import NULL
import string
import aiohttp
import time
import json
from itertools import zip_longest
import web3

async def get(nft, session, days):
    if nft != None:
        contract = nft['contract']
        print(f'contract {contract}')
        url = f"https://deep-index.moralis.io/api/v2/nft/{contract}/lowestprice?chain=eth&days={days}&marketplace=opensea"
        headers = {
            "Accept": "application/json",
            "X-API-Key": "IakxMY1LaiPnZiKt0kNOdfXGuf2JjAm2GvtYu88JRn7kCCXI8bAy4qtYMhYEE0Ce"
        }
        try:
            async with session.get(url=url, headers=headers) as response:
                resp = await response.read()
                # print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
                ret = await response.text()
                print(f'response {ret}')
                return ret 
                    
        except Exception as e:
            print("Unable to get {} due to {}.".format(nft['name'], e.__class__))


async def main(collection_data, days):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(nft, session, days) for nft in collection_data])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))
    return ret

def get_collection_prices(collection_data):
    temp = []
    days = 1
    for output in group_elements(5,collection_data):
        metadata = asyncio.run(main(output, days))
        for data in metadata:
            temp.append(data)
        time.sleep(1.1)

    for i in range(len(temp)):
        data = temp[i]
        if data != None:
            if is_json(temp[i]):
                price_data = json.loads(temp[i])
                try:
                    collection_data[i]['onedayprice'] = web3.Web3.fromWei(int(price_data['price']), 'ether')
                    print(f"got one day price data for {collection_data[i]['name']} price: {collection_data[i]['onedayprice']}")
                except Exception as e:
                    print(f'could not get one day price data for {collection_data[i]["name"]}')
            else:
                print("price data is not convertable to json")

    temp = []
    days = 7
    for output in group_elements(5,collection_data):
        metadata = asyncio.run(main(output, days))
        for data in metadata:
            temp.append(data)
        time.sleep(1.1)

    for i in range(len(temp)):
        data = temp[i]
        if data != None:
            if is_json(temp[i]):
                price_data = json.loads(temp[i])
                try:
                    collection_data[i]['sevendayprice'] = web3.Web3.fromWei(int(price_data['price']), 'ether')
                    print(f"got seven day price data for {collection_data[i]['name']} price: {collection_data[i]['sevendayprice']}")
                except Exception as e:
                    print(f'could not get one day price data for {collection_data[i]["name"]}')
            else:
                print("price data is not convertable to json")

    collection_data = [x for x in collection_data if 'onedayprice' in x or 'sevendayprice' in x]
    return collection_data

def group_elements(n, iterable, padvalue=None):
    return zip_longest(*[iter(iterable)]*n, fillvalue=padvalue)

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

