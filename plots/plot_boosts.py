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
from parameters import MAX_MAP_HEIGHT, MAX_MAP_WIDTH
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS

from harvester_boost_count import get_treasure_boost, parts_boost_harvester, legions_boost_harvester
from harvester_boost_count import extractors_boost_harvester, total_harvester_boost
from harvester_boost_count import distance_boost_harvester, calculate_distance_from_atlas


################ Varying legion numbers, fixed parts
def graph_total_harvester_boost_varying_legions():

    x1_num_parts = np.linspace(0, MAX_HARVESTER_PARTS, MAX_HARVESTER_PARTS+1)
    x2_num_legions = np.linspace(0, MAX_LEGIONS, MAX_HARVESTER_PARTS+1)

    total_boosted_max_hi_legion_rank = [total_harvester_boost(500, x2, []) for x2 in x2_num_legions]
    total_boosted_max = [total_harvester_boost(500, x2, []) for x2 in x2_num_legions]
    total_boosted_min = [total_harvester_boost(1, x2, [])   for x2 in x2_num_legions]

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

    x_parts = np.linspace(0, 500, 500+1)
    x_parts_2000 = np.linspace(0, MAX_HARVESTER_PARTS, MAX_HARVESTER_PARTS+1)

    parts_boosted = [
        parts_boost_harvester(num_parts=x, max_parts=500, boost_factor=1)
        for x in x_parts
    ]
    parts_boosted_2000 = [
        parts_boost_harvester(num_parts=x, max_parts=MAX_HARVESTER_PARTS, boost_factor=PARTS_BOOST_FACTOR)
        for x in x_parts_2000
    ]

    plt.plot(parts_boosted, label="max parts=500; max_boost=2x")
    plt.plot(parts_boosted_2000, label="max parts={}; max_boost={}x".format(MAX_HARVESTER_PARTS, PARTS_BOOST_FACTOR+1))
    plt.xlabel("number of parts")
    plt.ylabel("Boost multiplier")
    plt.title("Harvester Parts Boost")
    plt.grid(color='black', alpha=0.1)
    plt.legend()
    plt.show()
    # the marginal contribution of each peice of harvester part:
    # marginal_contribution = np.diff(parts_boosted)
    # starts at 2, then works it way down to 0
    # basically the first few parts count for 2, then steadily/linearly approachs 0 as we approach the 500th part



def graph_distance_boost():

    nobs = 101
    ymax = MAX_MAP_HEIGHT/2
    xmax = MAX_MAP_WIDTH/2

    coords = [
        (x,y) for (x,y) in
        zip(np.linspace(-xmax, xmax, nobs), np.linspace(-ymax, ymax, nobs))
    ]

    distance = [
        calculate_distance_from_atlas({
            'x': x,
            'y': y,
            'z': 0
        })
        for (x,y) in coords
    ]

    distance_boosts = [
        distance_boost_harvester({
            'x': x,
            'y': y,
            'z': 0
        })
        for (x,y) in coords
    ]

    print(coords)
    print(distance)

    plt.plot(
        distance,
        distance_boosts,
        label="distance boost"
    )
    plt.xlabel("Distance", color=gold)
    plt.ylabel("Boost multiplier", color=gold)
    plt.title("Harvester Distance Boost", color=gold)
    plt.grid(color=gold, alpha=0.1)
    plt.legend()
    plt.show()






brown = '#AC8F59'
offwhite = '#E7E8E9'
grey = '#a6a8ab'
gold = '#a48955'
fadegold = '#4c4b3f'
darkblue = '#0e171b'
darkdarkblue = '#0c1519'
lightblue = '#182329'

plt.rcParams['grid.color'] = fadegold


nobs = 100
xx = np.linspace(0, MAX_HARVESTER_PARTS, nobs)
yy = np.linspace(0, MAX_LEGIONS, nobs)


@np.vectorize
def f2(x, y):
    return total_harvester_boost(x, y)

X, Y = np.meshgrid(xx, yy)
Z = f2(X, Y)

fig = plt.figure(facecolor=darkdarkblue)
ax = plt.axes(projection='3d')

ax.set_xlabel('#Parts', color=gold)
ax.set_ylabel('#Legions', color=gold)
ax.set_zlabel('Harvester Boost', color=gold)
ax.set_facecolor(darkdarkblue)

ax.plot_surface(X, Y, Z,
    rstride=1, cstride=1,
    # linewidth=2,
    # cmap='binary',
    cmap='copper',
    edgecolors='none'
)

# ax.contour3D(X, Y, Z, 100, cmap='binary')

ax.set_title('Harvester Boosts', color=gold);

ax.spines['bottom'].set_color(gold)
ax.spines['top'].set_color(gold)
ax.spines['left'].set_color(gold)
ax.spines['right'].set_color(gold)
ax.xaxis.label.set_color(gold)
ax.tick_params(axis='x', colors=gold)
ax.tick_params(axis='y', colors=gold)
ax.tick_params(axis='z', colors=gold)

ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

xticks_pct = [100, 200, 300, 400, 500]
xticks_label = [100, 200, 300, 400, 500]

# yticks_pct = [0, 500, 1000, 1500, 2000, 2500]
# yticks_label = [0, 500, 1000, 1500, 2000, 2500]

yticks_pct = [0, 200, 400, 600, 800, 1000]
yticks_label = [0, 200, 400, 600, 800, 1000]

zticks_pct = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]
zticks_label = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]

ax.set_xticks(xticks_pct, color=gold)
ax.set_xticklabels(xticks_label, fontsize=7, color=gold)
ax.set_yticks(yticks_pct, color=gold)
ax.set_yticklabels(yticks_label, fontsize=7, color=gold)
ax.set_zticks(zticks_pct, color=gold)
ax.set_zticklabels(zticks_label, fontsize=7, color=gold)




for axis in [ax.w_xaxis, ax.w_yaxis, ax.w_zaxis]:
    axis.line.set_color(fadegold)

# ax.view_init(20, 35)
plt.show()