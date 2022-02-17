
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from parameters import MAX_MAP_HEIGHT, MAX_MAP_WIDTH
from harvester_boost_count import distance_boost_harvester, calculate_distance_from_atlas






# initialize variables, overwritten on 1st pass of simulation
ax1 = 1
ax2 = 1
im = 1
# params
nobs = 100
ymax = MAX_MAP_HEIGHT/2
xmax = MAX_MAP_WIDTH/2

coords1 = [
    (x,y) for (x,y) in
    zip(np.linspace(-50, -25, 25), np.linspace(-50, -25, 25))
]
coords2 = [
    (x,y) for (x,y) in
    zip(np.linspace(-25, 0, 25), np.linspace(-25, -25, 25))
]
coords3 = [
    (x,y) for (x,y) in
    zip(np.linspace(0, 0, 25), np.linspace(-25, 0, 25))
]
coords4 = [
    (x,y) for (x,y) in
    zip(np.linspace(0, 50, 25), np.linspace(0, 50, 25))
]
coords = coords1 + coords2 + coords3 + coords4


max_distance = calculate_distance_from_atlas({
    'x': MAX_MAP_WIDTH/2,
    'y': MAX_MAP_HEIGHT/2,
    'z': 0
})

distance_array = [
    calculate_distance_from_atlas({
        'x': x,
        'y': y,
        'z': 0
    })
    for (x,y) in coords
]
distance_boost_array = [
    distance_boost_harvester({
        'x': x,
        'y': y,
        'z': 0
    })
    for (x,y) in coords
]
prob_smol_attack_array = [
    distance/max_distance / 2
    for distance in distance_array
]

harvester_path_x = []
harvester_path_y = []


FRAMES = 100


def func_animate(i):

    global distance_array
    global distance_boost_array
    global prob_smol_attack_array

    coord = coords[i]
    x = coord[0]
    y = coord[1]

    harvester_path_x.append(x)
    harvester_path_y.append(y)

    distance = distance_array[i]
    distance_boost = distance_boost_array[i]
    prob_smol_attack = prob_smol_attack_array[i]

    # distance = calculate_distance_from_atlas({
    #     'x': x,
    #     'y': y,
    #     'z': 0
    # })

    # distance_boost = distance_boost_harvester({
    #     'x': x,
    #     'y': y,
    #     'z': 0
    # })
    # prob_smol_attack = distance/max_distance / 2

    # distance_array.append(distance)
    # distance_boost_array.append(distance_boost)
    # prob_smol_attack_array.append(prob_smol_attack)

    # distance boost plots
    ax1.clear()
    ax1.plot(
        distance_array,
        distance_boost_array,
        label="Distance Boost {:.2f}x".format(distance_boost),
        color='royalblue'
    )
    ax1.plot(
        distance_array,
        prob_smol_attack_array,
        label="Probility of smol attack {:.1f}%".format(prob_smol_attack*100),
        color='purple',
        linestyle=":",
    )
    ax1.scatter([ distance ], [ distance_boost ], color='royalblue', marker='o')
    ax1.scatter([ distance ], [ prob_smol_attack ], color='purple', marker='*')

    ax1.set_xlim([-100, 100])
    ax1.set_ylim([0,3])
    ax1.title.set_text("Distance Boost vs. Probability of Smol Attack")
    ax1.grid(color='black', alpha=0.15)

    # harvester coordinates
    ax2.clear()
    ax2.scatter(
        [x], [y],
        label="Harvester Location ({:.0f}, {:.0f})".format(x, y),
        color='royalblue',
        marker='*',
        s=80,
    )
    ax2.scatter(
        [0], [0],
        label="Atlas Location ({}, {})".format(0, 0),
        color='red',
        marker='^',
        s=100,
    )
    ax2.plot(
        harvester_path_x,
        harvester_path_y,
        color='royalblue',
        linestyle=":",
    )

    # Major ticks every 10, minor ticks every 1
    major_ticks = np.arange(-50, 50, 10)
    minor_ticks = np.arange(-50, 50, 1)

    ax2.set_xticks(major_ticks)
    ax2.set_xticks(minor_ticks, minor=True)
    ax2.set_yticks(major_ticks)
    ax2.set_yticks(minor_ticks, minor=True)

    ax2.set_xlim([-50, 50])
    ax2.set_ylim([-50, 50])
    ax2.title.set_text("Harvester Coordinates: ({:.0f}, {:.0f})".format(x, y))

    ax2.grid(which='minor', alpha=0.2)
    ax2.grid(which='major', alpha=0.4)


    ax1.legend()
    ax2.legend()

    # slows down aniimation
    extent = (-50, 50, -50, 50)
    implot = ax2.imshow(
        im,
        origin='upper',
        alpha=0.8,
        extent=extent,
    )



def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return



def run_distance_boost_simulation():

    global ax1
    global ax2
    global fig
    global im

    fig, (ax1, ax2) = plt.subplots(1,2, gridspec_kw={'width_ratios': [1, 1]})
    image_name = 'plots/map.jpg'
    im = plt.imread(image_name)

    fig.suptitle('Harvester Location, Distance Boosts vs. Probability of Smol Attack')
    fig.set_size_inches(12, 6)

    ani = FuncAnimation(
        fig,
        func_animate,
        frames=FRAMES,
        interval=10,
        repeat=False,
        init_func=init_plot,
    )

    # plt.subplots_adjust(left=0.08, right=0.7, top=0.9, bottom=0.1, hspace=0.3)

    plt.show()










