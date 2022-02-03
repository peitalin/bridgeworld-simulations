import sys
sys.path.append("..")
# for imports from parent directory

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

# parameters for configuring boosts
from parameters import PARTS_BOOST_FACTOR, LEGIONS_BOOST_FACTOR
from parameters import ATLAS_MINE_BONUS, EXPECTED_ATLAS_AUM, MAX_HARVESTER_PARTS, MAX_EXTRACTORS
from parameters import MIN_LEGIONS, MAX_LEGIONS
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS

from harvester_boosts import get_treasure_boost, parts_boost_harvester, legions_boost_harvester
from harvester_boosts import extractors_boost_harvester, total_harvester_boost, user_boost_inside_harvester
from harvester_boosts import calculate_avg_legion_rank

from plots.compare_6_harvesters import calculate_harvester_splits


#################################
####### SIMULATES USERS YIELD INSIDE HARVESTER WITH VARIOUS BOOSTS
#################################


def plot_yield_inside_mine(treasure_multiplier=1, legion_boost=1, linestyle='-', color='blue'):

    # # staking boosts for treasures
    m = treasure_multiplier
    honeycomb = 0.02631 * m
    quarter_penny = 0.0025 * m

    rank0 = 1+0.05 # common gen 1: 5% boost
    rank3 = 1+1 # uncommon: 100% boost
    rank4 = 1+2 # all-class 200% boost
    rank5 = 1+6 # 1/1 600% boost


    x1_num_treasures = np.linspace(0,50,51)
    # let daily emissions to atlas mine be 50,000
    daily_magic_emissions = 50000

    harvesters = [
        {
            'parts': 500,
            'legions': 3000,
            'avg_legion_rank': 2,
            'extractors': [],
        }
    ]

    (
        boost_atlas,
        mine_pct_share_atlas,
        user_pct_share_atlas,
        harvester_boosts,
        mine_pct_shares,
        user_pct_shares,
    ) = calculate_harvester_splits(harvesters=harvesters, debug=True)

    boost_h1 = harvester_boosts[0]
    mine_pct_share_h1 = mine_pct_shares[0]
    user_pct_share_h1 = user_pct_shares[0]


    x3_num_magic_daily_atlas = user_pct_share_atlas * daily_magic_emissions
    x3_num_magic_daily_h1_max = user_pct_share_h1 * daily_magic_emissions

    # honeycomb boost as you stack more and more honeycombs (up to 200)
    honeycomb_boosts = [(1+honeycomb)**n for n in x1_num_treasures]
    honeycomb_boosts2 = [(1+honeycomb*n) for n in x1_num_treasures]
    # quarter_pennny boost as you stack more and more (up to 200)
    quarter_penny_boosts = [(1+quarter_penny)**n for n in x1_num_treasures]
    # quarter_penny_boosts = [(1+quarter_penny*n) for n in x1_num_treasures]

    # plt.plot(x1_num_treasures, honeycomb_boosts, label="Stacking honeycombs, multiplicately", color="red", linestyle="-.")
    # plt.plot(x1_num_treasures, honeycomb_boosts2, label="Stacking honeycombs, sum", color="blue", linestyle="--")
    honeycomb_legion_boosts = [(1+honeycomb)**n * legion_boost for n in x1_num_treasures]
    honeycomb2_legion_boosts = [(1+honeycomb*n) * legion_boost for n in x1_num_treasures]
    quarter_penny_boosts = [(1+quarter_penny)**n * legion_boost for n in x1_num_treasures]

    # plt.plot(x1_num_treasures, honeycomb_legion_boosts, label="honeycombs (multiplicative), legion boost {}x".format(legion_boost), linestyle=linestyle, color=color)
    plt.plot(x1_num_treasures, honeycomb2_legion_boosts, label="honeycombs (sum), legion boost {}x".format(legion_boost), linestyle='-', color=color)
    plt.xlabel("#treasures staked")
    plt.ylabel("boost (x)")


    x4_no_treasures_h1_max = [x3_num_magic_daily_atlas * legion_boost for h in honeycomb_boosts]

    # Number of magic earned daily after boosting with n staked honeycombs
    x4_honeycomb_boosted_atlas = [x3_num_magic_daily_atlas * h * legion_boost for h in honeycomb_boosts]
    x4_honeycomb_boosted_h1_max = [x3_num_magic_daily_h1_max * h * legion_boost for h in honeycomb_boosts]

    x4_honeycomb_boosted_atlas2 = [x3_num_magic_daily_atlas * h * legion_boost for h in honeycomb_boosts2]
    x4_honeycomb_boosted_h1_max2 = [x3_num_magic_daily_h1_max * h * legion_boost for h in honeycomb_boosts2]

    # Number of magic earned daily after boosting with n staked quarter_penny
    x4_quarter_penny_boosted_atlas = [x3_num_magic_daily_atlas * h * legion_boost for h in quarter_penny_boosts]
    x4_quarter_penny_boosted_h1_max = [x3_num_magic_daily_h1_max * h * legion_boost for h in quarter_penny_boosts]


    ##### Comparing growth rates of stacking up to 20 treasures
    # # plt.plot(x1_num_treasures, x4_honeycomb_boosted_atlas, label="Stacking honeycombs", color="orange", linestyle="-.")
    # plt.plot(x1_num_treasures, x4_no_treasures_h1_max , label="No treasures staked, boosted mine", color="blue", linestyle="-")
    #
    # plt.plot(x1_num_treasures, x4_honeycomb_boosted_atlas, label="Stacking honeycombs, unboosted mine", color="red", linestyle="-.")
    # plt.plot(x1_num_treasures, x4_quarter_penny_boosted_atlas, label="Stacking quarter-pennies, unboosted mine", color="red", linestyle="--")
    # # fill between upper and lower bound
    # plt.fill_between(x1_num_treasures, x4_quarter_penny_boosted_atlas, x4_honeycomb_boosted_atlas, facecolor="red", alpha=0.2)
    #
    # plt.plot(x1_num_treasures, x4_honeycomb_boosted_h1_max, label="Stacking honeycombs, boosted mine", color="purple", linestyle="-.")
    # plt.plot(x1_num_treasures, x4_quarter_penny_boosted_h1_max, label="Stacking quarter-pennies, boosted mine", color="purple", linestyle="--")
    # # fill between upper and lower bound
    # plt.fill_between(x1_num_treasures, x4_quarter_penny_boosted_h1_max, x4_honeycomb_boosted_h1_max, facecolor="purple", alpha=0.2)


    baseline_magic = x4_no_treasures_h1_max[-1] # 5.51 magic/day on 10k
    penny_cost = 83
    honey_cost = 3200
    num = len(x1_num_treasures) - 1 # 20

    # incremental income from staking 20 pennies
    penny_income_20 = x4_quarter_penny_boosted_h1_max[-1] - baseline_magic
    penny_income_1 = x4_quarter_penny_boosted_h1_max[0] - baseline_magic

    honey_income_20 = x4_honeycomb_boosted_h1_max[-1] - baseline_magic
    honey_income_1 = x4_honeycomb_boosted_h1_max[0] - baseline_magic


    payback_pennies = [penny_cost*n / income for n,income in enumerate(x4_quarter_penny_boosted_h1_max)]
    payback_honey = [honey_cost*n / income for n,income in enumerate(x4_honeycomb_boosted_h1_max)]
    payback_honey2 = [honey_cost*n / income for n,income in enumerate(x4_honeycomb_boosted_h1_max2)]

    ##### Payback period plots
    # plt.plot(x1_num_treasures, payback_honey,
    #         label="Payback (days) honeycombs, {}x treasure, {}x legion boost".format(m, legion_boost),
    #         color="orange",
    #         linestyle=linestyle)
    # plt.plot(x1_num_treasures, payback_honey,
    #         label="Payback (days) honeycombs, multiplicative".format(m, legion_boost),
    #         color="orange",
    #         linestyle=linestyle)
    # plt.plot(x1_num_treasures, payback_honey2,
    #         label="Payback (days) honeycombs, additive".format(m, legion_boost),
    #         color="blue",
    #         linestyle=linestyle)
    # plt.plot(x1_num_treasures, payback_pennies,
    #          label="Payback (days) pennies, {}x treasure, {}x legion boost".format(m, legion_boost),
    #          color="black",
    #          linestyle=linestyle)

    # plt.xlabel("Varying number of parts staked")
    # plt.ylabel("Boost multiplier")
    # plt.title("Total Harvester Boost (parts x legions boost)")
    # plt.text(150, 2.0, "guilds will have boosts\n in this region")
    plt.show()




