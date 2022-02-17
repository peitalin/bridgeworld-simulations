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
from parameters import TOTAL_MAGIC_SUPPLY

from harvester_boost_count import total_harvester_boost


class HarvesterFactory:

    def __init__(
        self,
        admins=['treasure.eth'],
        war_admins=['treasure.eth', 'bridgeworld-tournament.eth'],
        total_magic_supply=TOTAL_MAGIC_SUPPLY,
    ):
        self.admins = admins
        self.war_admins = war_admins
        self.total_magic_supply = total_magic_supply
        self.atlas = Harvester(id='Atlas', is_atlas=True, is_active=True, aum_cap=None)
        self.harvesters = []

    def __getitem__(self, item):
        ### Lets you do harvester['parts'] to access its fields
        if item == 'admins':
            return self.admins
        if item == 'war_admins':
            return self.war_admins
        if item == 'total_magic_supply':
            return self.total_magic_supply
        if item == 'atlas':
            return self.atlas
        if item == 'harvesters':
            return self.harvesters

    def add_war_admin(self, war_admin_addr):
        # require(self.admins.includes(msg.sender))
        self.war_admin.append(war_admin_addr)

    def create_harvester(
        self,
        id=0,
        aum_cap=10_000_000,
    ):
        # require(self.war_admins.includes(msg.sender))
        h = Harvester(id=id, aum_cap=aum_cap)
        self.harvesters.append(h)
        return h

    def deactivate_harvester(self, harvester_id):
        # require(self.war_admins.includes(msg.sender))
        h = next(h for h in self.harvesters if h['id'] == harvester_id)
        h.deactivate()




class Harvester:

    def __init__(
        self,
        id,
        parts=0,
        legions=0,
        avg_legion_rank=2,
        extractors=[],
        is_atlas=False,
        is_active=False, # dormant by default
        aum_cap=10_000_000,
    ):
        self.id = id
        self.parts = 1
        self.legions = 1
        self.avg_legion_rank = avg_legion_rank
        self.extractors = extractors
        self.is_atlas = is_atlas
        self.is_active = is_active

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

    def deactivate(self):
        self.is_active = False

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

    def deposit(self, amount):
        if self.is_active:
            print('deposit')
            # self.deposit.append(amount)

    def withdraw(self, amount):
        print('withdraw')
        # self.deposit.append(amount)


    def getMiningBoost(self):
        if self.is_active:
            return total_harvester_boost(
                num_parts=self.parts,
                num_legions=self.legions,
                avg_legion_rank=self.avg_legion_rank,
                extractors=self.extractors,
                is_atlas=self.is_atlas,
            )
        else:
            return 0





def calculate_deposit_cap_per_address(boost, default_cap=200_000):
    """
        Works out a wallet's deposit cap, based on its individual-level NFTboost
        (staked legions + treasures => NFTboost)

        default_cap = 200,000 MAGIC

        Then caps would look something like:
        • Guilds like clocksnatcher with 1/1, 2x all-class + 20x honeycomb
            • cap is ~2.8mil MAGIC
        • Smaller guilds with 3x all-class + 20x honeycomb
            • cap is ~2mil MAGIC
        • Stakers with no NFTs
            • cap is 200k MAGIC
        • middle-class folk with 1x genesis legion + 2 honeycombs
            • cap is around ~360k MAGIC
    """
    # remember to add the 1 to NFTBoost since it starts at 0% if no NFTs are present
    # see user-level boosts in whitepaper
    return (1 + NFTBoost) * default_cap



