
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

from params import CRAFTING_EXP, QUESTING_EXP, PR_DROP_LOOT_FROM_QUEST
from params import QUEST_TIMES, CRAFT_TIMES
from legion import Legion
from treasure_accounting import TreasureAccounting

#################################################
#################################################
##### Questing and Crafting Simulations
#################################################
#################################################

def calculate_percentage_legion_questing(
    net_inflation_deflation = 0,
    threshold_upper = 500,
    threshold_lower = 500,
    max_pct_upper = 0.8,
    min_pct_lower = 0.4,
):
    """
        net_inflation_deflation: net inflation/deflation of a particular tier of treasures
        threshold_upper: upper threshold where 100% of legions are crafting
        threshold_lower: lower threshold where 100% of legions are questing
        offset: makes sure percentage_legion_questing stays within this thresholds
    """

    if net_inflation_deflation >= 0:
        # too much inflation, less legions questing pls
        pct = (100 - (threshold_lower + net_inflation_deflation)/10) / 100
    else:
        # too much burn, more legions questing pls
        pct = (100 - (threshold_upper + net_inflation_deflation)/10) / 100

    if pct >= max_pct_upper:
        return max_pct_upper
    elif pct <= min_pct_lower:
        return min_pct_lower
    else:
        return pct





days = [] # x-axis is days
pct_crafting = []
pct_questing = []

fig, (ax1, ax2, ax3) = plt.subplots(1,3, gridspec_kw={'width_ratios': [1,1,1]})
fig.set_size_inches(15, 8)

## Initial numbers of legions crafting, questing, summoning
NUM_LEGIONS_QUESTING = 50
NUM_LEGIONS_CRAFTING = 50
NUM_LEGIONS_SUMMONING = 0
NUM_LEGIONS = 1000


treasureAccounting = TreasureAccounting()

legions_summoning = [Legion(treasureAccounting) for l in range(NUM_LEGIONS_SUMMONING)]
# legions_questing = [Legion(treasureAccounting) for l in range(NUM_LEGIONS_QUESTING)]
# legions_crafting = [Legion(treasureAccounting) for l in range(NUM_LEGIONS_CRAFTING)]
legions_questing = []
legions_crafting = []
legions_all = [Legion(treasureAccounting) for l in range(NUM_LEGIONS)]

created_treasures_array = {
    't1': [],
    't2': [],
    't3': [],
    't4': [],
    't5': [],
}
broken_treasures_array = {
    't1': [],
    't2': [],
    't3': [],
    't4': [],
    't5': [],
}
net_diff_treasures_array = {
    't1': [],
    't2': [],
    't3': [],
    't4': [],
    't5': [],
}

FRAMES = 800


def func_animate(i):

    ## Every loop of i is 2 days
    day = i * 2
    hours_in_2_days = 24 * 2

    global days
    days.append(day) # 2 days per tick

    # global legions_questing
    # global legions_crafting
    global legions_all
    global pct_legions_to_questing


    rolling_mean_t5_supply = np.mean(net_diff_treasures_array['t5'][-7:])
    if not np.isnan(rolling_mean_t5_supply):
        pct_legions_to_questing = calculate_percentage_legion_questing(rolling_mean_t5_supply)
    else:
        pct_legions_to_questing = 0.5
    print("\n\npct_legions questing: ", pct_legions_to_questing)

    pct_questing.append(pct_legions_to_questing)
    pct_crafting.append(1-pct_legions_to_questing)


    ## Reset population of legions crafting vs questing every iteration
    ## to let legions freely switch between questing or crafting

    num_legions = len(legions_all)
    num_legions_questing = int(num_legions * pct_legions_to_questing)
    num_legions_crafting = int(num_legions * (1 - pct_legions_to_questing))

    print('rolling mean t5 supply', rolling_mean_t5_supply)
    print('#questing', num_legions_questing)
    print('#crafting', num_legions_crafting)
    legions_questing = legions_all[:num_legions_questing] if num_legions_questing > 0 else []
    legions_crafting = legions_all[-num_legions_crafting:] if num_legions_crafting > 0 else []

    len_legions_summoning = len(legions_summoning)
    len_legions_questing = len(legions_questing)
    len_legions_crafting = len(legions_crafting)

    print('questing', len_legions_questing)
    print('crafting', len_legions_crafting)

    # every 7 days, add new summoned legions to questing
    # number of new legions is just length of legions_summoning array they start at level 0 questing/crafting
    # because every i is two days, mod 7 >= 1 will roughly count the passage of weeks
    if (day % 7 >= 1) or (day % 7 == 0):
        # new batch of summoned legions
        new_aux_legions = legions_summoning.copy()
        midpoint_new_legions = int(len(new_aux_legions)/2)

        first_half_legions = new_aux_legions[:midpoint_new_legions] if midpoint_new_legions > 0 else []
        last_half_legions = new_aux_legions[midpoint_new_legions:] if midpoint_new_legions > 0 else []

        [legions_all.insert(0, s) for s in first_half_legions]
        [legions_all.append(s) for s in last_half_legions]

        # suppose % of new aux legions go into questing
        # legions_to_questing = round(len_legions_summoning * pct_legions_to_questing)

        # [legions_questing.append(s) for s in new_aux_legions[:legions_to_questing]]
        # [legions_crafting.append(s) for s in new_aux_legions[legions_to_questing:]]
        # print("len legions questing: ", len(legions_questing))
        # print("len legions crafting: ", len(legions_crafting))


    for l1 in legions_questing:
        if l1.quest_lvl >= 5:
            # hard quests take 16hrs, 48/16 = 3 times
            num_times_quest = int(hours_in_2_days / QUEST_TIMES['hard'])
            [l1.quest() for x in range(num_times_quest)]
        elif l1.quest_lvl >= 3:
            # medium quests take 12hrs, 48/12 = 4 times
            num_times_quest = int(hours_in_2_days / QUEST_TIMES['medium'])
            [l1.quest() for x in range(num_times_quest)]
        else:
            # easy quests take 8hrs, 48/8 = 6 times
            num_times_quest = int(hours_in_2_days / QUEST_TIMES['easy'])
            [l1.quest() for x in range(num_times_quest)]


    for l2 in legions_crafting:
        if l2.craft_lvl >= 5:
            # hard craft take 48hrs, 48/48 = 1 times
            # how many times you can craft in 2 days
            num_times_craft = int(hours_in_2_days / CRAFT_TIMES['hard'])
            [l2.craft('hard') for x in range(num_times_craft)]

        elif l2.craft_lvl >= 3:
            # medium craft take 16hrs, 48/16 = 3 times
            # how many times you can craft in 2 days
            num_times_craft = int(hours_in_2_days / CRAFT_TIMES['medium'])
            [l2.craft('medium') for x in range(num_times_craft)]

        else:
            # easy craft take 12hrs, 48/12 = 4 times
            # how many times you can craft in 2 days
            num_times_craft = int(hours_in_2_days / CRAFT_TIMES['easy'])
            [l2.craft('easy') for x in range(num_times_craft)]

    broken_treasures = treasureAccounting.broken_treasures
    created_treasures = treasureAccounting.created_treasures

    broken_treasures_array['t1'].append(broken_treasures['t1'])
    broken_treasures_array['t2'].append(broken_treasures['t2'])
    broken_treasures_array['t3'].append(broken_treasures['t3'])
    broken_treasures_array['t4'].append(broken_treasures['t4'])
    broken_treasures_array['t5'].append(broken_treasures['t5'])

    created_treasures_array['t1'].append(created_treasures['t1'])
    created_treasures_array['t2'].append(created_treasures['t2'])
    created_treasures_array['t3'].append(created_treasures['t3'])
    created_treasures_array['t4'].append(created_treasures['t4'])
    created_treasures_array['t5'].append(created_treasures['t5'])

    net_diff_treasures_array['t1'].append(created_treasures['t1'] - broken_treasures['t1'])
    net_diff_treasures_array['t2'].append(created_treasures['t2'] - broken_treasures['t2'])
    net_diff_treasures_array['t3'].append(created_treasures['t3'] - broken_treasures['t3'])
    net_diff_treasures_array['t4'].append(created_treasures['t4'] - broken_treasures['t4'])
    net_diff_treasures_array['t5'].append(created_treasures['t5'] - broken_treasures['t5'])

    colors = {
        't1': 'crimson',
        't2': 'orange',
        't3': 'mediumorchid',
        't4': 'royalblue',
        't5': 'black',
    }


    # broken plots
    ax1.clear()
    ax1.plot(days, np.log10(broken_treasures_array['t5']), label="t5 broken", color=colors['t5'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_array['t4']), label="t4 broken", color=colors['t4'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_array['t3']), label="t3 broken", color=colors['t3'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_array['t2']), label="t2 broken", color=colors['t2'], linestyle='--')
    ax1.plot(days, np.log10(broken_treasures_array['t1']), label="t1 broken", color=colors['t1'], linestyle='--')

    ax1.plot(days, np.log10(created_treasures_array['t5']), label="t5 minted", color=colors['t5'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_array['t4']), label="t4 minted", color=colors['t4'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_array['t3']), label="t3 minted", color=colors['t3'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_array['t2']), label="t2 minted", color=colors['t2'], linestyle=':')
    ax1.plot(days, np.log10(created_treasures_array['t1']), label="t1 minted", color=colors['t1'], linestyle=':')

    ax1.set_xlim([0,FRAMES])
    ax1.set_ylim([0,10])
    ax1.title.set_text("Treasures minted/broken from questing/crafting")
    ax1.grid(color='black', alpha=0.15)

    # minted plots
    ax2.clear()
    ax2.plot(days, pct_crafting, label="%legions crafting", color='blue', linestyle='-', alpha=0.5)
    ax2.plot(days, pct_questing, label="%legions questing", color='red', linestyle='-', alpha=0.5)

    ax2.set_xlim([0,FRAMES])
    ax2.set_ylim([0,1])
    ax2.title.set_text("Percentage of legions questing vs crafting")
    ax2.grid(color='black', alpha=0.15)

    # diff plots
    ax3.clear()
    ax3.plot(days, net_diff_treasures_array['t5'], label="t5", color=colors['t5'])
    ax3.plot(days, net_diff_treasures_array['t4'], label="t4", color=colors['t4'])
    ax3.plot(days, net_diff_treasures_array['t3'], label="t3", color=colors['t3'])
    ax3.plot(days, net_diff_treasures_array['t2'], label="t2", color=colors['t2'])
    ax3.plot(days, net_diff_treasures_array['t1'], label="t1", color=colors['t1'])

    ax3.set_xlim([0,FRAMES])
    ax3.set_ylim([-10000,10000])
    ax3.title.set_text("Net gain/burn in Treasures")
    ax3.grid(color='black', alpha=0.15)

    if day >= 14:
        ax3.axvline(x=6, color='black', linestyle=':', alpha=0.5, label="medium crafts start")

    if day >= 40:
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
        # 'DAY: {} | {} crafting | {} questing | {} summoning => {:.0%} to questing'.format(
        #     day,
        #     len_legions_crafting,
        #     len_legions_questing,
        #     len_legions_summoning,
        #     pct_legions_to_questing,
        # ),
        'DAY: {} | {:.0%} questing'.format(
            day,
            pct_legions_to_questing,
        ),
        fontsize=14
    )


ani = FuncAnimation(fig, func_animate, frames=FRAMES, interval=100, repeat=False)

plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.1)
plt.legend()
plt.show()









