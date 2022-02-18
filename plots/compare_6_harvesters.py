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
from parameters import AUM_CAP_HARVESTER
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS
from parameters import MAGIC_EMISSIONS_BY_YEAR

from harvester_boost_count import get_treasure_boost, parts_boost_harvester, legions_boost_harvester
from harvester_boost_count import extractors_boost_harvester, total_harvester_boost
from harvester_boost_count import calculate_avg_legion_rank

## prototype contracts
from master_of_coin import MasterOfCoin
from harvester_factory import Harvester, HarvesterFactory
from harvester_middleman import UtilizationMiddleman





#################################
####### COMPARISON TO ATLAS MINE
#################################

# In the beginning there will only be 1 aux harvester, with low parts and legions
# over time, the harvester will get larger boosts (more parts + legions)
# and more harvesters will come online (6 in total)
# harvesters will launch roughly every month

# initialize plot variables, overwritten on 1st pass of simulation
ax1 = 1
ax2 = 1
ax3 = 1

## Array of y-axis data points
y_boosts = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    'atlas': [],
}

y_emissions_pct_shares = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    'atlas': [],
}

y_user_pct_shares = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    'atlas': [],
}

y_user_magic_yield = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    'atlas': [],
}


harvester_linestyle = [
    '--',
    ':',
    ':',
    ':',
    ':',
    ':',
]
harvester_colors = [
    'mediumorchid',
    'royalblue',
    'mediumseagreen',
    'gold',
    'darkorange',
    'black',
]

## x-axis is days
days = []

# each frame is 2 days: 250 frames, 500 days
FRAMES = 250
num_obs = 501
_x_parts = np.linspace(0, MAX_HARVESTER_PARTS, num_obs) # 1 to 500 parts
_x_members = np.linspace(0, 100, num_obs) # 100 members in a 10mil harvester
_x_legions = np.linspace(0, MAX_LEGIONS, num_obs) # 1 to 2000 legions
# user stakes 1 mil MAGIC in mines
NUM_MIL_USER_STAKES = 1



extractors = [
    'large_extractor',
    'large_extractor',
    'large_extractor',
    'large_extractor',
    'large_extractor',
]

active_from_day = {
    ## Launch with 2 harvesters, then 1 every 20 days after
    'h1': 30,
    'h2': 30,
    'h3': 50,
    'h4': 70,
    'h5': 90,
    'h6': 110,
}


master_of_coin = MasterOfCoin()
harvester_factory = HarvesterFactory()
middleman = UtilizationMiddleman(
    master_of_coin=master_of_coin,
    harvester_factory=harvester_factory,
)

harvester_factory.create_harvester(id=0)
harvester_factory.create_harvester(id=1)
harvester_factory.create_harvester(id=2)
harvester_factory.create_harvester(id=3)
harvester_factory.create_harvester(id=4)
harvester_factory.create_harvester(id=5)


def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return


def draw_atlas_harvest_comparison(i):

    day = i * 2 # each i-frame is 2 days
    days.append(day)

    # magic emissions for the first year
    MAGIC_EMISSIONS = MAGIC_EMISSIONS_BY_YEAR[1]

    # global all_harvesters
    global harvester_factory
    global active_from

    # parts = _x_parts[day]
    # members = _x_members[day]
    # legions = _x_legions[day]

    # 36hrs to make a part
    # lets say 100 parts are made every 2 days between ~50 users
    parts_to_increment = 100

    # assume 200 legions are added every 2 days
    legions_to_increment = 200

    all_harvesters = harvester_factory['harvesters']
    atlas = harvester_factory['atlas_mine']
    h1 = all_harvesters[0]
    h2 = all_harvesters[1]
    h3 = all_harvesters[2]
    h4 = all_harvesters[3]
    h5 = all_harvesters[4]
    h6 = all_harvesters[5]

    # harvesters = [ h1, h2, h3, h4, h5 ]

    if day < active_from_day['h1']:
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER
    # elif active_from_day['h1'] <= day < active_from_day['h2']:
    #     h1.activate()
    #     h1.increment_parts(parts_to_increment)
    #     h1.increment_legions(legions_to_increment)
    #     expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER
    elif active_from_day['h2'] <= day < active_from_day['h3']:
        h1.activate()
        h2.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        h2.increment_parts(parts_to_increment)
        h2.increment_legions(legions_to_increment)
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*2
    elif active_from_day['h3'] <= day < active_from_day['h4']:
        h1.activate()
        h2.activate()
        h3.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        h2.increment_parts(parts_to_increment)
        h2.increment_legions(legions_to_increment)
        h3.increment_parts(parts_to_increment)
        h3.increment_legions(legions_to_increment)
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*3
    elif active_from_day['h4'] <= day < active_from_day['h5']:
        h1.activate()
        h2.activate()
        h3.activate()
        h4.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        h2.increment_parts(parts_to_increment)
        h2.increment_legions(legions_to_increment)
        h3.increment_parts(parts_to_increment)
        h3.increment_legions(legions_to_increment)
        h4.increment_parts(parts_to_increment)
        h4.increment_legions(legions_to_increment)
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*3.5
    elif active_from_day['h5'] <= day < active_from_day['h6']:
        h1.activate()
        h2.activate()
        h3.activate()
        h4.activate()
        h5.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        h2.increment_parts(parts_to_increment)
        h2.increment_legions(legions_to_increment)
        h3.increment_parts(parts_to_increment)
        h3.increment_legions(legions_to_increment)
        h4.increment_parts(parts_to_increment)
        h4.increment_legions(legions_to_increment)
        h5.increment_parts(parts_to_increment)
        h5.increment_legions(legions_to_increment)
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*4
    else:
        h1.activate()
        h2.activate()
        h3.activate()
        h4.activate()
        h5.activate()
        # h6.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        h2.increment_parts(parts_to_increment)
        h2.increment_legions(legions_to_increment)
        h3.increment_parts(parts_to_increment)
        h3.increment_legions(legions_to_increment)
        h4.increment_parts(parts_to_increment)
        h4.increment_legions(legions_to_increment)
        h5.increment_parts(parts_to_increment)
        h5.increment_legions(legions_to_increment)
        # h6.increment_parts(parts_to_increment)
        # h6.increment_legions(legions_to_increment)
        # last harvester comes out, but not as much AUM flows from Atlas
        # because it's all already locked.
        # 85mil locked
        # 45mil MAGIC locked for 1 year
        # https://twitter.com/bjornsamuel/status/1486957771979427844
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*4


    ( atlas_boost, harvester_boosts ) = middleman.recalculate_harvester_boosts()

    ( emissions_pct_share_atlas, emissions_pct_shares ) = middleman.recalculate_emission_shares()

    ( user_pct_share_atlas, user_pct_shares ) = middleman._calculate_user_pct_shares(
        expected_atlas_aum=expected_atlas_aum,
        num_mil_user_stakes=NUM_MIL_USER_STAKES
    )


    # clear plots to redraw
    # ax1.clear()
    ax2.clear()
    ax3.clear()

    y_boosts['atlas'].append(atlas_boost)
    y_emissions_pct_shares['atlas'].append(emissions_pct_share_atlas)
    y_user_pct_shares['atlas'].append(user_pct_share_atlas)

    atlas_user_magic_yield = MAGIC_EMISSIONS * user_pct_share_atlas / (NUM_MIL_USER_STAKES * 1_000_000)
    y_user_magic_yield['atlas'].append(atlas_user_magic_yield)

    #### Plot 1 - Boosts
    for h in all_harvesters:

        active_from = round(active_from_day["h{}".format(h.id+1)] / 2)
        current_boost = h.getMiningBoost()
        current_emissions_pct_share = emissions_pct_shares[h.id]
        current_user_pct_share = user_pct_shares[h.id]
        current_user_magic_yield = MAGIC_EMISSIONS * current_user_pct_share / (NUM_MIL_USER_STAKES * 1_000_000)

        y_boosts[h.id].append(current_boost)
        y_emissions_pct_shares[h.id].append(current_emissions_pct_share)
        y_user_pct_shares[h.id].append(current_user_pct_share)
        y_user_magic_yield[h.id].append(current_user_magic_yield)


        if h.is_active:
            # ax1.plot(
            #     days[active_from:],
            #     y_boosts[h.id][active_from:],
            #     label="H{} boost {:.2f}x | {:.0f} parts {:.0f} legions".format(h.id, current_boost, h.parts, h.legions),
            #     color=harvester_colors[h.id],
            # )

            ax2.plot(
                days[active_from:],
                y_emissions_pct_shares[h.id][active_from:],
                label="H{} {:.2f}x boost | Share {:.2%}".format(h.id, current_boost, current_emissions_pct_share),
                color=harvester_colors[h.id],
                linestyle=harvester_linestyle[h.id],
            )

            ax3.plot(
                days[active_from:],
                # y_user_pct_shares[h.id][active_from:],
                y_user_magic_yield[h.id][active_from:],
                label='H{} 1m/{}m: {:.2%}% APR in MAGIC'.format(h.id, AUM_CAP_HARVESTER, current_user_magic_yield),
                color=harvester_colors[h.id],
            )


    # ### Atlas Boosts
    # #### Plot 1 - Harvester Boosts
    # ax1.plot([], label="Atlas with {}x default boost (configurable)".format(ATLAS_MINE_BONUS), color='red')
    # ax1.set(xlabel='', ylabel='Boost Multiplier')

    #### Plot 2 - Harvester Emission Share
    ax2.plot(
        days,
        y_emissions_pct_shares['atlas'],
        label="Atlas {:.2f}x boost | Share {:.2%}".format(ATLAS_MINE_BONUS, emissions_pct_share_atlas),
        color='red',
        linestyle="--",
    )
    ax2.set(xlabel='', ylabel='% share of emissions')
    # plot 2 y-ticks
    yticks_pct = [0, 0.2, 0.4, 0.6, 0.8, 1]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax2.set_yticks(yticks_pct)
    ax2.set_yticklabels(yticks_label, fontsize=7)

    #### Plot 3 - Users MAGIC yield in the Mine (APR)
    ax3.plot(
        days,
        y_user_magic_yield['atlas'],
        label='Atlas: 1m/{:.0f}m: {:.2%}% APR in MAGIC'.format(expected_atlas_aum, atlas_user_magic_yield),
        color='red',
        linestyle="--",
    )
    # plot 3 y-ticks
    yticks_pct = [0, 0.5, 1, 1.5, 2, 2.5]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax3.set_yticks(yticks_pct)
    ax3.set_yticklabels(yticks_label, fontsize=7)

    # ax1.set_title('Harvester Boosts', size=10)
    ax2.set_title('Harvesters share of total emissions'.format(current_boost), size=10)
    ax3.set_title("User with 1m MAGIC: APR in different mines", size=10)

    ax2.set(xlabel='days | day {}'.format(day), ylabel='% share of emissions')
    ax3.set(xlabel='days | day {}'.format(day), ylabel='APR % in MAGIC')

    # ax1.grid(color='black', alpha=0.1)
    ax2.grid(color='black', alpha=0.1)
    ax3.grid(color='black', alpha=0.1)

    # ax1.legend(bbox_to_anchor=(1.48, 1), loc="upper right")
    ax2.legend(bbox_to_anchor=(1.4, 1), loc="upper right")
    ax3.legend(bbox_to_anchor=(1.47, 1), loc="upper right")







def run_harvester_split_simulation_6():

    global fig
    global ax1
    global ax2
    global ax3

    fig, (ax2, ax3) = plt.subplots(2)
    # fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Atlas {}x Boost (45m locked 12months) vs. 6 Harvesters'.format(ATLAS_MINE_BONUS))
    fig.set_size_inches(12, 9)

    ani = FuncAnimation(
        fig,
        draw_atlas_harvest_comparison,
        frames=FRAMES,
        interval=100,
        repeat=False,
        init_func=init_plot,
    )

    plt.subplots_adjust(left=0.08, right=0.7, top=0.9, bottom=0.1, hspace=0.3)

    plt.show()


