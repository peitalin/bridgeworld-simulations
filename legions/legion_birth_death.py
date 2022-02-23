import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot

from params import QUEST_TIMES, CRAFT_TIMES, PR_DROP_LOOT_FROM_QUEST
from legion import Legion


def pop(
    N = 100,
    k = 100,
    b = 1,
    d = 0,
    f = lambda N,k: N/k
):
    """
        N: summoning population size
        b: birth rate
        d: death rate
        k: carrying capacity (crafting population)
    """
    return (b * f(N, k) - d) * N


def linear(N = 100, k = 100):
    return (1 - N/k)

def inverse_linear(N = 100, k = 100):
    return 1 / (1 + N/k)

def inverse_quad(N = 100, k = 100):
    return 1 / (1 + (N/k)**2)

def inverse_exp(N = 100, k = 100):
    return np.exp(-np.log(2) * N / k)


colors = [
    'crimson',
    'mediumorchid',
    'royalblue',
    'black',
]

N = np.linspace(0, 2000, 2001)
N_k200 = [n/200 for n in N]
N_k400 = [n/400 for n in N]
N_k800 = [n/800 for n in N]

# dN_dt_1 = [pop(N=n, k=200, f=logistic) for n in N]
# dN_dt_2 = [pop(N=n, k=400, f=logistic) for n in N]
# dN_dt_3 = [pop(N=n, k=800, f=logistic) for n in N]
dN_dt_1 = [inverse_exp(N=n, k=200) for n in N]
dN_dt_2 = [inverse_exp(N=n, k=400) for n in N]
dN_dt_3 = [inverse_exp(N=n, k=800) for n in N]

# change in growth rate, vs population
plt.plot(N, dN_dt_1, label="#crafters=200", color=colors[0])
plt.plot(N, dN_dt_2, label="#crafters=400", color=colors[1])
plt.plot(N, dN_dt_3, label="#crafters=800", color=colors[2])

plt.grid(color='black', alpha=0.15)
plt.legend()
plt.ylabel("%Chance of Summon Success")
plt.xlabel("Number of Legions")
plt.title("%Chance of Summon Success vs Legion population")
plt.show()








# treasure_demand = crafting_for_harvesters + crafting_for_summoning_boosts
# + crafting_in_ecosystem_partners + more_utility_for_treasures

# treasure_supply = legions_questing * drop_rate
# supply is a function of treasure prices, there is no supply-side scarcity
# it depends on legions questing, in tun determined by summoning rates

# legions_questing = percentage_of_legions_questing * legions
# legions = (n * (n - 1)) / 2
# # where n is nth summoning period
# # legions population accelerates over time

# legions_questing = percentage_of_legions_questing * legions

# Er[questing] = PR_DROP_LOOT_FROM_QUEST * drop_rate_weighted_price of treasures
# # [drop_rate * price for drop_rate, price in [t1, t2, t3, t4, t5 treasure tiers]]

# Er[mining] = NFTBoost * user_wealth
# # legions are more useful in the mine for richer users

# Er[summoning] = -500MAGIC - opportunity_cost_of_questing_1_week + Er[questing at t+1]
# # sacrifice 1 period of questing/mining and 500 MAGIC for 1x  lifetime value of a legion
# # which is an income stream of questing 1 period from now = Er_t+1[questing]



## Prices are a function of supply and demand
prices = [
    1000,
    400,
    315,
    75,
    10,
]

def pr_weighted_price_of_treasures(lvl='easy'):
    # pr: probabilities of dropping t1, t2, t3, t4, t5 loot
    # in percentages
    if lvl=='easy':
        pr = [0.0, 0.025, 0.05, 0.15, 0.775]
    if lvl=='medium':
        pr = [0.015, 0.05, 0.07, 0.17, 0.695]
    if lvl=='hard':
        pr = [0.025, 0.09, 0.08, 0.022, 0.0585]
    return np.sum([price*prob for price,prob in zip(prices,pr)])






## Weekly expected ROI on differnet legion pathways
def expected_roi_questing(lvl='easy', days=7):
    # Er[questing] = PR_DROP_LOOT_FROM_QUEST * drop_rate_weighted_price of treasures
    # [drop_rate * price for drop_rate, price in [t1, t2, t3, t4, t5 treasure tiers]]

    nquests = 24 / QUEST_TIMES[lvl] * days
    roi = PR_DROP_LOOT_FROM_QUEST * nquests * pr_weighted_price_of_treasures(lvl)
    return roi
    # return 1 / population_questing


def expected_roi_mining(aum=50_000, nftBoost=0.75):
    # Er[mining] = NFTBoost * user_wealth
    # legions are more useful in the mine for richer users
    weeks = 52
    return aum * nftBoost / weeks


def expected_roi_summoning():
    # Er[summoning] = -500MAGIC - opportunity_cost_of_questing_1_week + Er[questing at t+1...]
    # sacrifice 1 period of questing/mining and 500 MAGIC for 1x  lifetime value of a legion
    # which is an income stream of questing 1 period from now = Er_t+1[questing]

    opportunity_cost_of_questing_1_week = expected_roi_questing()
    ltv_questing = expected_roi_questing() / 0.08 # assume 8% discount rate or roughly 12 week return
    return -500 - opportunity_cost_of_questing_1_week + ltv_questing


print('expected_roi_questing', expected_roi_questing() * 12)
print('expected_roi_mining' , expected_roi_mining())
print('expected_roi_summoning' , expected_roi_summoning())

