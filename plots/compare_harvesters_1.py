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

from harvester_boosts import get_treasure_boost, parts_boost_harvester, legions_boost_harvester
from harvester_boosts import extractors_boost_harvester, total_harvester_boost, user_boost_inside_harvester
from harvester_boosts import calculate_avg_legion_rank

from harvester_emission_splits import calculate_harvester_splits



#################################
####### COMPARISON TO ATLAS MINE
#################################

# In the beginning there will only be 1 aux harvester, with low parts and legions
# over time, the harvester will get larger boosts (more parts + legions)
# and more harvesters will come online (6 in total)
# harvesters will launch roughly every month


# fig, (ax1, ax2, ax3) = plt.subplots(3)
fig, (ax2, ax3) = plt.subplots(2)

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

y_mine_pct_shares = {
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


harvester_colors = [
    'mediumorchid',
    'royalblue',
    'dodgerblue',
    'mediumseagreen',
    'gold',
    'darkorange',
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


class Harvester:

    def __init__(
        self,
        id,
        parts=0,
        legions=0,
        avg_legion_rank=2,
        extractors=[],
        is_atlas=False,
        is_active=False,
        active_from=0,
    ):
        self.id = id
        self.parts = 1
        self.legions = 1
        self.avg_legion_rank = avg_legion_rank
        self.extractors = extractors
        self.is_atlas = is_atlas
        self.is_active = False # dormant by default
        self.active_from = active_from # day which harvester comes online

    def __repr__(self):
        return """
        Harvester:\t{id}
        Parts:\t{parts}
        Legions:\t{legions}
        Avg Legion Rank:\t{avg_legion_rank}
        Extractors:\t{extractors}
        """.format(
            id=self.id,
            parts=self.parts,
            legions=self.legions,
            avg_legion_rank=self.avg_legion_rank,
            extractors=self.extractors,
        )

    def __getitem__(self, item):
        if item == 'id':
            return self.id
        if item == 'parts':
            return self.parts
        if item == 'legions':
            return self.legions
        if item == 'avg_legion_rank':
            return self.avg_legion_rank
        if item == 'extractors':
            return self.extractors

    def activate(self):
        self.is_active = True

    def increment_parts(self, parts=1):
        if self.parts + parts <= 500:
            self.parts += parts
        else:
            self.parts = MAX_HARVESTER_PARTS

    def increment_legions(self, legions=1):
        if self.legions + legions <= 2000:
            self.legions += legions
        else:
            self.legions = MAX_LEGIONS

    def set_avg_legion_rank(self, avg_legion_rank):
        if avg_legion_rank <= 5:
            self.avg_legion_rank = avg_legion_rank

    def add_extractor(self, extractor):
        self.extractors.append(extractor)


all_harvesters = [
    Harvester(id=0, parts=0, legions=0, active_from=0),
    Harvester(id=1, parts=0, legions=0, active_from=30),
    Harvester(id=2, parts=0, legions=0, active_from=60),
    Harvester(id=3, parts=0, legions=0, active_from=90),
    Harvester(id=4, parts=0, legions=0, active_from=120),
    Harvester(id=5, parts=0, legions=0, active_from=150),
]


def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return



def draw_atlas_harvest_comparison(i):

    day = i * 2 # each i-frame is 2 days
    days.append(day)

    # magic emissions for the first year
    magic_emissions = MAGIC_EMISSIONS_BY_YEAR[1]

    global all_harvesters

    # parts = _x_parts[day]
    # members = _x_members[day]
    # legions = _x_legions[day]

    # 16hrs to make 2 parts, 3 parts every 2 days
    parts_to_increment = 3 * 3

    legions_to_increment = 20 * 3
    # # lets assume 20 new users (60 legions) every 2 days
    # if day < 10:
    #     legions_to_increment = 20 * 3
    # elif
    #     legions_to_increment = 2 * 3

    h1 = all_harvesters[0]
    h2 = all_harvesters[1]
    h3 = all_harvesters[2]
    h4 = all_harvesters[3]
    h5 = all_harvesters[4]
    h6 = all_harvesters[5]

    if day < 30:
        h1.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        harvesters = [ h1, h2, h3, h4, h5, h6 ]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER
    elif day < 60:
        h1.activate()
        h2.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        h2.increment_parts(parts_to_increment)
        h2.increment_legions(legions_to_increment)
        harvesters = [ h1, h2, h3, h4, h5, h6 ]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*2
    elif day < 90:
        h1.activate()
        h2.activate()
        h3.activate()
        h1.increment_parts(parts_to_increment)
        h1.increment_legions(legions_to_increment)
        h2.increment_parts(parts_to_increment)
        h2.increment_legions(legions_to_increment)
        h3.increment_parts(parts_to_increment)
        h3.increment_legions(legions_to_increment)
        harvesters = [ h1, h2, h3, h4, h5, h6 ]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*3
    elif day < 120:
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
        harvesters = [ h1, h2, h3, h4, h5, h6 ]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*4
    elif day < 150:
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
        harvesters = [ h1, h2, h3, h4, h5, h6 ]
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*5
    else:
        h1.activate()
        h2.activate()
        h3.activate()
        h4.activate()
        h5.activate()
        h6.activate()
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
        h6.increment_parts(parts_to_increment)
        h6.increment_legions(legions_to_increment)
        harvesters = [ h1, h2, h3, h4, h5, h6 ]
        # last harvester comes out, but not as much AUM flows from Atlas
        # because it's all already locked
        expected_atlas_aum = EXPECTED_ATLAS_AUM - AUM_CAP_HARVESTER*5.5

    (
        boost_atlas,
        mine_pct_share_atlas,
        user_pct_share_atlas,
        harvester_boosts,
        mine_pct_shares,
        user_pct_shares,
    ) = calculate_harvester_splits(
        harvesters=harvesters,
        expected_atlas_aum=expected_atlas_aum,
        debug=False,
        num_mil_user_stakes=NUM_MIL_USER_STAKES
    )

    # clear plots to redraw
    # ax1.clear()
    ax2.clear()
    ax3.clear()

    y_boosts['atlas'].append(boost_atlas)
    y_mine_pct_shares['atlas'].append(mine_pct_share_atlas)
    y_user_pct_shares['atlas'].append(user_pct_share_atlas)

    atlas_user_magic_yield = magic_emissions * user_pct_share_atlas / (NUM_MIL_USER_STAKES * 1_000_000)
    y_user_magic_yield['atlas'].append(atlas_user_magic_yield)

    #### Plot 1 - Boosts
    for h in harvesters:

        hid = h.id
        active_from = round(h.active_from/2) # each i is 2 days
        current_boost = harvester_boosts[hid]
        current_mine_pct_share = mine_pct_shares[hid]
        current_user_pct_share = user_pct_shares[hid]
        current_user_magic_yield = magic_emissions * current_user_pct_share / (NUM_MIL_USER_STAKES * 1_000_000)

        y_boosts[hid].append(current_boost)
        y_mine_pct_shares[hid].append(current_mine_pct_share)
        y_user_pct_shares[hid].append(current_user_pct_share)
        y_user_magic_yield[hid].append(current_user_magic_yield)


        if h.is_active:
            # ax1.plot(
            #     days[active_from:],
            #     y_boosts[hid][active_from:],
            #     label="H{} boost {:.2f}x | {:.0f} parts {:.0f} legions".format(h.id, current_boost, h.parts, h.legions),
            #     color=harvester_colors[h.id],
            # )

            ax2.plot(
                days[active_from:],
                y_mine_pct_shares[hid][active_from:],
                label="H{} {:.2f}x boost | Share {:.2%}".format(h.id, current_boost, current_mine_pct_share),
                color=harvester_colors[h.id],
            )

            ax3.plot(
                days[active_from:],
                # y_user_pct_shares[hid][active_from:],
                y_user_magic_yield[hid][active_from:],
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
        y_mine_pct_shares['atlas'],
        label="Atlas {:.2f}x boost | Share {:.2%}".format(ATLAS_MINE_BONUS, mine_pct_share_atlas),
        color='red'
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
        color='red'
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
    ax3.set(xlabel='days | day {}'.format(day), ylabel='% share of emissions')

    # ax1.grid(color='black', alpha=0.1)
    ax2.grid(color='black', alpha=0.1)
    ax3.grid(color='black', alpha=0.1)

    # ax1.legend(bbox_to_anchor=(1.48, 1), loc="upper right")
    ax2.legend(bbox_to_anchor=(1.4, 1), loc="upper right")
    ax3.legend(bbox_to_anchor=(1.47, 1), loc="upper right")




def run_harvester_split_simulation_1():

    fig.suptitle('Emission Splits: Atlas vs. 6 Harvesters over time')
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


