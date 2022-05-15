from plots.compare_6_harvesters import run_harvester_split_simulation_6
from plots.compare_distance import run_distance_boost_simulation

## contracts
from master_of_coin import MasterOfCoin
from harvester_factory import Harvester, HarvesterFactory
from harvester_middleman import UtilizationMiddleman
from harvester_boost_count import total_user_boost_inside_harvester, getNftBoost




# 1. Create MasterOfCoin
master_of_coin = MasterOfCoin()

# 2. create HarvesterFactory
harvester_factory = HarvesterFactory()

# 3. create UtilizationMiddleware
# which can pull emissions from MasterOfCoin
# and has access to harvester utilization and boost info from HarvesterFactory
middleman = UtilizationMiddleman(
	master_of_coin=master_of_coin,
	harvester_factory=harvester_factory
)

# 4. Create harvesters one by one, and watch utilization ratios change
harvester_factory.create_harvester(id=0, aum_staked=5_000_000)
harvester_factory.create_harvester(id=1, aum_staked=6_000_000)
# activate harvester, otherwise it has no impact on emission shares
harvester_factory.harvesters[0].activate()
harvester_factory.harvesters[1].activate()

print(middleman)
print(harvester_factory)

print("\n\t====================================================")
print("\t************ Creating 2 more Harvesters ************")
print("\t====================================================\n")


harvester_factory.create_harvester(id=2, aum_staked=7_000_000)
harvester_factory.create_harvester(id=3, aum_staked=10_000_000)
#
harvester_factory.harvesters[2].activate()
harvester_factory.harvesters[3].activate()

print(middleman)
print(harvester_factory)





# import plotly.graph_objects as go

# c = {
#     "red": '#EBBAB5',
#     "yellow": '#FEF3C7',
#     "green": '#A6E3D7',
#     "purple": '#CBB4D5',
#     "blue": '#bddbec',
#     "black": '#eeeeee',
# }
# red = c['red']
# yellow = c['yellow']
# green = c['green']
# purple = c['purple']
# blue = c['blue']
# black = c['black']


# m = middleman

# amounts = {
#     'atlas': m.atlas_emission_share * m.magic_balance,
#     'h1': m.harvester_emission_shares[0]['emission_share'] * m.magic_balance,
#     'h2': m.harvester_emission_shares[1]['emission_share'] * m.magic_balance,
#     'h3': m.harvester_emission_shares[2]['emission_share'] * m.magic_balance,
#     'h4': m.harvester_emission_shares[3]['emission_share'] * m.magic_balance,
# }
# users = {
#     'User A': amounts['atlas'] * 0.2,
#     'User B': amounts['atlas'] * 0.8,
#     'User C': amounts['h1'] * 0.25,
#     'User D': amounts['h1'] * 0.75,
#     'User E': amounts['h2'] * 0.10,
#     'User F': amounts['h2'] * 0.10,
#     'User G': amounts['h2'] * 0.20,
#     'User H': amounts['h2'] * 0.20,
#     'User I': amounts['h2'] * 0.30,
#     'User J': amounts['h2'] * 0.10,
#     'User K': amounts['h3'] * 0.50,
#     'User L': amounts['h3'] * 0.30,
#     'User M': amounts['h3'] * 0.20,
#     'User N': amounts['h4'] * 0.60,
#     'User O': amounts['h4'] * 0.40,
# }


# flows = [
#     ### Bridgeworld Flows
#     { 'source': 0, 'target': 1, 'l': red, 'n': black, 'amount': amounts['atlas'] },
#     { 'source': 0, 'target': 2, 'l': yellow, 'n': black, 'amount': amounts['h1'] },
#     { 'source': 0, 'target': 3, 'l': green, 'n': black, 'amount': amounts['h2'] },
#     { 'source': 0, 'target': 4, 'l': purple, 'n': black, 'amount': amounts['h3'] },
#     { 'source': 0, 'target': 5, 'l': blue, 'n': black, 'amount': amounts['h4'] },
#     ### Atlas Mine Flows
#     { 'source': 1, 'target': 6, 'l': red, 'n': red, 'amount': users['User A'] },
#     { 'source': 1, 'target': 7, 'l': red, 'n': red, 'amount': users['User B'] },
#     ### Harvester 1 Flows
#     { 'source': 2, 'target': 8, 'l': yellow, 'n': yellow, 'amount': users['User C'] },
#     { 'source': 2, 'target': 9, 'l': yellow, 'n': yellow, 'amount': users['User D'] },
#     ### Harvester 2 Flows
#     { 'source': 3, 'target': 10, 'l': green, 'n': green, 'amount': users['User E'] },
#     { 'source': 3, 'target': 11, 'l': green, 'n': green, 'amount': users['User F'] },
#     { 'source': 3, 'target': 12, 'l': green, 'n': green, 'amount': users['User G'] },
#     { 'source': 3, 'target': 13, 'l': green, 'n': green, 'amount': users['User H'] },
#     { 'source': 3, 'target': 14, 'l': green, 'n': green, 'amount': users['User I'] },
#     { 'source': 3, 'target': 15, 'l': green, 'n': green, 'amount': users['User J'] },
#     ### Harvester 3 Flows
#     { 'source': 4, 'target': 16, 'l': purple, 'n': purple, 'amount': users['User K'] },
#     { 'source': 4, 'target': 17, 'l': purple, 'n': purple, 'amount': users['User L'] },
#     { 'source': 4, 'target': 18, 'l': purple, 'n': purple, 'amount': users['User M'] },
#     ### Harvester 4 Flows
#     { 'source': 5, 'target': 19, 'l': blue, 'n': blue, 'amount': users['User N'] },
#     { 'source': 5, 'target': 20, 'l': blue, 'n': blue, 'amount': users['User O'] },
# ]

# source = [x['source'] for x in flows]
# target = [x['target'] for x in flows]
# values = [x['amount'] for x in flows]
# color_link = [x['l'] for x in flows]
# color_node = [black] + [x['n'] for x in flows]

# label = [
#     'Bridgeworld Emissions',
#     'Atlas Mine',
#     'Harvester 2',
#     'Harvester 3',
#     'Harvester 4',
#     'Harvester 5',
#     'User A',
#     'User B',
#     'User C',
#     'User D',
#     'User E',
#     'User F',
#     'User G',
#     'User H',
#     'User I',
#     'User J',
#     'User K',
#     'User L',
#     'User M',
#     'User N',
#     'User O',
# ]




# # # data to dict, dict to sankey
# # link = dict(source=source, target=target, value=values, color=color_link)
# # node = dict(label=label, pad=15, thickness=5, color=color_node)
# # data = go.Sankey(link=link, node=node)
# # # plot
# # fig = go.Figure(data)
# # fig.update_traces(orientation="h")
# # fig.update_layout(
# #     hovermode = 'x',
# #     title="MAGIC Emission Allocations Between Harvesters",
# #     font=dict(size=10, color='white'),
# #     paper_bgcolor='#5B5958'
# # )
# # fig.show()



# h1 = harvester_factory.harvesters[0]
# h2 = harvester_factory.harvesters[1]
# h3 = harvester_factory.harvesters[2]
# h4 = harvester_factory.harvesters[3]

# h1.stake_parts(800)
# h4.stake_parts(800)

# ### For H1 with 5/10mil AUM (50% utilisation => 80% emissions)
# # 1x emission share: 11.63%
# # 2x emission share * 80% utilisation modifier = 11.63 * 0.8 * 2 = 18.6%

# ### For H4 with 10/10mil AUM (100% utilisation => 100% emissions)
# # 1x emission share: 11.63%
# # 2x emission share = 11.63 * 2 = 23.26%








# ####### Harvesters Yield Wars Simulation #######
# # run_harvester_split_simulation_6()

# ####### Distance Boost Simulation ######
# # run_distance_boost_simulation()