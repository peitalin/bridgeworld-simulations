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
    plt.xlabel("Distance")
    plt.ylabel("Boost multiplier")
    plt.title("Harvester Distance Boost")
    plt.grid(color='black', alpha=0.1)
    plt.legend()
    plt.show()







nobs = 100
xx = np.linspace(0, MAX_HARVESTER_PARTS, nobs)
yy = np.linspace(0, MAX_LEGIONS, nobs)


@np.vectorize
def f2(x, y):
    return total_harvester_boost(x, y)

X, Y = np.meshgrid(xx, yy)
Z = f2(X, Y)

fig = plt.figure()
ax = plt.axes(projection='3d')

ax.set_xlabel('#Parts')
ax.set_ylabel('#Legions')
ax.set_zlabel('Harvester Boost');

ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                cmap='binary', edgecolor='none')

# ax.contour3D(X, Y, Z, 100, cmap='binary')

ax.set_title('Harvester Boosts');

# ax.view_init(20, 35)
plt.show()