
import requests
import time
import pandas as pd
import asyncio
from pyppeteer import launch

ARBISCAN_API_KEY=""


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



def get_legions_on_brink_of_parts():
    ## 1. get legions on the brink of becoming lvl 3
    legions_crafters = requests.post(
        url,
        json={
            'query': get_crafting_legions(),
        },
    )

    legions_crafters_raw_data = json.loads(legions_crafters.text)
    legions = legions_crafters_raw_data ["data"]["legionInfos"]
    return legions


def get_owner_of_legion(legions=[]):
    for legion in legions:
        if legion.get('ownerId'):
            print("skipping ", legion.get('tokenId'))
            continue

        legion_id = legion['id'].replace('-metadata', '')
        token_id = get_legion_id(legion_id)
        print("fetching tokenId: ", token_id)
        r = requests.post(
            url,
            json={
                'query': get_user_from_legion_id(legion_id),
            },
        )
        owner_id = get_owner_id(r)

        legion['id'] = legion_id
        legion['tokenId'] = token_id
        legion['ownerId'] = owner_id
        time.sleep(0.25)

    return legions



async def get_owner_from_arbiscan(tokenIds=[], found_owners=[]):

    ARB_URL = "https://arbiscan.io"
    ARB_URL = "https://arbiscan.io"
    # legions contract
    ARB_721_OWNER_QUERY = ARB_URL + "/token/0xfe8c1ac365ba6780aec5a985d989b327c27670a1"
    browser = await launch(headless=False)
    page = await browser.newPage()
    # tokenIds = [10018, 10019, 10120, 10180, 16321, 138]
    tokenIds = legions_missing_owners

    for tokenId in tokenIds:
        query = ARB_721_OWNER_QUERY + "?a={}#inventory".format(tokenId)
        await page.goto(query)
        await page.waitFor(4000)
        new_addr = await page.evaluate('''() => {
            let iframe1 = document.getElementById('tokenerc721_inventory_pageiframe')
            let alist = iframe1.contentWindow.document.querySelectorAll("a")
            return Object.values(alist).map(a => a.innerText)
        }''')
        found_owners.append(new_addr)
        print(new_addr)

    await browser.close()
    return [tokenIds, found_owners]




def get_user_balance(addr='0x08ef1a3a2428c7a0ca92fa248b012f07f676ba95'):
    ARB_API_URL = "https://api.arbiscan.io/api"
    # arbiscane API key, can just revoke
    ARB_BALANCE_QUERY =  ARB_API_URL + "?module=account&action=tokenbalance&tag=latest&apikey={}".format(ARBISCAN_API_KEY)
    MAGIC_ERC20 = "0x539bdE0d7Dbd336b79148AA742883198BBF60342"
    ARB_BALANCE_QUERY += "&contractaddress={}&address={}".format(MAGIC_ERC20, addr)
    r = requests.get(ARB_BALANCE_QUERY)
    balance = json.loads(r.text)
    balance2 = balance.get("result")
    balance3 = int(balance2) / 1e18
    print('\naddr:', addr)
    print('balance:', balance3)
    return balance3 if balance3 else 0





# 1. get legions close to lvl3 crafting or above
legions = get_legions_on_brink_of_parts()
# 2. get the owner's address of each legion
legions2 = get_owner_of_legion(legions)
# 3. for the missing owners not in quest/craft/summon/mine (in wallet),
## track down their owner address by scraping arbiscan
## with the get_owner_from_arbiscan() function

## 4. Import legions into a dataframe
ddat = pd.DataFrame(legions2)
ddat = ddat.set_index('id')

## 5. Match the legions missing owners from arbiscan to the legions
legions_missing_owners = [x['tokenId'] for x in legions if x['ownerId'] is None]
found_owners = []

for owner in found_owners:
    tokenId = int(owner[0])
    ownerAddr = owner[1]
    ddat.loc[ddat["tokenId"] == tokenId, 'ownerId'] = ownerAddr

[legions_missing_owners, found_owners] = get_owner_from_arbiscan(legions_missing_owners)
ddat.to_csv("crafter_without_balances.csv")







## 6. once you have all legions and their owners, get their:
## a) deposits expiring in the next month before harvesters launch
## b) their wallet balance from arbiscan


def get_unlocking_deposits_from_atlas(ddat):
    ### Get Atlas Mine deposits that will expire in the next month before harvesters launch
        # enum Lock { twoWeeks, oneMonth, threeMonths, sixMonths, twelveMonths }
        # 0: twoWeeks
        # 1: oneMonth
        # 2: threeMonths
        # ...

    QUERY_ATLAS_DEPOSITS = """
    query {{
        users(where: {{ id_in: ["{userId}"] }}) {{
            id
            deposits(where: {{ lock_in: [0,1] }}) {{
                id
                amount
                endTimestamp
                lock
            }}
        }}
    }}
    """

    user_deposits = []

    for userId in ddat['ownerId']:
        res2 = requests.post(
            url,
            json={ 'query': QUERY_ATLAS_DEPOSITS.format(userId=userId) },
        )
        adata = json.loads(res2.text)
        # print(adata)
        _users = adata['data']['users']
        total_deposits_in_1_month = 0

        if len(_users) > 0:
            _u = _users[0]
            _udeposits = _u['deposits']
            _uid = _u['id']
            user_deposits.append(_u)

            if len(_udeposits) > 0:
                for d in _udeposits:
                    total_deposits_in_1_month += int(d['amount']) / 1e18
                    print("\nuser: ", _uid)
                    print("totalDeposits", total_deposits_in_1_month )
                    ddat.loc[ddat["ownerId"] == _uid, 'atlas_deposit_unlocking'] = total_deposits_in_1_month

    return ddat


## warning: we get the atlas deposits for each legion -> user -> deposit
## meaning the data here has duplicate entries,
ddat2 = get_unlocking_deposits_from_atlas(ddat)
# need to remove duplicates before aggregating

def merge_legions_on_user_address(ddat2):
    players = {}
    for row in ddat2.iterrows():

        legionId = row[1][4]
        ownerId = row[1][5]
        atlasDeposit = row[1][6]
        print('\nlegionId: ',legionId)
        print('ownerId: ', ownerId)
        print('atlasDeposit: ', atlasDeposit)

        if players.get(ownerId):
            players[ownerId]['legionIds'].append(legionId)
        else:
            players[ownerId] = {
                'ownerId': ownerId,
                'legionIds': [legionId],
                'atlas_deposit_unlocking': atlasDeposit
            }

    return players


players = merge_legions_on_user_address(ddat2)
ddat_no_dupes = pd.DataFrame.from_dict(players, orient='index')
ddat_no_dupes = ddat_no_dupes.set_index('ownerId')
# ddat_no_dupes = ddat2.drop_duplicates(subset=['ownerId'])
# ddat_no_dupes = ddat_no_dupes.set_index('ownerId')


# def get_wallet_balances(ddat_no_dupes):
#     ### Get Wallet magic balances
#     for ownerId in ddat_no_dupes.index:
#         balance = get_user_balance(ownerId)
#         ddat_no_dupes.loc[ddat_no_dupes.index == ownerId, 'wallet_balance'] = balance
#     return ddat_no_dupes

# ddat_no_dupes = get_wallet_balances(ddat_no_dupes)

for ownerId in ddat_no_dupes.index:
    if not ownerId:
        print("ownerId missing")
        balance = 0
    else:
        balance = get_user_balance(ownerId)

    ddat_no_dupes.loc[ddat_no_dupes.index == ownerId, 'wallet_balance'] = balance

ddat_no_dupes.to_csv("crafter_balances.csv")



#### Aggregate balances across atlas and wallet balances,
#### and merge duplicate wallet's balances

wallets_balances = {}
unique_wallets = 0
total_magic_depositable_in_harvesters = 0

for row in ddat_no_dupes.iterrows():
    addr = row[0]
    atlas_deposit = row[1][1]
    wallet_balance = row[1][2]

    atlas_deposit = atlas_deposit if not np.isnan(atlas_deposit) else 0
    wallet_balance = wallet_balance if not np.isnan(wallet_balance) else 0
    total = atlas_deposit + wallet_balance
    print('addr', addr)
    print('total', total)

    total_magic_depositable_in_harvesters += total

    if wallets_balances.get(addr):
        wallets_balances[addr] += total
    else:
        unique_wallets += 1
        wallets_balances[addr] = total

print("\nUnique addresses", unique_wallets)
print("Total magic deployable in harvesters by crafterse", total_magic_depositable_in_harvesters)
