import sys
sys.path.append("..")
# for imports from parent directory

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot

# parameters for configuring boosts
from parameters import PARTS_BOOST_FACTOR, LEGIONS_BOOST_FACTOR
from parameters import ATLAS_MINE_BONUS, EXPECTED_ATLAS_AUM, MAX_HARVESTER_PARTS, MAX_EXTRACTORS
from parameters import MIN_LEGIONS, MAX_LEGIONS
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS

from harvester_boosts import get_treasure_boost, parts_boost_harvester, legions_boost_harvester
from harvester_boosts import extractors_boost_harvester, total_harvester_boost


################ Varying legion numbers, fixed parts
def graph_total_harvester_boost_varying_legions():

    x1_num_parts = np.linspace(0,500,501)
    x2_num_legions = np.linspace(0,2000,501)

    total_boosted_max_hi_legion_rank = [total_harvester_boost(500, x2, [], 4) for x2 in x2_num_legions]
    total_boosted_max = [total_harvester_boost(500, x2, [], 1) for x2 in x2_num_legions]
    total_boosted_min = [total_harvester_boost(1, x2, [], 1)   for x2 in x2_num_legions]

    plt.plot(x2_num_legions, total_boosted_max_hi_legion_rank, label="Harvester with 500 parts; high legion rank", color="orange", linestyle=":")
    plt.plot(x2_num_legions, total_boosted_max, label="Harvester with 500 parts", color="orange", linestyle="-")
    plt.plot(x2_num_legions, total_boosted_min, label="Harvester with 1 part", color="orange", linestyle="--")
    # fill between upper and lower bound
    plt.fill_between(x2_num_legions, total_boosted_min, total_boosted_max, facecolor="orange", alpha=0.2)

    plt.xlabel("Number of legions staked")
    plt.ylabel("Emissions Boost (x)")
    plt.title("Harvester Emissions Boost (parts x legions boost)")
    plt.legend()
    plt.show()


# ###################################
# ###### Parts Boost Graph
# ###################################
def graph_parts_boost():

    x_parts = np.linspace(0, 500, 501)
    parts_boosted = [parts_boost_harvester(x) for x in x_parts]

    plt.plot(parts_boosted)
    plt.xlabel("number of parts")
    plt.ylabel("Boost multiplier")
    plt.title("Harvester Parts Boost")
    plt.grid(color='black', alpha=0.1)
    plt.show()
    # the marginal contribution of each peice of harvester part:
    # marginal_contribution = np.diff(parts_boosted)
    # starts at 2, then works it way down to 0
    # basically the first few parts count for 2, then steadily/linearly approachs 0 as we approach the 500th part
