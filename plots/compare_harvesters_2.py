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

from harvester_boost_count import get_treasure_boost, parts_boost_harvester, legions_boost_harvester
from harvester_boost_count import extractors_boost_harvester, total_harvester_boost
from harvester_boost_count import calculate_avg_legion_rank



def compare_harvester_yield_2harvesters(parts1=20, members1=20, parts2=20, members2=20, atlas_parts=0, debug=True):
    """
        parts1, members1 for harvester 1
        parts2, members2 for harvester 2
    """

    EXPECTED_AUM_ATLAS = EXPECTED_ATLAS_AUM # 80mil in atlas mine, about 80% supply staked
    AUM_CAP_HARVESTER = 10 # 10mil cap in harvesters
    avg_legion_rank = 2

    # num_millions_user_stakes = 0.01 # 10k
    num_millions_user_stakes = 0.1 # 100k
    # num_millions_user_stakes = 1 # 1mil

    num_legions1 = members1*3 # 3 legions per user
    num_legions2 = members2*3

    if debug:
        print("\n============================================")
        print("Harvester_1 has:")
        print("{} parts, {} members, {} total legions\n".format(parts1, members1, members1*3))
        print("Harvester_2 has:")
        print("{} parts, {} members, {} total legions\n".format(parts2, members2, members2*3))

    boost_h1 = total_harvester_boost(num_parts=parts1, num_legions=num_legions1, extractors=[], avg_legion_rank=avg_legion_rank)
    boost_h2 = total_harvester_boost(num_parts=parts2, num_legions=num_legions2, extractors=[], avg_legion_rank=avg_legion_rank)
    # original atlas mine is treated as a harvester with uncapped AUM
    # it has 0 harvester parts to begin with, and can have up to 2000 staked legions to boost its mining (avg legion rank 1)
    boost_atlas = total_harvester_boost(num_parts=atlas_parts, num_legions=2000, extractors=[], avg_legion_rank=1, is_atlas=True) # 6x boost by default
    if debug:
        print("Atlas gets:\t{:.2f}x boost".format(boost_atlas))
        print("Harv_1 gets:\t{:.2f}x boost\n".format(boost_h1))

    # set harvester base points = 100
    points_atlas = boost_atlas * 100
    points_h1    = boost_h1 * 100
    points_h2    = boost_h2 * 100
    points_total = points_atlas + points_h1 + points_h2

    # Calculate percentage share of total emissions split between Atlas and Harvester 1 and Harvester 2
    emissions_pct_share_atlas = points_atlas / points_total
    emissions_pct_share_h1 = points_h1 / points_total
    emissions_pct_share_h2 = points_h2 / points_total
    if debug:
        print("Atlas gets:\t{:.2%} of emissions".format(emissions_pct_share_atlas))
        print("Harv_1 gets:\t{:.2%} of emissions\n".format(emissions_pct_share_h1))
        print("Harv_2 gets:\t{:.2%} of emissions\n".format(emissions_pct_share_h2))

    # a user's share of total emission, staying inside Atlas mine, vs. Harvester 1 and Harvester 2
    user_pct_share_atlas = num_millions_user_stakes/EXPECTED_AUM_ATLAS * emissions_pct_share_atlas
    user_pct_share_h1 = num_millions_user_stakes/10 * emissions_pct_share_h1
    user_pct_share_h2 = num_millions_user_stakes/10 * emissions_pct_share_h2

    if debug:
        print("For a whale with 1mil:")
        print("1m in Atlas with {AUM}m AUM gives you:\t 1/{AUM} * {MINE_PCT:.4f} = {USER_PCT:.2%} of emissions".format(
            AUM=EXPECTED_AUM_ATLAS,
            MINE_PCT=emissions_pct_share_atlas,
            USER_PCT=user_pct_share_atlas
        ))
        print("1m in Harv_1 with 10m AUM gives you:\t 1/{AUM_CAP} * {MINE_PCT:.4f} = {USER_PCT:.2%}".format(
            AUM_CAP=AUM_CAP_HARVESTER,
            MINE_PCT=emissions_pct_share_h1,
            USER_PCT=user_pct_share_h1
        ))
        print("1m in Harv_2 with 10m AUM gives you:\t 1/{AUM_CAP} * {MINE_PCT:.4f} = {USER_PCT:.2%}".format(
            AUM_CAP=AUM_CAP_HARVESTER,
            MINE_PCT=emissions_pct_share_h2,
            USER_PCT=user_pct_share_h2
        ))
        print("\nAn entrepreneurial whale can potentially get a {:.2%} / {:.2%}\n= {:.2f}x improvement in yield".format(
            user_pct_share_h1,
            user_pct_share_atlas,
            user_pct_share_h1 / user_pct_share_atlas
        ))
        print("for collecting {} harvester parts, a guild of {} users, {} legions".format(parts1, members1, members1*3))
        print("\nNote: assumes he can deploy his full 1m in the 10m cap harvester 1 alongside other guild members")
        print("he will get an even better yield initially before the 10m cap is reached")

    return (
        boost_h1,
        boost_h2,
        boost_atlas,
        emissions_pct_share_h1,
        emissions_pct_share_h2,
        emissions_pct_share_atlas,
        user_pct_share_h1,
        user_pct_share_h2,
        user_pct_share_atlas,
    )







## Atlas vs 2 Harvesters
def plot_atlas_harvest_comparison_2(atlas_parts=0):

    ## Array of x-axis data points
    x_boost_h1 = []
    x_boost_h2 = []
    x_boost_atlas = []

    x_emissions_pct_share_h1 = []
    x_emissions_pct_share_h2 = []
    x_emissions_pct_share_atlas = []

    x_user_pct_share_h1 = []
    x_user_pct_share_h2 = []
    x_user_pct_share_atlas = []


    num_obs = 501
    _x_parts = np.linspace(0, 500, num_obs) # 1 to 500 parts
    _x_members = np.linspace(0, 666.66, num_obs) # 1 to 666 users, 666.6 users * 3 legions = 2000 legions


    for parts,members in zip(_x_parts, _x_members):

        (
            boost_h1,
            boost_h2,
            boost_atlas,
            emissions_pct_share_h1,
            emissions_pct_share_h2,
            emissions_pct_share_atlas,
            user_pct_share_h1,
            user_pct_share_h2,
            user_pct_share_atlas,
        ) = compare_harvester_yield_2harvesters(
            parts1=parts,
            members1=members,
            parts2=parts/2,
            members2=members*0.5,
            # members2=members,
            atlas_parts=atlas_parts,
            debug=False
        )

        x_boost_h1.append(boost_h1)
        x_boost_h2.append(boost_h2)
        x_boost_atlas.append(boost_atlas)

        x_emissions_pct_share_h1.append(emissions_pct_share_h1)
        x_emissions_pct_share_h2.append(emissions_pct_share_h2)
        x_emissions_pct_share_atlas.append(emissions_pct_share_atlas)

        x_user_pct_share_h1.append(user_pct_share_h1)
        x_user_pct_share_h2.append(user_pct_share_h2)
        x_user_pct_share_atlas.append(user_pct_share_atlas)

        print("boost_h1: ", boost_h1)
        print("boost_h2: ", boost_h2)
        print("boost_atlas: ", boost_atlas)

        print("emissions_pct_share_h1: ", emissions_pct_share_h1)
        print("emissions_pct_share_h2: ", emissions_pct_share_h2)
        print("emissions_pct_share_atlas: ", emissions_pct_share_atlas)

        print("user_pct_share_h1: ", user_pct_share_h1)
        print("user_pct_share_h2: ", user_pct_share_h2)
        print("user_pct_share_atlas: ", user_pct_share_atlas)


    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Emission Splits: Atlas vs. 2 Harvesters')

    #### Plot 1
    ax1.plot(x_boost_h1, label="H1 boost ranges from 1x to ~3.3x boost")
    ax1.plot(x_boost_h2, label="H2 boost ranges from 1x to 2.6x boost")
    ax1.plot([], label="Atlas has {}x Atlas boost by default".format(ATLAS_MINE_BONUS), color='red')
    ax1.set(xlabel='(parts, legions)', ylabel='Boost Multiplier')
    ax1.set_xticks([0, 100, 200, 300, 400, 500])
    ax1.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=7)
    ax1.set_title('Harvest Boost', size=9)
    ax1.legend()
    ax1.grid(color='black', alpha=0.1)

    #### Plot 2
    ax2.plot(x_emissions_pct_share_h1, label="H1 Share")
    ax2.plot(x_emissions_pct_share_h2, label="H2 Share")
    ax2.plot(x_emissions_pct_share_atlas, label="Atlas Share", color='red')
    ax2.set(xlabel='Boost (x)', ylabel='% share of emissions')
    # plot 2 x-ticks
    boost_xticks = ["{:.1f}x".format(b) for b in [x_boost_h1[0], x_boost_h1[100], x_boost_h1[200], x_boost_h1[300], x_boost_h1[400], x_boost_h1[500]]]
    ax2.set_xticks([0, 100, 200, 300, 400, 500])
    ax2.set_xticklabels(boost_xticks, fontsize=7)
    # plot 2 y-ticks
    yticks_pct = [0, 0.2, 0.4, 0.6, 0.8, 1]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax2.set_yticks(yticks_pct)
    ax2.set_yticklabels(yticks_label, fontsize=7)
    ax2.set_title('Share of emissions between Mines', size=9)
    ax2.legend()
    ax2.grid(color='black', alpha=0.1)

    #### Plot 3
    ax3.plot(x_user_pct_share_h1, label='$100k in H1')
    ax3.plot(x_user_pct_share_h2, label='$100k in H2')
    ax3.plot(x_user_pct_share_atlas, label='$100k in Atlas', color='red')
    # plot 3 x-ticks
    ax3.set_xticks([0, 100, 200, 300, 400, 500])
    ax3.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=8)
    ax3.set(xlabel='Boost (x)', ylabel='% share of emissions')
    ax3.set_xticklabels(boost_xticks, fontsize=7)
    # plot 3 y-ticks
    yticks_pct = [0, 0.0010, 0.0020, 0.0030, 0.0040, 0.0050]
    yticks_label = ["{:.2%}".format(b) for b in yticks_pct]
    ax3.set_yticks(yticks_pct)
    ax3.set_yticklabels(yticks_label, fontsize=7)
    ax3.set_title("User with $100k: their share of total emission in different Mines", size=9)
    ax3.legend()
    ax3.grid(color='black', alpha=0.1)

    plt.subplots_adjust(hspace=0.5)
    plt.show()


