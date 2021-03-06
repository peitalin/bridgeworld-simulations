
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

from params import QUEST_TIMES, CRAFT_TIMES
from legion import Legion
from legion_populations import calculate_percentage_legion_questing
from legion_populations import LegionPopulations
from treasure_accounting import TreasureAccounting

#################################################
#################################################
##### Questing and Crafting Simulations
#################################################
#################################################

days = [] # x-axis is days
fig, (ax1, ax2, ax3) = plt.subplots(1,3, gridspec_kw={'width_ratios': [1,1,1]})
fig.set_size_inches(15, 8)

# Stores all treasure minted/broken balances and histories
treasureAccounting = TreasureAccounting()

NUM_LEGIONS_SUMMONING = 0
NUM_LEGIONS = 6000
ROLLING_MEAN_LAG = 3

legionPopulations = LegionPopulations(
    treasureAccounting,
    num_legions=NUM_LEGIONS,
    num_legions_summoning=NUM_LEGIONS_SUMMONING,
    rolling_mean_lag=ROLLING_MEAN_LAG,
    # number of days to average back T5 excess supply to decide when to switch from
    # questing to crafting
)


FRAMES = 800


def check_durations_divisible_in_simulation(hours_in_period):
    # Check that durations on questing and crafting are
    # less than 1 simulation period, otherwise you get fractional
    # quests/crafts and simulations round it to zero
    assert QUEST_TIMES['easy'] <= hours_in_period
    assert QUEST_TIMES['medium'] <= hours_in_period
    assert QUEST_TIMES['hard'] <= hours_in_period
    assert CRAFT_TIMES['easy'] <= hours_in_period
    assert CRAFT_TIMES['medium'] <= hours_in_period
    assert CRAFT_TIMES['hard'] <= hours_in_period



def func_animate(i):

    ## Every loop of i (period) is 3 days or 72 hrs
    ## Every loop of i (period) is 4 days or 96 hrs
    day = i * 4
    hours_in_period = 24 * 4

    global days
    days.append(day)

    check_durations_divisible_in_simulation(hours_in_period)

    # Every 7 days, add N new summoned legions
    # Because every i is two days, the first summon period will
    # land on day = 8, then 14, then 22, then 28
    # so need day % 7 == 1 or == 0
    if (day % 7 == 1) or (day % 7 == 0):
        legionPopulations.update_legion_populations(summoning_cycle_complete=True)
    else:
        legionPopulations.update_legion_populations(summoning_cycle_complete=False)

    pct_legions_questing_now = legionPopulations.pct_questing[-1]
    print("pct_legions_questing_now ", pct_legions_questing_now )


    for l1 in legionPopulations.legions_questing:
        if l1.quest_lvl >= 5:
            # hard quests take 16hrs, 48/16 = 3 times
            num_times_quest = int(hours_in_period / QUEST_TIMES['hard'])
            [l1.quest() for x in range(num_times_quest)]
        elif l1.quest_lvl >= 3:
            # medium quests take 12hrs, 48/12 = 4 times
            num_times_quest = int(hours_in_period / QUEST_TIMES['medium'])
            [l1.quest() for x in range(num_times_quest)]
        else:
            # easy quests take 8hrs, 48/8 = 6 times
            num_times_quest = int(hours_in_period / QUEST_TIMES['easy'])
            [l1.quest() for x in range(num_times_quest)]


    for l2 in legionPopulations.legions_crafting:
        if l2.craft_lvl >= 5:
            # hard craft take 48hrs, 48/48 = 1 times
            # how many times you can craft in 2 days
            num_times_craft = int(hours_in_period / CRAFT_TIMES['hard'])
            [l2.craft('hard') for x in range(num_times_craft)]

        elif l2.craft_lvl >= 3:
            # medium craft take 16hrs, 48/16 = 3 times
            # how many times you can craft in 2 days
            num_times_craft = int(hours_in_period / CRAFT_TIMES['medium'])
            [l2.craft('medium') for x in range(num_times_craft)]

        else:
            # easy craft take 12hrs, 48/12 = 4 times
            # how many times you can craft in 2 days
            num_times_craft = int(hours_in_period / CRAFT_TIMES['easy'])
            [l2.craft('easy') for x in range(num_times_craft)]


    #######################################################
    # After all legions have crafted/quested, take a snapshot of net treasures created/broken
    treasureAccounting.take_snapshot_of_treasure_balances()
    #######################################################

    broken_treasures_history = treasureAccounting.broken_treasures_history
    created_treasures_history = treasureAccounting.created_treasures_history
    net_diff_treasures_history = treasureAccounting.net_diff_treasures_history


    colors = {
        't1': 'crimson',
        't2': 'orange',
        't3': 'mediumorchid',
        't4': 'royalblue',
        't5': 'black',
    }

    # broken plots
    ax1.clear()
    ax1.plot(days, np.log10(broken_treasures_history['t5']), label="t5 broken", color=colors['t5'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_history['t4']), label="t4 broken", color=colors['t4'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_history['t3']), label="t3 broken", color=colors['t3'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_history['t2']), label="t2 broken", color=colors['t2'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_history['t1']), label="t1 broken", color=colors['t1'], linestyle='--')

    ax1.plot(days, np.log10(created_treasures_history['t5']), label="t5 minted", color=colors['t5'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_history['t4']), label="t4 minted", color=colors['t4'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_history['t3']), label="t3 minted", color=colors['t3'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_history['t2']), label="t2 minted", color=colors['t2'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_history['t1']), label="t1 minted", color=colors['t1'], linestyle=':')

    ax1.set_xlim([0,FRAMES])
    ax1.set_ylim([0,10])
    ax1.title.set_text("Treasures minted/broken from questing/crafting")
    ax1.grid(color='black', alpha=0.15)

    # minted plots
    ax2.clear()
    ax2.plot(days, legionPopulations.pct_crafting, label="%legions crafting", color='blue', linestyle='-', alpha=0.5)
    ax2.plot(days, legionPopulations.pct_questing, label="%legions questing", color='red', linestyle='-', alpha=0.5)

    ax2.set_xlim([0,FRAMES])
    ax2.set_ylim([0,1])
    ax2.title.set_text("Percentage of legions questing vs crafting")
    ax2.grid(color='black', alpha=0.15)

    # diff plots
    ax3.clear()
    ax3.plot(days, net_diff_treasures_history['t5'], label="t5", color=colors['t5'])
    ax3.plot(days, net_diff_treasures_history['t4'], label="t4", color=colors['t4'])
    ax3.plot(days, net_diff_treasures_history['t3'], label="t3", color=colors['t3'])
    ax3.plot(days, net_diff_treasures_history['t2'], label="t2", color=colors['t2'])
    ax3.plot(days, net_diff_treasures_history['t1'], label="t1", color=colors['t1'])

    ax3.set_xlim([0,FRAMES])
    ax3.set_ylim([-20000,20000])
    ax3.title.set_text("Net gain/burn in Treasures")
    ax3.grid(color='black', alpha=0.15)

    if day >= 33:
        ax3.axvline(x=6, color='black', linestyle=':', alpha=0.5, label="medium crafts start")

    if day >= 60:
        ax3.axvline(x=32, color='black', linestyle='--', alpha=0.5, label="hard crafts start")

    ax1.legend()
    ax2.legend()
    ax3.legend()

    # 50 frames, map to 100 days
    days_xticks = [
        0, 100, 200, 300, 400,
        500, 600, 700, 800,
    ]
    days_xticklabels = [
        '0', '100', '200', '300', '400',
        '500', '600', '700', '800',
    ]

    ax1.set_xticks(days_xticks)
    ax1.set_xticklabels(days_xticklabels, fontsize=8)
    ax1.set(xlabel='Days', ylabel='#treasures (log10 scale)')

    ax2.set_xticks(days_xticks)
    ax2.set_xticklabels(days_xticklabels, fontsize=8)
    ax2.set(xlabel='Days', ylabel='')

    ax3.set_xticks(days_xticks)
    ax3.set_xticklabels(days_xticklabels, fontsize=8)
    ax3.set(xlabel='Days', ylabel='')

    ax1_yticks = [
        0, 1, 2, 3,
        4, 5, 6, 7, 8
    ]
    ax1_yticklabels = [
        '0', '10', '100', '1,000',
        '10,000', '100,000', '1,000,000', '10,000,000', '100,000,000',
    ]
    ax1.set_yticks(ax1_yticks)
    ax1.set_yticklabels(ax1_yticklabels, fontsize=8)

    ax2_yticks = [
        0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1
    ]
    ax2_yticklabels = [
        '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%'
    ]
    ax2.set_yticks(ax2_yticks)
    ax2.set_yticklabels(ax2_yticklabels, fontsize=8)


    fig.suptitle(
        'DAY: {} | {:.0%} questing | {:.0f} legions | {:.0f} summoning'.format(
            day,
            pct_legions_questing_now,
            len(legionPopulations.legions_all),
            len(legionPopulations.legions_summoning),
        ),
        fontsize=14
    )


ani = FuncAnimation(fig, func_animate, frames=FRAMES, interval=100, repeat=False)

plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.1)
plt.legend()
plt.show()









