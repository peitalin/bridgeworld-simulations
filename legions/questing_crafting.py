
import numpy as np
from params import PR_DROP_LOOT_FROM_QUEST


def maybe_drop_loot_from_quest(lvl):
    # from 0 to 100
    score = np.random.uniform(0,100)
    if score < (100 - (PR_DROP_LOOT_FROM_QUEST * 100)):
        return None

    return drop_loot_tiers(lvl=lvl)


# pr: probabilities of dropping t1, t2, t3, t4, t5 loot in percentages
LOOT_DROP_PR = {
    "easy": {
        "t1": 0,
        "t2": 0.025,
        "t3": 0.05,
        "t4": 0.15,
        "t5": 0.775
    },
    "medium": {
        "t1": 0.02,
        "t2": 0.055,
        "t3": 0.08,
        "t4": 0.17,
        "t5": 0.675
    },
    "hard": {
        "t1": 0.04,
        "t2": 0.10,
        "t3": 0.11,
        "t4": 0.22,
        "t5": 0.53
    },
}

def drop_loot_tiers(lvl='easy'):
    loot_pr = LOOT_DROP_PR[lvl]
    treasure = np.random.choice(a=list(loot_pr.keys()), p=list(loot_pr.values()))
    return treasure



TREASURE_BREAK_PR = {
    "grin": 0.0,
    "honeycomb": 0.0,
    "t1": 0.027,
    "t2": 0.054,
    "t3": 0.069,
    "t4": 0.113,
    "t5": 0.18104,
}

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
        't3', 't3',
        't2',
        't1',
    ],

    # Extractor
    "hard": [
        't5', 't5', 't5', 't5',
        't4', 't4', 't4',
        't3',
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


