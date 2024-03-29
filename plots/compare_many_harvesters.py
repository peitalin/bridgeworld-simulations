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
# and more harvesters will come online (~9 in total)
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
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    'atlas': [],
}

y_emissions_pct_shares = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    'atlas': [],
}

y_user_pct_shares = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    'atlas': [],
}

y_user_magic_yield = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
    'atlas': [],
}


harvester_linestyle = [
    '--',
    ':',
    ':',
    ':',
    ':',
    ':',
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
    'violet',
    'slategrey',
    'slategrey',
    'slategrey',
    'slategrey',
    'slategrey',
]

brown = '#AC8F59'
offwhite = '#E7E8E9'
grey = '#a6a8ab'
gold = '#a48955'
darkblue = '#0e171b'
lightblue = '#182329'



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



active_from_day = {
    ## Launch with 2 harvesters, then 1 every 20 days after
    'h1': 30,
    'h2': 30,
    'h3': 50,
    'h4': 70,
    'h5': 90,
    'h6': 110,
    'h7': 130,
    'h8': 130,
    'h9': 130,
    'h10': 130,
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
harvester_factory.create_harvester(id=6)
harvester_factory.create_harvester(id=7)
harvester_factory.create_harvester(id=8)
harvester_factory.create_harvester(id=9)


# # print("harvester_factory['harvesters'][0]", harvester_factory['harvesters'][0])
# ##### 5x extractors for harvester 0
# harvester_factory['harvesters'][0].set_extractors(extractors=['large_extractor']*MAX_EXTRACTORS)
# harvester_factory['harvesters'][1].set_extractors(extractors=['large_extractor']*MAX_EXTRACTORS)
# harvester_factory['harvesters'][2].set_extractors(extractors=['large_extractor']*MAX_EXTRACTORS)
# harvester_factory['harvesters'][3].set_extractors(extractors=['large_extractor']*MAX_EXTRACTORS)
# harvester_factory['harvesters'][4].set_extractors(extractors=['large_extractor']*MAX_EXTRACTORS)
# harvester_factory['harvesters'][5].set_extractors(extractors=['large_extractor']*MAX_EXTRACTORS)
# harvester_factory['harvesters'][6].set_extractors(extractors=['large_extractor']*MAX_EXTRACTORS)

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
    h7 = all_harvesters[6]
    h8 = all_harvesters[7]
    h9 = all_harvesters[8]


    if day < active_from_day['h1']:
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER
    # elif active_from_day['h1'] <= day < active_from_day['h2']:
    #     h1.activate()
    #     h1.stake_parts(parts_to_increment)
    #     h1.stake_legions(legions_to_increment)
    #     expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER
    elif active_from_day['h2'] <= day < active_from_day['h3']:
        [h.activate() for h in[h1, h2]]
        [h.stake_parts(parts_to_increment) for h in [h1,h2]]
        [h.stake_legions(legions_to_increment) for h in [h1,h2]]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*2

    elif active_from_day['h3'] <= day < active_from_day['h4']:
        [h.activate() for h in[h1, h2, h3]]
        [h.stake_parts(parts_to_increment) for h in [h1, h2, h3]]
        [h.stake_legions(legions_to_increment) for h in [h1, h2, h3]]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*3

    elif active_from_day['h4'] <= day < active_from_day['h5']:
        [h.activate() for h in[h1, h2, h3, h4]]
        [h.stake_parts(parts_to_increment) for h in [h1, h2, h3, h4]]
        [h.stake_legions(legions_to_increment) for h in [h1, h2, h3, h4]]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*4

    elif active_from_day['h5'] <= day < active_from_day['h6']:
        [h.activate() for h in[h1, h2, h3, h4, h5]]
        [h.stake_parts(parts_to_increment) for h in [h1, h2, h3, h4, h5]]
        [h.stake_legions(legions_to_increment) for h in [h1, h2, h3, h4, h5]]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*5
    elif active_from_day['h6'] <= day < active_from_day['h7']:
        [h.activate() for h in[h1, h2, h3, h4, h5, h6]]
        [h.stake_parts(parts_to_increment) for h in [h1, h2, h3, h4, h5, h6]]
        [h.stake_legions(legions_to_increment) for h in [h1, h2, h3, h4, h5, h6]]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*6
    else:
        [h.activate() for h in[h1, h2, h3, h4, h5, h6, h7, h8, h9]]
        [h.stake_parts(parts_to_increment) for h in [h1, h2, h3, h4, h5, h6, h7, h8, h9]]
        [h.stake_legions(legions_to_increment) for h in [h1, h2, h3, h4, h5, h6, h7, h8, h9]]
        # h6.activate()
        # h6.stake_parts(parts_to_increment)
        # h6.stake_legions(legions_to_increment)
        # last harvester comes out, but not as much AUM flows from Atlas
        # because it's all already locked.
        # 85mil locked
        # 45mil MAGIC locked for 1 year
        # https://twitter.com/bjornsamuel/status/1486957771979427844
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*7

    print('harvester_factory!!!!!', harvester_factory.harvesters)


    ( atlas_boost, harvester_boosts ) = middleman.calculate_harvester_boosts()

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

    for h in [h for h in all_harvesters if h.is_active]:

        active_from = round(active_from_day["h{}".format(h.id+1)] / 2)
        current_boost = h.getMiningBoost()
        current_emissions_pct_share = emissions_pct_shares[h.id]
        current_user_pct_share = user_pct_shares[h.id]
        current_user_magic_yield = MAGIC_EMISSIONS * current_user_pct_share / (NUM_MIL_USER_STAKES * 1_000_000)

        y_boosts[h.id].append(current_boost)
        y_emissions_pct_shares[h.id].append(current_emissions_pct_share['emission_share'])
        y_user_pct_shares[h.id].append(current_user_pct_share)
        y_user_magic_yield[h.id].append(current_user_magic_yield)


        if h.is_active:
            # ax1.plot(
            #     days[active_from:],
            #     y_boosts[h.id][active_from:],
            #     label="H{} boost {:.2f}x | {:.0f} parts {:.0f} legions".format(h.id + 1, current_boost, h.parts, h.legions),
            #     color=harvester_colors[h.id],
            # )

            ax2.plot(
                days[active_from:],
                y_emissions_pct_shares[h.id],
                label="Harvester {} {:.2f}x boost | Share {:.2%}".format(h.id + 1, current_boost, current_emissions_pct_share['emission_share']),
                color=harvester_colors[h.id],
                linestyle=harvester_linestyle[h.id],
            )

            ax3.plot(
                days[active_from:],
                # y_user_pct_shares[h.id][active_from:],
                y_user_magic_yield[h.id],
                label='Harvester {} 1/{}m: {:.2%}% APR MAGIC'.format(h.id + 1, AUM_CAP_HARVESTER, current_user_magic_yield),
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
        color='crimson',
        linestyle="--",
    )
    ax2.set(xlabel='', ylabel='% share of emissions')
    # plot 2 y-ticks
    yticks_pct = [0, 0.2, 0.4, 0.6, 0.8, 1]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax2.set_yticks(yticks_pct, color=gold)
    ax2.set_yticklabels(yticks_label, fontsize=7, color=gold)

    #### Plot 3 - Users MAGIC yield in the Mine (APR)
    ax3.plot(
        days,
        y_user_magic_yield['atlas'],
        label='Atlas: 1m/{:.0f}m: {:.2%}% APR MAGIC'.format(expected_atlas_aum, atlas_user_magic_yield),
        color='crimson',
        linestyle="--",
    )
    # plot 3 y-ticks
    yticks_pct = [0, 0.5, 1, 1.5, 2]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax3.set_yticks(yticks_pct, color=gold)
    ax3.set_yticklabels(yticks_label, fontsize=7, color=gold)

    # ax1.set_title('Harvester Boosts', size=10)
    ax2.set_title('Harvesters share of total emissions', size=10, color=gold)
    ax3.set_title("User with 1m MAGIC: APR in different mines", size=10, color=gold)

    ax2.set_ylabel('% share of emissions', color=gold)
    ax2.set_xlabel('day {}'.format(day), color=gold)

    ax3.set_ylabel('APR% in MAGIC', color=gold)
    ax3.set_xlabel('day {}'.format(day), color=gold)

    # ax1.grid(color='black', alpha=0.1)
    ax2.grid(color=gold, alpha=0.1)
    ax3.grid(color=gold, alpha=0.1)

    ax2.spines['bottom'].set_color(gold)
    ax2.spines['top'].set_color(gold)
    ax2.spines['left'].set_color(gold)
    ax2.spines['right'].set_color(gold)
    ax2.xaxis.label.set_color(gold)
    ax2.tick_params(axis='x', colors=gold)
    ax2.tick_params(axis='y', colors=gold)

    ax3.spines['bottom'].set_color(gold)
    ax3.spines['top'].set_color(gold)
    ax3.spines['left'].set_color(gold)
    ax3.spines['right'].set_color(gold)
    ax3.xaxis.label.set_color(gold)
    ax3.tick_params(axis='x', colors=gold)
    ax3.tick_params(axis='y', colors=gold)

    # ax1.legend(bbox_to_anchor=(1.48, 1), loc="upper right")
    ax2.legend(
        bbox_to_anchor=(1.47, 1),
        loc="lower center",
        labelcolor=grey,
        # edgecolor=lightblue,
        # facecolor=lightblue
        edgecolor=darkblue,
        facecolor=darkblue
    )

    ax3.legend(bbox_to_anchor=(1.47, 1), loc="lower center",
        labelcolor=grey,
        # edgecolor=lightblue,
        # facecolor=lightblue
        edgecolor=darkblue,
        facecolor=darkblue
    )







def run_harvester_split_simulation_9():

    global fig
    global ax1
    global ax2
    global ax3

    fig, (ax2, ax3) = plt.subplots(2, facecolor=darkblue)
    # fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Atlas {}x Boost vs Harvesters (no Extractors)'.format(ATLAS_MINE_BONUS),
        color=gold)
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
    ax2.set_facecolor(lightblue)
    ax3.set_facecolor(lightblue)

    plt.show()


