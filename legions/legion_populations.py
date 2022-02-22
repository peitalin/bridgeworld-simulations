import numpy as np

from params import QUEST_TIMES, CRAFT_TIMES
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
        num_legions = 2000,
        num_legions_summoning = 50,
        rolling_mean_lag = 3,
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

        """.format(
            pct_crafting=self.pct_crafting,
            pct_questing=self.pct_legions_to_questing,
        )

    def get_rolling_mean_treasure_supply(self, tier='t5'):
        """ tier = treasure tier
            lag = num periods back to average over """

        lag = self.rolling_mean_lag
        net_diff_treasures_history = self.treasureAccounting.net_diff_treasures_history
        rolling_mean_treasure_supply = np.mean(net_diff_treasures_history[tier][-lag:])
        return rolling_mean_treasure_supply


    def update_pct_legions_questing(self, tier='t5'):

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






# treasure_demand = crafting_for_harvesters + crafting_for_summoning_boosts
# + crafting_in_ecosystem_partners + more_utility_for_treasures

# treasure_supply = legions_questing * drop_rate
# # supply is a function of treasure prices, there is no supply-side scarcity
# # it depends on legions questing, in tun determined by summoning rates

# legions_questing = percentage_of_legions_questing * legions
# legions = (n * (n - 1)) / 2
# # where n is nth summoning period
# # legions population accelerates over time

# legions_questing = percentage_of_legions_questing * legions

# Er[questing] = 0.2 * drop_rate_weighted_price of treasures
# # [drop_rate * price for drop_rate, price in [t1, t2, t3, t4, t5 treasure tiers]]

# Er[mining] = NFTBoost * user_wealth
# # legions are more useful in the mine for richer users

# Er[summoning] = -500MAGIC - opportunity_cost_of_questing_1_week + Er[questing at t+1]
# # sacrifice 1 period of questing/mining and 500 MAGIC for 1x  lifetime value of a legion
# # which is an income stream of questing 1 period from now = Er_t+1[questing]
