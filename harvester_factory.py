import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

# parameters for configuring boosts
from parameters import PARTS_BOOST_FACTOR, LEGIONS_BOOST_FACTOR, DISTANCE_BOOST_FACTOR
from parameters import ATLAS_MINE_BONUS, EXPECTED_ATLAS_AUM, MAX_HARVESTER_PARTS, MAX_EXTRACTORS
from parameters import MIN_LEGIONS, MAX_LEGIONS
from parameters import MAX_MAP_HEIGHT, MAX_MAP_WIDTH
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS


class HarvesterFactory:

    def __init__(
        self,
        admins=['treasure.eth'],
        war_admins=['treasure.eth', 'bridgeworld-tournament.eth'],
    ):
        self.admins = admins
        self.war_admins = war_admins

    def __getitem__(self, item):
        ### Lets you do harvester['parts'] to access its fields
        if item == 'admins':
            return self.admins
        if item == 'war_admins':
            return self.war_admins

    def create_harvester(self, aum_cap=10_000_000):
        return Harvester(aum_cap=aum_cap)




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
        aum_cap=10_000_000,
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
        ### Prints Harvester Details
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
        ### Lets you do harvester['parts'] to access its fields
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
        if self.parts + parts <= MAX_HARVESTER_PARTS:
            self.parts += parts
        else:
            self.parts = MAX_HARVESTER_PARTS

    def increment_legions(self, legions=1):
        if self.legions + legions <= MAX_LEGIONS:
            self.legions += legions
        else:
            self.legions = MAX_LEGIONS

    def set_avg_legion_rank(self, avg_legion_rank):
        if avg_legion_rank <= 5:
            self.avg_legion_rank = avg_legion_rank

    def add_extractor(self, extractor):
        self.extractors.append(extractor)






