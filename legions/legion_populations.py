import numpy as np

from params import QUEST_TIMES, CRAFT_TIMES, PR_DROP_LOOT_FROM_QUEST
from legion import Legion


## Naive legion populations, based on net inflation/deflation of treasures
def calculate_percentage_legion_questing(
    net_inflation_deflation = 0,
    threshold_upper = 500,
    threshold_lower = 500,
    max_pct_upper = 0.8,
    min_pct_lower = 0.4,
):
    """
        net_inflation_deflation: net inflation/deflation of a particular tier of treasures
        threshold_upper: upper threshold where 100% of legions are crafting
        threshold_lower: lower threshold where 100% of legions are questing
        offset: makes sure percentage_legion_questing stays within this thresholds
    """

    if net_inflation_deflation >= 0:
        # too much inflation, less legions questing pls
        pct = (100 - (threshold_lower + net_inflation_deflation)/10) / 100
    else:
        # too much burn, more legions questing pls
        pct = (100 - (threshold_upper + net_inflation_deflation)/10) / 100

    if pct >= max_pct_upper:
        return max_pct_upper
    elif pct <= min_pct_lower:
        return min_pct_lower
    else:
        return pct




class LegionPopulations:

    def __init__(
        self,
        treasureAccounting,
        num_legions = 1000,
        num_legions_summoning = 50,
        rolling_mean_lag = 7,
    ):
        self.treasureAccounting = treasureAccounting
        self.pct_crafting = []
        self.pct_questing = []

        self.legions_summoning = [Legion(treasureAccounting) for l in range(num_legions_summoning)]
        self.legions_all = [Legion(treasureAccounting) for l in range(num_legions)]
        self.legions_questing = []
        self.legions_crafting = []

        self.pct_legions_to_questing = 0.5
        self.rolling_mean_lag = rolling_mean_lag

    def __repr__(self):
        return """
        ========== Legion Populations ==========
        %Legions Crafting: {pct_crafting}
        %Legions Questing: {pct_questing}

        #Craftors: {num_crafting}
        #Questors: {num_questing}
        #Summoners: {num_summoning}
        Total Legions: {num_legions}
        """.format(
            pct_crafting=self.pct_crafting,
            pct_questing=self.pct_legions_to_questing,
            num_craftors=len(self.legions_crafting),
            num_questors=len(self.legions_questors),
            num_summoners=len(self.legions_summoners),
            num_legions=len(self.legions_all),
        )

    def get_rolling_mean_treasure_supply(self, tier='t5'):
        """ tier = treasure tier
            lag = num periods back to average over """

        lag = self.rolling_mean_lag
        net_diff_treasures_history = self.treasureAccounting.net_diff_treasures_history
        rolling_mean_treasure_supply = np.mean(net_diff_treasures_history[tier][-lag:])
        return rolling_mean_treasure_supply


    def update_legion_populations(self, tier='t5', summoning_cycle_complete=False):

        lag = self.rolling_mean_lag
        rolling_mean_treasure_supply = self.get_rolling_mean_treasure_supply(tier)

        if not np.isnan(rolling_mean_treasure_supply):
            ## Replace with model that actually models population dynamics between:
            # questors, craftors, miners, summoners
            # with a system of equations
            pct_legions_to_questing = calculate_percentage_legion_questing(rolling_mean_treasure_supply)
        else:
            pct_legions_to_questing = 0.5

        self.pct_questing.append(pct_legions_to_questing)
        self.pct_crafting.append(1 - pct_legions_to_questing)

        ## Reset population of legions crafting vs questing every iteration
        ## to let legions freely switch between questing or crafting
        num_legions = len(self.legions_all)
        num_legions_questing = int(num_legions * pct_legions_to_questing)
        num_legions_crafting = int(num_legions * (1 - pct_legions_to_questing))

        self.legions_questing = self.legions_all[:num_legions_questing] if num_legions_questing > 0 else []
        self.legions_crafting = self.legions_all[-num_legions_crafting:] if num_legions_crafting > 0 else []

        if summoning_cycle_complete:
            # new batch of summoned legions
            new_aux_legions = self.legions_summoning.copy()
            midpoint_new_legions = int(len(new_aux_legions)/2)

            first_half_legions = new_aux_legions[:midpoint_new_legions] if midpoint_new_legions > 0 else []
            last_half_legions = new_aux_legions[midpoint_new_legions:] if midpoint_new_legions > 0 else []

            # half in front, half at back so we distribute new summons evenly across
            # crafting and questing (which is split in middle)
            [self.legions_all.insert(0, s) for s in first_half_legions]
            [self.legions_all.append(s) for s in last_half_legions]






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

