
import requests
import time
from bs4 import BeautifulSoup


url = 'https://api.thegraph.com/subgraphs/name/treasureproject/bridgeworld'

def get_user_query(userId):
    return """
        query {
            user(id: {}) {
                id
                deposits {
                    id
                    amount
                    endTimestamp
                }
            }
        }
    """.format(userId)



# Get all the legions which are closest to lvl 3 or above
def get_crafting_legions(crafting_level=2):
    return """
        query {{
            legionInfos(
                first: 500
                where: {{ crafting_gte: {} }}
            ) {{
                id
                craftingXp
                crafting
                role
                rarity
            }}
        }}
    """.format(crafting_level)


def get_user_from_legion_id(legion_id="0xfe8c1ac365ba6780aec5a985d989b327c27670a1-0x5fdd"):
    legion_id = legion_id.replace('-metadata', '')
    return """
        {{
            stakedTokens(where: {{ token: "{legion_id}" }}) {{
                user {{
                    id
                }}
            }}
            crafts(where: {{ token: "{legion_id}", status_not: Finished }}) {{
                user {{
                    id
                }}
            }}
            quests(where: {{ token: "{legion_id}", status_not: Finished }}) {{
                user {{
                    id
                }}
            }}
            summons(where: {{ token: "{legion_id}", status_not: Finished }}) {{
                user {{
                    id
                }}
            }}
        }}
    """.format(legion_id=legion_id)


def get_owner_id(response):

    owners_raw = json.loads(response.text)['data']

    stakedTokens = owners_raw['stakedTokens']
    crafts = owners_raw['crafts']
    quests = owners_raw['quests']
    summons = owners_raw['summons']

    if len(stakedTokens) > 0:
        user = stakedTokens[0].get('user')
    elif len(crafts) > 0:
        user = crafts[0].get('user')
    elif len(quests) > 0:
        user = quests[0].get('user')
    elif len(summons) > 0:
        user = summons[0].get('user')
    else:
        user = None

    if user:
        return user.get('id')
    else:
        return None



def get_legion_id(id):
    # '0xfe8c1ac365ba6780aec5a985d989b327c27670a1-0x1016-metadata'
    # middle part is a hex => int(hex) to get id of token
    return int(id.split("-")[1], base=16)



## 1. get legions on the brink of becoming lvl 3
legions_crafters = requests.post(
    url,
    headers={},
    json={
        'query': get_crafting_legions(),
        'variables': {},
    },
)

legions_crafters_raw_data = json.loads(legions_crafters.text)
legions = legions_crafters_raw_data ["data"]["legionInfos"]


for legion in legions:
    if legion.get('ownerId'):
        print("skipping ", legion.get('tokenId'))
        continue

    legion_id = legion['id'].replace('-metadata', '')
    token_id = get_legion_id(legion_id)
    print("fetching tokenId: ", token_id)
    r = requests.post(
        url,
        headers={},
        json={
            'query': get_user_from_legion_id(legion_id),
            'variables': {},
        },
    )
    owner_id = get_owner_id(r)

    legion['id'] = legion_id
    legion['tokenId'] = token_id
    legion['ownerId'] = owner_id
    time.sleep(0.25)




import asyncio
from pyppeteer import launch

missing_owners = []

async def get_owner_from_arbiscan(tokenIds=[10180, 2298]):

    ARB_URL = "https://arbiscan.io"
    ARB_721_OWNER_QUERY = ARB_URL + "/token/0xfe8c1ac365ba6780aec5a985d989b327c27670a1"
    browser = await launch(headless=False)
    page = await browser.newPage()

    for tokenId in tokenIds:
        query = ARB_721_OWNER_QUERY + "?a={}#inventory".format(tokenId)
        await page.goto(query)
        await page.waitFor(4000)
        new_addr = await page.evaluate('''() => {
            let iframe1 = document.getElementById('tokenerc721_inventory_pageiframe')
            let alist = iframe1.contentWindow.document.querySelectorAll("a")
            return Object.values(alist).map(a => a.innerText)
        }''')
        missing_owners.append(new_addr)
        print(new_addr)

    await browser.close()

get_owner_from_arbiscan()


def get_user_balance(addr=''):
    ARB_API_URL = "https://api.arbiscan.io/api"
    # arbiscane API key, can just revoke
    API_KEY = ""
    ARB_BALANCE_QUERY =  ARB_API_URL + "?module=account&action=tokenbalance&tag=latest&apikey={}".format(API_KEY)
    MAGIC_ERC20 = "0x539bdE0d7Dbd336b79148AA742883198BBF60342"
    ARB_BALANCE_QUERY += "&contractaddress={}&address={}".format(MAGIC_ERC20, addr)
    r = requests.get(ARB_BALANCE_QUERY)
    balance = json.loads(r.text)
    balance2 = balance.get("result")
    if balance2:
        return int(balance2) / 1e18
