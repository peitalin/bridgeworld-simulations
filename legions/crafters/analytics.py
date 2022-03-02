import requests

url = 'https://api.thegraph.com/subgraphs/name/treasureproject/bridgeworld'
query = """
    query {
        user(id: "0x62054e5bc3d4111b1b1b9023db95260e01c9c046") {
            id
            deposits {
                id
                amount
                endTimestamp
            }
        }
    }
"""
variables = {}


LEGION_INFOS = """
    query($number: Int) {
        legionInfos(block: { number: $number }) {
            id
            boost
            constellation {
                id
            }
            crafting
            craftingXp
            questing
            questingXp
            rarity
            role
            summons
            type
        }
    }
"""
variables = { 'number': 5065200 }


query = LEGION_INFOS

r = requests.post(
    url,
    headers={},
    json={
        'query': query,
        'variables': variables,
    },
)

print(r.status_code)
print(r.text)