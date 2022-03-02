
import numpy as np
from params import PR_DROP_LOOT_FROM_QUEST


def maybe_drop_loot_from_quest(lvl):
    # from 0 to 100
    score = np.random.uniform(0,100)
    if score < (100 - (PR_DROP_LOOT_FROM_QUEST * 100)):
        return None

    return drop_loot_tiers(lvl=lvl)



def drop_loot_tiers(lvl='easy'):
    # pr: probabilities of dropping t1, t2, t3, t4, t5 loot
    # in percentages
    if lvl=='easy':
        pr = [0, 2.5, 5, 15, 77.5]
    if lvl=='medium':
        pr = [2, 5.5, 8, 17, 67.5]
    if lvl=='hard':
        pr = [4, 10, 11, 22, 53]

    score2 = np.random.uniform(0,100)
    # cutoffs for probability intervals
    t1 = pr[0]
    t2 = pr[1] + t1
    t3 = pr[2] + t2
    t4 = pr[3] + t3
    t5 = pr[4] + t4

    # see where RNG sample lies in between intervals
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



# TREASURE_BREAK_PR = {
#     "grin": 0.00597,
#     "honeycomb": 0.00597,
#     "t1": 0.03275,
#     "t2": 0.06440,
#     "t3": 0.08203,
#     "t4": 0.11293,
#     "t5": 0.18104,
# }
TREASURE_BREAK_PR = {
    "grin": 0.0,
    "honeycomb": 0.0,
    "t1": 0.027,
    "t2": 0.054,
    "t3": 0.069,
    "t4": 0.113,
    "t5": 0.18104,
}
# t1: 3.2% => 2.7%
# t2: 6.4% => 5.4%
# t3: 8.2% => 6.9%
# t4: unchanged
# t5: unchanged


CRAFTING_RECIPES = {
    # Prism
    "easy": [
        't5', 't5', 't5', 't5',
        't4', 't4',
        't3',
    ],

    # Harvester Part
    "medium": [
        't5', 't5', 't5', 't5', 't5',
        't4', 't4',
        # 't3', 't3', 't3',
        't3', 't3',
        # 't2', 't2',
        't2',
        't1',
    ],

    # Extractor
    "hard": [
        # 't5', 't5', 't5', 't5', 't5',
        't5', 't5', 't5', 't5',
        't4', 't4', 't4',
        't3',
        # 't2', 't2',
        't2',
    ],
}


def see_if_treasures_break(craft_lvl='easy'):

    treasures = CRAFTING_RECIPES[craft_lvl]

    broken = []

    for t in treasures:
        # score = 100%
        score = np.random.uniform(0,1)
        if score < TREASURE_BREAK_PR[t]:
            broken.append(t)

    return broken


