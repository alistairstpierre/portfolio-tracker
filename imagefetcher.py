import asyncio
from asyncio.windows_events import NULL
import string
import aiohttp
import time
import json

async def get(nft, session):
    url = nft['token_uri']
    name = nft['name']
    if url != 'Invalid uri' and nft['metadata'] != 'null':
        try:
            async with session.get(url=url) as response:
                resp = await response.read()
                # print("Successfully got url {} with resp of length {}.".format(url, len(resp)))
                ret = await response.text()
                return ret 
                    
        except Exception as e:
            print("Unable to get {} due to {}.".format(name, e.__class__))


async def main(nfts):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(nft, session) for nft in nfts])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))
    return ret

def format_urls(nfts):
    start = time.time()
    metadata = asyncio.run(main(nfts))
    end = time.time()

    for i in range(len(nfts)):
        nfts[i]['token_uri'] = metadata[i]
    for nft in nfts:
        data = nft['token_uri']
        if data != None:
            if is_json(data):
                data = json.loads(data)
                nft['token_uri'] = url_cleanup(data['image'])


    nfts = [x for x in nfts if not x['token_uri'] == None]

    print("Took {} seconds to pull {} websites.".format(end - start, len(nfts)))
    return nfts

def url_cleanup(url):
    temp = url
    if url.startswith('ipfs://'):
        temp = temp.replace('ipfs://', 'https://ipfs.io/ipfs/')
    return temp

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True