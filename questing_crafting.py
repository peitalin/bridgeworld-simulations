
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation


time_to_complete = {
    "easy": 8,
    "medium": 12,
    "hard": 16,
}

# 20%
PR_DROP_LOOT_FROM_QUEST = 0.2


def add_to_global_created(treasures=[]):
    global created_treasures
    for t in treasures:
        created_treasures[t] += 1

def add_to_global_broken(treasures=[]):
    global broken_treasures
    for t in treasures:
        broken_treasures[t] += 1



class Legion:

    def __init__(
        self,
        is_genesis=True,
        class_type="common",
    ):
        self.craft_lvl = 1
        self.quest_lvl = 1
        self.qp = 0 # questing points
        self.cp = 0 # crafting points
        self.class_type = class_type
        self.is_genesis = is_genesis
        self.loot = {
            't1': 0,
            't2': 0,
            't3': 0,
            't4': 0,
            't5': 0,
            'shards': 0,
            'starlight': 0,
        }

    def __repr__(self):
        return """
        Legion:\t{class_type} - {series}
        Quest level:\t{quest_lvl}
        Craft level:\t{craft_lvl}
        Quest points:\t{questpoints}
        Loot:\t{loot}
        """.format(
            class_type=self.class_type,
            series="gen0" if self.is_genesis else "gen1",
            quest_lvl=self.quest_lvl,
            craft_lvl=self.craft_lvl,
            questpoints=self.qp,
            loot=self.loot
        )

    def _check_lvl_for_quest(self, lvl):
        if lvl == "hard":
            assert self.quest_lvl >= 5, "Must be at least quest lvl. 5"
        if lvl == "medium":
            assert self.quest_lvl >= 3, "Must be at least quest lvl. 3"

    def _check_lvl_for_craft(self, lvl):
        if lvl == "hard":
            assert self.craft_lvl >= 5, "Must be at least craft lvl. 5"
        if lvl == "medium":
            assert self.craft_lvl >= 3, "Must be at least craft lvl. 3"

    def _get_quest_difficulty(self):
        if self.quest_lvl >= 5:
            return "hard"
        elif self.quest_lvl >= 3:
            return "medium"
        else:
            return "easy"

    def _get_craft_difficulty(self):
        if self.craft_lvl >= 5:
            return "hard"
        elif self.craft_lvl >= 3:
            return "medium"
        else:
            return "easy"


    def quest(self, lvl=None):

        if lvl:
            self._check_lvl_for_quest(lvl)
        else:
            lvl = self._get_quest_difficulty()

        gained_exp = 10
        if lvl == 'easy':
            gained_exp = 10
        elif lvl == 'medium':
            gained_exp = 20
        elif lvl == 'hard':
            gained_exp = 40

        loot = maybe_drop_loot_from_quest(lvl=lvl)
        # print("Gained {} points <total: {}>".format(gained_exp, self.qp + gained_exp))
        if loot:
            # print("Found loot! {}".format(loot))
            add_to_global_created(treasures=[ loot ])
            self.loot[loot] += 1

        self._update_shards_and_starlight(lvl=lvl)
        self.qp += gained_exp
        self._update_own_questing_lvl()

    def _update_own_questing_lvl(self):
        new_lvl = get_lvl_from_questing_points(self.qp)
        self.quest_lvl = new_lvl
        # if (self.quest_lvl != new_lvl):
        #     print("Level increased to {}!".format(new_lvl))

    def _update_shards_and_starlight(self, lvl):
        if lvl=='easy':
            self.loot['shards'] += 1
            self.loot['starlight'] += 1
        if lvl=='medium':
            self.loot['shards'] += 2
            self.loot['starlight'] += 2
        if lvl=='hard':
            self.loot['shards'] += 3
            self.loot['starlight'] += 3


    def craft(self, lvl=None):

        if lvl:
            self._check_lvl_for_craft(lvl)
        else:
            lvl = self._get_craft_difficulty()

        gained_exp = 10
        if self.craft_lvl == 1:
            gained_exp = 10
        elif self.craft_lvl == 2:
            gained_exp = 20
        elif self.craft_lvl == 3:
            gained_exp = 30
        elif self.craft_lvl == 4:
            gained_exp = 40
        elif self.craft_lvl == 5:
            gained_exp = 50

        broken = see_if_treasures_break(craft_lvl=lvl)
        # print('broken: ', broken)
        add_to_global_broken(treasures=broken)

        # print("Gained {} points <total: {}>".format(gained_exp, self.cp + gained_exp))
        self.cp += gained_exp
        self._update_own_crafting_lvl()


    def _update_own_crafting_lvl(self):
        new_lvl = get_lvl_from_crafting_points(self.cp)
        self.craft_lvl = new_lvl
        # if (self.craft_lvl != new_lvl):
        #     print("Level increased to {}!".format(new_lvl))




def maybe_drop_loot_from_quest(lvl):
    # from 0 to 100
    score = np.random.uniform(0,100)
    if score < (100 - PR_DROP_LOOT_FROM_QUEST * 100):
        return None

    if lvl == 'easy':
        return drop_loot_tiers(lvl='easy')
    if lvl == 'medium':
        return drop_loot_tiers(lvl='medium')
    if lvl == 'hard':
        return drop_loot_tiers(lvl='hard')



def drop_loot_tiers(lvl='easy'):
    # pr: probabilities of dropping t1, t2, t3, t4, t5 loot
    if lvl=='easy':
        pr = [0, 2.5, 5, 15, 77.5]
    if lvl=='medium':
        pr = [1.5, 5, 7, 17, 69.5]
    if lvl=='hard':
        pr = [2.5, 9, 8, 22, 58.5]

    score2 = np.random.uniform(0,100)
    t1 = pr[0]
    t2 = pr[1] + t1
    t3 = pr[2] + t2
    t4 = pr[3] + t3
    t5 = pr[4] + t4

    if score2 <= t1:
        return 't1'
    if t1 < score2 <= t2:
        return 't2'
    if t2 < score2 <= t3:
        return 't3'
    if t3 < score2 <= t4:
        return 't4'
    if t4 < score2:
        return 't5'



def get_lvl_from_questing_points(qp):
    if qp >= QUEST_LVL_TIERS['level_6']:
        return 6
    elif qp >= QUEST_LVL_TIERS['level_5']:
        return 5
    elif qp >= QUEST_LVL_TIERS['level_4']:
        return 4
    elif qp >= QUEST_LVL_TIERS['level_3']:
        return 3
    elif qp >= QUEST_LVL_TIERS['level_2']:
        return 2
    else:
        return 1


def get_lvl_from_crafting_points(cp):
    if cp >= CRAFT_LVL_TIERS['level_5']:
        return 5
    elif cp >= CRAFT_LVL_TIERS['level_4']:
        return 4
    elif cp >= CRAFT_LVL_TIERS['level_3']:
        return 3
    elif cp >= CRAFT_LVL_TIERS['level_2']:
        return 2
    else:
        return 1

# total questing points needed to hit lvls
QUEST_LVL_TIERS = {
    "level_1": 0,
    "level_2": 100,
    "level_3": 300,
    "level_4": 900,
    "level_5": 2400,
    "level_6": 4400,
    # incremental increases in levels require:
    # "level_1": 100,
    # "level_2": 200,
    # "level_3": 600,
    # "level_4": 1500,
    # "level_5": 2000,
}
# total questing points needed to hit lvls
CRAFT_LVL_TIERS = {
    "level_1": 0,
    "level_2": 100,
    "level_3": 300,
    "level_4": 700,
    "level_5": 2200,
    # incremental increases in levels require:
    # "level_1": 100,
    # "level_2": 200,
    # "level_3": 400,
    # "level_4": 1500,
    # "level_5": 2000,
}


TREASURE_BREAK_PR = {
    "grin": 0.00597,
    "honeycomb": 0.00597,
    "t1": 0.03275,
    "t2": 0.06440,
    "t3": 0.08203,
    "t4": 0.11293,
    "t5": 0.18104,
}

def see_if_treasures_break(craft_lvl='easy'):

    if craft_lvl == 'easy':
        treasures = ['t4','t5','t5']
    if craft_lvl == 'medium':
        treasures = ['t3', 't4', 't4', 't5', 't5']
    if craft_lvl == 'hard':
        treasures = ['t1', 't2', 't3', 't4', 't4', 't5', 't5']

    broken = []

    for t in treasures:
        # score = 100%
        score = np.random.uniform(0,1)
        if score < TREASURE_BREAK_PR[t]:
            broken.append(t)

    return broken












created_treasures = {
    't1': 0,
    't2': 0,
    't3': 0,
    't4': 0,
    't5': 0,
}
broken_treasures = {
    't1': 0,
    't2': 0,
    't3': 0,
    't4': 0,
    't5': 0,
}
days = [] # x-axis is days

fig, (ax1, ax2, ax3) = plt.subplots(1,3, gridspec_kw={'width_ratios': [1,1,1]})
fig.set_size_inches(15, 8)

## Initial numbers of legions crafting, questing, summoning
NUM_LEGIONS_QUESTING = 50
NUM_LEGIONS_CRAFTING = 50
NUM_LEGIONS_SUMMONING = 50

legions_summoning = [Legion() for l in range(NUM_LEGIONS_SUMMONING)]
legions_questing = [Legion() for l in range(NUM_LEGIONS_QUESTING)]
legions_crafting = [Legion() for l in range(NUM_LEGIONS_CRAFTING)]

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

FRAMES = 100

def func_animate(i):

    ## Every loop of i is 2 days
    day = i * 2
    days.append(day) # 2 days per tick

    global legions_questing
    global legions_crafting

    len_legions_summoning = len(legions_summoning)
    len_legions_crafting = len(legions_crafting)
    len_legions_questing = len(legions_questing)



    # every 7 days, add new summoned legions to questing
    # number of new legions is just length of legions_summoning array they start at level 0 questing/crafting
    # because every i is two days, mod 7 >= 1 will roughly count the passage of weeks
    if day % 7 >= 1:

        # new batch of summoned legions
        new_aux_legions = legions_summoning.copy()
        # suppose 75% of new aux legions go into questing
        pct_legions_to_questing = 0.75
        legions_to_questing = round(len_legions_summoning * pct_legions_to_questing)
        print("legions_to_questing: ", legions_to_questing)


        [legions_questing.append(s) for s in new_aux_legions[:legions_to_questing]]
        [legions_crafting.append(s) for s in new_aux_legions[legions_to_questing:]]
        print("len legions questing: ", len(legions_questing))
        print("len legions crafting: ", len(legions_crafting))


    for l1 in legions_questing:
        # hard quests take 16hrs, 48/16 = 3 times
        if l1.quest_lvl >= 5:
            [l1.quest() for x in range(3)]
        # medium quests take 12hrs, 48/12 = 4 times
        elif l1.quest_lvl >= 3:
            [l1.quest() for x in range(4)]
        # easy quests take 8hrs, 48/8 = 6 times
        else:
            [l1.quest() for x in range(6)]


    for l2 in legions_crafting:
        # hard craft take 16hrs, 48/16 = 3 times
        if l2.craft_lvl >= 5:
            [l2.craft() for x in range(3)]
        # medium craft take 12hrs, 48/12 = 4 times
        elif l2.craft_lvl >= 3:
            [l2.craft() for x in range(4)]
        # easy craft take 8hrs, 48/8 = 6 times
        else:
            [l2.craft() for x in range(6)]


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

    # broken plots
    ax1.clear()
    ax1.plot(days, broken_treasures_array['t5'], label="t5", color='royalblue')
    ax1.plot(days, broken_treasures_array['t3'], label="t3", color='mediumorchid')
    ax1.plot(days, broken_treasures_array['t1'], label="t1", color='crimson')

    ax1.set_xlim([0,FRAMES])
    ax1.set_ylim([0,9000])
    ax1.title.set_text("Treasures broken from crafting")
    ax1.grid(color='black', alpha=0.15)

    # minted plots
    ax2.clear()
    ax2.plot(days, created_treasures_array['t5'], label="t5", color='royalblue')
    ax2.plot(days, created_treasures_array['t3'], label="t3", color='mediumorchid')
    ax2.plot(days, created_treasures_array['t1'], label="t1", color='crimson')

    ax2.set_xlim([0,FRAMES])
    ax2.set_ylim([0,9000])
    ax2.title.set_text("Treasures created from questing")
    ax2.grid(color='black', alpha=0.15)

    # diff plots
    ax3.clear()
    ax3.plot(days, net_diff_treasures_array['t5'], label="t5", color='royalblue')
    ax3.plot(days, net_diff_treasures_array['t3'], label="t3", color='mediumorchid')
    ax3.plot(days, net_diff_treasures_array['t1'], label="t1", color='crimson')

    ax3.set_xlim([0,FRAMES])
    ax3.set_ylim([-8000,1000])
    ax3.title.set_text("Net gain/burn in Treasures")
    ax3.grid(color='black', alpha=0.15)

    if i*2 >= 6:
        ax1.axvline(x=6, color='black', linestyle=':', alpha=0.5, label="medium crafts start")
        ax3.axvline(x=6, color='black', linestyle=':', alpha=0.5, label="medium crafts start")

    if i*2 >= 32:
        ax1.axvline(x=32, color='black', linestyle='--', alpha=0.5, label="hard crafts start")
        ax3.axvline(x=32, color='black', linestyle='--', alpha=0.5, label="hard crafts start")

    ax1.legend()
    ax2.legend()
    ax3.legend()

    # 50 frames, map to 100 days
    ax1.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    ax1.set_xticklabels(['0', '20', '40', '60', '80', '100', '120', '140', '160', '180', '200'], fontsize=8)
    ax1.set(xlabel='Days', ylabel='')
    ax2.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    ax2.set_xticklabels(['0', '20', '40', '60', '80', '100', '120', '140', '160', '180', '200'], fontsize=8)
    ax2.set(xlabel='Days', ylabel='')
    ax3.set_xticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    ax3.set_xticklabels(['0', '20', '40', '60', '80', '100', '120', '140', '160', '180', '200'], fontsize=8)
    ax3.set(xlabel='Days', ylabel='')

    fig.suptitle('{} crafting | {} questing | {} summoning'.format(len_legions_crafting, len_legions_questing, len_legions_summoning), fontsize=14)


ani = FuncAnimation(fig, func_animate, frames=FRAMES, interval=100, repeat=False)

plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.1)
plt.legend()
plt.show()









