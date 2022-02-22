
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

from params import CRAFTING_EXP, QUESTING_EXP, PR_DROP_LOOT_FROM_QUEST
from questing_crafting import see_if_treasures_break, maybe_drop_loot_from_quest



class Legion:

    def __init__(
        self,
        treasure_accounting,
        is_genesis=True,
        class_type="common",
    ):
        self.treasure_accounting = treasure_accounting
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
        Craft points:\t{craftpoints}
        Loot:\t{loot}
        """.format(
            class_type=self.class_type,
            series="gen0" if self.is_genesis else "gen1",
            quest_lvl=self.quest_lvl,
            craft_lvl=self.craft_lvl,
            questpoints=self.qp,
            craftpoints=self.cp,
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
        gained_exp = QUESTING_EXP[lvl]

        loot = maybe_drop_loot_from_quest(lvl=lvl)
        # print("Gained {} points <total: {}>".format(gained_exp, self.qp + gained_exp))
        if loot:
            # print("Found loot! {}".format(loot))
            self.treasure_accounting.add_to_created(treasures=[ loot ])
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
        gained_exp = CRAFTING_EXP[lvl]

        broken = see_if_treasures_break(craft_lvl=lvl)
        # print('broken: ', broken)
        self.treasure_accounting.add_to_broken(treasures=broken)

        # print("Gained {} points <total: {}>".format(gained_exp, self.cp + gained_exp))
        self.cp += gained_exp
        self._update_own_crafting_lvl()


    def _update_own_crafting_lvl(self):
        new_lvl = get_lvl_from_crafting_points(self.cp)
        self.craft_lvl = new_lvl
        # if (self.craft_lvl != new_lvl):
        #     print("Level increased to {}!".format(new_lvl))



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
    if cp >= CRAFT_LVL_TIERS['level_6']:
        return 6
    elif cp >= CRAFT_LVL_TIERS['level_5']:
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
    "level_2": 140,
    "level_3": 300,
    "level_4": 460,
    "level_5": 620,
    "level_6": 1100,
    # incremental increases in levels require:
    # "level_1": 140,
    # "level_2": 160,
    # "level_3": 160,
    # "level_4": 160,
    # "level_5": 480,
    # "level_5": 480,
}




