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
from parameters import TOTAL_MAGIC_SUPPLY, DEFAULT_USER_AUM_CAP

from harvester_boost_count import total_harvester_boost
from harvester_boost_count import getNftBoost


class HarvesterFactory:
    """
        Deploys harvesters
        * Governed by Admin
        * Allows for multiple wallets to hold Admin role to support future “wars” smart contracts and disabling/deployment automation
        * Stores harvester's configuration and exposes it to Middleman for rewards calculations
        * Allows for disabling a Harvester
            * Disabled harvester allows users only to exit
            * Rewards for harvester are canceled
            * Depositing and staking are disabled
        * Defines “Total Supply” of MAGIC for utilization calculations
    """


    def __init__(
        self,
        admins=['treasure.eth'],
        war_admins=['treasure.eth', 'bridgeworld-tournament.eth'],
        total_magic_supply=TOTAL_MAGIC_SUPPLY,
    ):
        self.admins = admins
        self.war_admins = war_admins
        self.total_magic_supply = total_magic_supply
        self.total_magic_supply_outside_harvesters = 0

        atlas_staked = EXPECTED_ATLAS_AUM * 1_000_000

        self.atlas_mine = Harvester(
            id='Atlas',
            is_atlas=True,
            is_active=True,
            aum_staked=atlas_staked, # pretend 0% of circulating supply staked for Atlas initially
            aum_cap=total_magic_supply, # uncapped, but use total_magic_supply to calculate utilization
        )
        self.harvesters = []

    def __repr__(self):
        ### Prints Harvester Details
        return """
        ========== Harvester Factory ==========
        Total Circulating Supply: {supply:,} MAGIC
        Total Supply Outside Harvesters: {supply_outside:,} MAGIC

        Atlas AUM Staked: {atlas_aum_staked:,} MAGIC

        Atlas Utilization: {atlas_util:.2%}
        Harvester Utilizations: {utils}

        """.format(
            supply=self.total_magic_supply,
            supply_outside=self.total_magic_supply_outside_harvesters,
            atlas_aum_staked=self.atlas_mine.aum_staked,
            atlas_util=self.atlas_mine.utilization,
            utils=['h{}: {:.2%}'.format(h.id, h.utilization) for h in self.harvesters],
        )

    def __getitem__(self, item):
        ### Lets you do harvester['parts'] to access its fields
        if item == 'admins':
            return self.admins
        if item == 'war_admins':
            return self.war_admins
        if item == 'total_magic_supply':
            return self.total_magic_supply
        if item == 'atlas_mine':
            return self.atlas_mine
        if item == 'harvesters':
            return self.harvesters

    def add_war_admin(self, war_admin_addr):
        # require(self.admins.includes(msg.sender))
        self.war_admin.append(war_admin_addr)

    def create_harvester(
        self,
        id=0,
        aum_cap=10_000_000,
        aum_staked=10_000_000,
    ):
        # require(self.war_admins.includes(msg.sender))
        existing_h = list(filter(lambda h: h.id == id, self.harvesters))

        if len(existing_h) > 0:
            print("harvester with that id already exists")
        else:
            # 1. create harvester and register with harvesterFactory
            h = Harvester(id=id, aum_cap=aum_cap, aum_staked=aum_staked)
            self.harvesters.append(h)

            # 2. update total_supply for Atlas (its cap) for Atlas utilization calculations
            self.update_atlas_cap_for_utilization()

            return h

    def deactivate_harvester(self, harvester_id):
        # require(self.war_admins.includes(msg.sender))
        h = next(h for h in self.harvesters if h.id == harvester_id)
        h.deactivate()
        # update total_supply for Atlas (its cap) for Atlas utilization calculations
        self.update_atlas_cap_for_utilization()


    def update_atlas_cap_for_utilization(self):
        # Atlas mine does not have a cap, but we set the cap as total_circulating_supply
        # to make utilisation easier to calculate.
        total_harvester_aums = np.sum([h.aum_staked for h in self.harvesters])
        total_supply_outside_harvesters = self.total_magic_supply - total_harvester_aums
        # this total_magic_supply needs to exclude wallets like ecosystem fund, etc.
        # e.g. the excludedWallets list.

        self.atlas_mine.set_cap_for_atlas(total_supply_outside_harvesters)
        self.total_magic_supply_outside_harvesters = total_supply_outside_harvesters




class Harvester:

    def __init__(
        self,
        id,
        parts=0,
        legions=0,
        avg_legion_rank=1,
        init_extractors=[],
        is_atlas=False,
        is_active=False, # dormant by default
        aum_cap=10_000_000,
        aum_staked=10_000_000, # assume its full when created for demo purposes
    ):
        self.id = id
        self.parts = 1
        self.legions = 1
        self.avg_legion_rank = avg_legion_rank
        self.extractors = init_extractors
        self.is_atlas = is_atlas
        self.is_active = is_active

        self.aum_staked = aum_staked
        self.aum_cap = aum_cap
        self.utilization = aum_staked / aum_cap
        # only harvesters have utilization at harvester-level, Atlas utilization
        # is calculated on total_circulating_supply of MAGIC
        self.user_aums = {}

    def __repr__(self):
        ### Prints Harvester Details
        return """
        ========== Harvester: {id} ==========
        Parts: {parts}
        Legions: {legions}
        Avg Legion Rank: {avg_legion_rank}
        Extractors: {extractors}
        AUM Staked: {aum_staked}
        AUM Cap: {aum_cap}
        Utilization: {utilization:.2%}
        IsActive: {is_active}

        """.format(
            id=self.id,
            parts=self.parts,
            legions=self.legions,
            avg_legion_rank=self.avg_legion_rank,
            extractors=self.extractors,
            aum_staked=self.aum_staked,
            aum_cap=self.aum_cap,
            utilization=self.utilization,
            is_active=self.is_active,
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
        if item == 'utilization':
            return self.utilization

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def stake_parts(self, parts=1):
        if self.parts + parts >= MAX_HARVESTER_PARTS:
            self.parts = MAX_HARVESTER_PARTS
        elif 0 < self.parts + parts:
            self.parts += parts

    def stake_legions(self, legions=1):
        if self.legions + legions >= MAX_LEGIONS:
            self.legions = MAX_LEGIONS
        elif 0 < self.legions + legions:
            self.legions += legions

    def unstake_parts(self, parts=1):
        if self.parts - parts <= 0:
            self.parts = 0
        else:
            self.parts -= parts

    def unstake_legions(self, legions=1):
        if self.legions - legions <= 0:
            self.legions = 0
        else:
            self.legions -= legions

    def set_avg_legion_rank(self, avg_legion_rank):
        if avg_legion_rank <= 5:
            self.avg_legion_rank = avg_legion_rank

    def set_extractors(self, extractors=[]):
        self.extractors = extractors

    def get_user_aum_cap(self):
        userNftBoost = getNftBoost()
        # DEFAULT_USER_AUM_CAP = 200_00
        return DEFAULT_USER_AUM_CAP * (1 + userNftBoost)

    def deposit(self, amount, msg_sender_addr):

        if self.user_aums.get(msg_sender_addr):
            user_aum = self.user_aums.get(msg_sender_addr)
        else:
            user_aum = 0

        new_user_aum = user_aum + amount

        # check new deposit doesn't cause balance to exceed cap
        assert(new_user_aum <= self.get_user_aum_cap())

        if not self.is_active:
            print("Harvester inactive, cannot deposit")
        else:
            new_aum = amount + self.aum_staked
            if new_aum > self.aum_cap:
                print("Deposit exceeds AUM cap: ", self.aum_cap)
            else:
                self.aum_staked += new_aum
                self.user_aums[msg_sender_addr] = new_aum
                self.utilization = new_aum / self.aum_cap # as a percentage of AUM cap

    def withdraw(self, amount):
        new_aum = self.aum_staked - amount
        self.utilization = new_aum / self.aum_cap # as a percentage of AUM cap

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

    def set_cap_for_atlas(self, aum_cap):
        # since Atlas is uncapped, it's cap is just the total_magic_supply circulating
        # we use this cap to determine utilization for atlas
        if self.is_atlas:
            self.aum_cap = aum_cap
            # update utilization for atlas
            self.utilization = self.aum_staked / aum_cap





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



