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

from harvester_emission_splits import calculate_harvester_splits



#################################
####### COMPARISON TO ATLAS MINE
#################################

# So I compared how boosts affect the split of emissions between the Atlas mine
# and auxiliary harvester.
#
# In the beginning there will only be 1 aux harvester, with low parts and legions
# over time, the harvester will get larger boosts (more parts + legions)
# and more harvesters may come online

# This section models out the early stages of when 1 or 2 harvesters come online
# and can be generalized for when more and more harvesters come online


# The Atlas mine will initially have 0 parts
# Atlas mine can have parts-boosts, maybe Governance votes for outperforming harvesters to
# "become the Atlas mine" where it'll retain the number of parts/boost
# In this instance the choice between staying in the Atlas mine, and creating another Harvester
# is ambiguous, sometimes its better to be in Atlas, but if you are entrepreneurial, starting another
# harvester may be better

## Atlas vs 1 Harvester

# def func_animate(i):

fig, (ax1, ax2, ax3) = plt.subplots(3)

## Array of x-axis data points
x_boost_h1 = []
x_boost_atlas = []

x_mine_pct_share_h1 = []
x_mine_pct_share_atlas = []

x_user_pct_share_h1 = []
x_user_pct_share_atlas = []

days = []

FRAMES = 250
num_obs = 501
_x_parts = np.linspace(0, 500, num_obs) # 1 to 500 parts
_x_legions = np.linspace(0, 2000, num_obs) # 1 to 2000 legions

# def calculate_x_axis_labels():

#     ## Array of x-axis data points
#     x_boost_h1 = []
#     x_boost_h2 = []
#     x_boost_atlas = []

#     x_mine_pct_share_h1 = []
#     x_mine_pct_share_h2 = []
#     x_mine_pct_share_atlas = []

#     x_user_pct_share_h1 = []
#     x_user_pct_share_h2 = []
#     x_user_pct_share_atlas = []


#     num_obs = 501
#     _x_parts = np.linspace(0, 500, num_obs) # 1 to 500 parts
#     _x_members = np.linspace(0, 666.66, num_obs) # 1 to 666 users, 666.6 users * 3 legions = 2000 legions

#     for parts,members in zip(_x_parts, _x_members):

#         (
#             boost_h1,
#             boost_h2,
#             boost_atlas,
#             mine_pct_share_h1,
#             mine_pct_share_h2,
#             mine_pct_share_atlas,
#             user_pct_share_h1,
#             user_pct_share_h2,
#             user_pct_share_atlas,
#         ) = compare_harvester_yield_2harvesters(
#             parts1=parts,
#             members1=members,
#             parts2=parts/2,
#             members2=members*0.5,
#             # members2=members,
#             atlas_parts=atlas_parts,
#             debug=False
#         )

#         x_boost_h1.append(boost_h1)
#         x_boost_h2.append(boost_h2)
#         x_boost_atlas.append(boost_atlas)

#         x_mine_pct_share_h1.append(mine_pct_share_h1)
#         x_mine_pct_share_h2.append(mine_pct_share_h2)
#         x_mine_pct_share_atlas.append(mine_pct_share_atlas)

#         x_user_pct_share_h1.append(user_pct_share_h1)
#         x_user_pct_share_h2.append(user_pct_share_h2)
#         x_user_pct_share_atlas.append(user_pct_share_atlas)


#     boost_h1 = harvester_boosts[0]
#     mine_pct_share_h1 = mine_pct_shares[0]
#     user_pct_share_h1 = user_pct_shares[0]

#     x_boost_h1.append(boost_h1)
#     x_boost_atlas.append(boost_atlas)
#     x_mine_pct_share_h1.append(mine_pct_share_h1)
#     x_mine_pct_share_atlas.append(mine_pct_share_atlas)
#     x_user_pct_share_atlas.append(user_pct_share_atlas)
#     x_user_pct_share_h1.append(user_pct_share_h1)




def draw_atlas_harvest_comparison_1(i):

    day = i * 2 # each i is 2 days
    days.append(day)

    parts = _x_parts[day]
    legions = _x_legions[day]

    harvesters = [
        {
            'parts': parts,
            'legions': legions,
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

    x_boost_h1.append(boost_h1)
    x_boost_atlas.append(boost_atlas)
    x_mine_pct_share_h1.append(mine_pct_share_h1)
    x_mine_pct_share_atlas.append(mine_pct_share_atlas)
    x_user_pct_share_atlas.append(user_pct_share_atlas)
    x_user_pct_share_h1.append(user_pct_share_h1)


    #### Plot 1
    ax1.clear()
    # ax1.plot(days, y_boost_h1, label="H1 boost ranges from 1x to {:.1f}x max".format(x_boost_h1[-1]))
    ax1.plot(days, y_boost_h1, label="H1 boost ranges from 1x to {:.1f}x max".format(3), color='royalblue')
    # ax1.plot([], label="Atlas is {}x boost by default (configurable)".format(ATLAS_MINE_BONUS), color='red')
    ax1.set(xlabel='(parts, legions)', ylabel='Boost Multiplier')
    # ax1.set_xticks([0, 100, 200, 300, 400, 500])
    # ax1.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=7)
    ax1.set_title('Harvest Boost | {} parts | {} legions'.format(parts, legions), size=9)
    ax1.grid(color='black', alpha=0.1)

    #### Plot 2
    ax2.clear()
    ax2.plot(x_mine_pct_share_h1, label="H1 Share", color='royalblue')
    ax2.plot(x_mine_pct_share_atlas, label="Atlas Share", color='red')
    ax2.set(xlabel='Boost (x)', ylabel='% share of emissions')
    ## plot 2 x-ticks
    # boost_xticks = ["{:.1f}x".format(b) for b in [x_boost_h1[0], x_boost_h1[100], x_boost_h1[200], x_boost_h1[300], x_boost_h1[400], x_boost_h1[500]]]
    # boost_xticks = ["{:.1f}x".format(b) for b in [1,1.5,2,2.5,3,3.5]]
    # ax2.set_xticks([0, 100, 200, 300, 400, 500])
    # ax2.set_xticklabels(boost_xticks, fontsize=7)
    # plot 2 y-ticks
    yticks_pct = [0, 0.2, 0.4, 0.6, 0.8, 1]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax2.set_yticks(yticks_pct)
    ax2.set_yticklabels(yticks_label, fontsize=7)
    ax2.set_title('Share of emissions between Mines', size=9)
    ax2.grid(color='black', alpha=0.1)

    #### Plot 3
    ax3.clear()
    ax3.plot(x_user_pct_share_h1, label='$1m in H1', color='royalblue')
    ax3.plot(x_user_pct_share_atlas, label='$1m in Atlas', color='red')
    # # plot 3 x-ticks
    # ax3.set_xticks([0, 100, 200, 300, 400, 500])
    # ax3.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=8)
    # ax3.set(xlabel='Boost (x)', ylabel='% share of emissions')
    # ax3.set_xticklabels(boost_xticks, fontsize=7)
    # plot 3 y-ticks
    yticks_pct = [0, 0.01, 0.02, 0.03, 0.04, 0.05]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax3.set_yticks(yticks_pct)
    ax3.set_yticklabels(yticks_label, fontsize=7)
    ax3.set_title("User with 1m: their share of total emission in different Mines", size=9)
    ax3.grid(color='black', alpha=0.1)

    ax1.legend()
    ax2.legend()
    ax3.legend()




def run_harvester_split_simulation_1():

    fig.suptitle('Emission Splits: Atlas vs. 1 Harvester')
    fig.set_size_inches(12, 8)

    ani = FuncAnimation(fig, draw_atlas_harvest_comparison_1, frames=FRAMES, interval=1, repeat=False)

    plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.2)
    plt.legend()
    plt.show()


