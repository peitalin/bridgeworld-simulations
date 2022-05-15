import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

# parameters for configuring boosts
from parameters import PARTS_BOOST_FACTOR, LEGIONS_BOOST_FACTOR
from parameters import ATLAS_MINE_BONUS, EXPECTED_ATLAS_AUM, MAX_HARVESTER_PARTS, MAX_EXTRACTORS
from parameters import MIN_LEGIONS, MAX_LEGIONS
from parameters import AUM_CAP_HARVESTER
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS

from harvester_boost_count import total_harvester_boost


class UtilizationMiddleman:
    """
        # Middleman
        * Implements Peita's math to calculate current rewards for each harvester and atlas mine
        * Takes for account utilization of each harvester
        * If harvester has utilization below 100%, its “leftover” rewards are distributed automatically to other harvesters
        * Pulls data of active harvesters directly from the factory to support Harvester disabling
        * Pulls rewards from MasterOfCoin
        * That way one can easily budget the amount of rewards in bulk for Harvesters and Atlas Mine in MasterOfCoin
             and outsource heavy lifting of dynamic calculations and distribution to Middleman.
    """

    def __init__(self, master_of_coin, harvester_factory):
        self.master_of_coin = master_of_coin
        self.harvester_factory = harvester_factory
        self.magic_balance = 0
        # pull magic emission from MasterOfCoin
        self.pull_magic_from_master_of_coin()

        atlas_mine = harvester_factory.atlas_mine
        self.atlas_emission_share = 1
        self.harvester_emission_shares = []

    def __repr__(self):
        # pull data from HarvesterFactory first and update
        self.recalculate_emission_shares()

        boosts = self.calculate_harvester_boosts()
        atlas_boost = boosts[0]
        harvesters_boosts = boosts[1]

        return """
        ========== Utilization Middleman ==========
        Magic Balance in Middleman Contract: {balance:,} MAGIC

        Atlas Emission Share: {atlas_emissions_share:.2%}
        Active Harvesters Emission Shares: {h_emissions_share}

        Atlas Boost: {atlas_boost:.2f}x
        Harvesters Boosts: {h_boosts}

        """.format(
            balance=self.magic_balance,
            atlas_emissions_share=self.atlas_emission_share,
            h_emissions_share=[
                "{}: {:.2%}".format(s['id'], s['emission_share'])
                for s in self.harvester_emission_shares
            ],
            atlas_boost=atlas_boost,
            h_boosts=["{:.2f}x".format(b) for b in harvesters_boosts],
        )

    def pull_magic_from_master_of_coin(self):
        ## pulls the year 1 emissions from MasterOfCoin
        self.magic_balance += self.master_of_coin.get_emissions_for_bridgeworld(year=1)


    def calculate_harvester_boosts(self):
        # Pulls data of active harvesters directly from the factory
        atlas_mine = self.harvester_factory.atlas_mine

        # uses boost calculates from harvester_boost_count.py
        atlas_boost = total_harvester_boost(
            num_parts=atlas_mine.parts,
            num_legions=atlas_mine.legions,
            avg_legion_rank=atlas_mine.avg_legion_rank,
            extractors=atlas_mine.extractors,
            is_atlas=True
        )

        harvester_boosts = [
            total_harvester_boost(
                num_parts=h.parts,
                num_legions=h.legions,
                avg_legion_rank=h.avg_legion_rank,
                extractors=h.extractors,
            )
            if h.is_active else 0
            for h in self.harvester_factory.harvesters
        ]

        return (
            atlas_boost,
            harvester_boosts,
        )


    def mining_power_based_on_utilization(self, util=0):
        # Same math as solidity contract function: getRealMagicReward()
        if util < 0.3:
            # if utilization < 30%, no emissions
            return 0
        elif util < 0.4:
            # if 30% < utilization < 40%, 50% emissions
            return 0.5
        elif util < 0.5:
            # if 40% < utilization < 50%, 60% emissions
            return 0.6
        elif util < 0.6:
            # if 50% < utilization < 60%, 80% emissions
            return 0.8
        else:
            # 100% emissions above 60% utilization
            return 1


    def recalculate_emission_shares(self):
        #################################################
        ### 1. Calculate Mining Power for each ACTIVE mine
        #################################################

        # mining_power_based_on_utilization() returns a number between [0, 1]
        # then boost it according to their parts + legions + extractors
        atlas_mine = self.harvester_factory.atlas_mine
        atlas_mining_power = self.mining_power_based_on_utilization(atlas_mine.utilization)

        atlas_boosted_mining_power = atlas_mining_power * atlas_mine.getMiningBoost()

        harvester_mining_powers = [
            {
                'id': "h{}".format(h['id']),
                'mining_power': self.mining_power_based_on_utilization(h.utilization) * h.getMiningBoost()
                ## return a percent with getMiningBoost()
                ## such that sum of all the boosts is 1
                ##
            }
            for h in self.harvester_factory.harvesters
            if h.is_active
        ]
        ## if a mine gets disabled, does it's AUM automatically affect Atlas's utilization?
        ## or only when users withdraw? (it is currently like this, probably better this way)

        total_mining_power = atlas_boosted_mining_power + np.sum([h['mining_power'] for h in harvester_mining_powers])


        ### how to remove this loop above
        ## total_mining_power is a parameter that is pre-calculated by MasterOfCoin
        ## just need to get the individual harvester's mining power
        ## without loopin
        ## can we do this in a single loop

        ## loops are dangerous


        #################################################
        ### 2. Calculate share of emissions for each mine
        #################################################
        emissions_pct_share_atlas = atlas_boosted_mining_power / total_mining_power

        emissions_pct_shares = [
            {
                'id': p['id'],
                'emission_share': p['mining_power'] / total_mining_power
            }
            for p in harvester_mining_powers
        ]

        self.atlas_emission_share = emissions_pct_share_atlas
        self.harvester_emission_shares = emissions_pct_shares

        return (
            emissions_pct_share_atlas,
            emissions_pct_shares,
        )


    # Only used in plotting, ignore for solidity implementation
    def _calculate_user_pct_shares(self,
        expected_atlas_aum=EXPECTED_ATLAS_AUM,
        num_mil_user_stakes=1, # 1mil
    ):
        #################################################
        ### Calculate a user's share of total emission inside different mines
        #################################################
        # a user's share of total emission, staying inside Atlas mine, vs. another Harvester
        # ASSUMING the user has no individual-level boosts (e.g timeLock boost, etc)

        ( emissions_pct_share_atlas, emissions_pct_shares ) = self.recalculate_emission_shares()

        user_pct_share_atlas = num_mil_user_stakes/expected_atlas_aum  * emissions_pct_share_atlas
        user_pct_shares = [
            num_mil_user_stakes/AUM_CAP_HARVESTER * emissions_pct_share['emission_share']
            for emissions_pct_share in emissions_pct_shares
        ]
        print("user_pct_shares ", user_pct_shares )

        return (
            user_pct_share_atlas,
            user_pct_shares,
        )







# def _debug_print_harvester_splits(
#     debug=True,
#     harvesters=[],
#     harvester_boosts=[],
#     atlas_boost=1,
#     user_pct_share_atlas=0,
#     emissions_pct_share_atlas=0,
#     emissions_pct_shares=[],
#     user_pct_shares=[],
#     num_mil_user_stakes=0,
# ):
#     ### For printing only
#     if debug:
#         # harvester params
#         for i, harvester in enumerate(harvesters):
#             j = i + 1
#             parts = harvester['parts']
#             legions = harvester['legions']
#             avg_legion_rank = harvester['avg_legion_rank']
#             extractors = harvester['extractors']
#             members = legions / 3 # 3 legions per user
#             print("\n\n============================================\n\n")
#             print("Harv_{} has {} parts, {} total legions\n".format(j, parts, legions))

#         # boosts
#         print("Atlas gets:\t{:.2f}x boost".format(atlas_boost))
#         for i, boost in enumerate(harvester_boosts):
#             j = i + 1
#             print("Harv_{} gets:\t{:.2f}x boost\n".format(j, boost))

#         # emission shares/splits
#         print("Atlas gets:\t{:.2%} of emissions".format(emissions_pct_share_atlas))
#         for i, emissions_pct_share_harvester in enumerate(emissions_pct_shares):
#             j = i + 1
#             print("Harv_{} gets:\t{:.2%} of emissions\n".format(j, emissions_pct_share_harvester))

#         # user shares of emissions
#         print("For a whale with {} mil:".format(num_mil_user_stakes))
#         print("being in Atlas with {AUM}m AUM gives you:\t 1/{AUM} * {MINE_PCT:.4f} = {USER_PCT:.2%} of emissions".format(
#             AUM=EXPECTED_ATLAS_AUM ,
#             MINE_PCT=emissions_pct_share_atlas,
#             USER_PCT=user_pct_share_atlas
#         ))
#         for i, pct_share in enumerate(zip(emissions_pct_shares, user_pct_shares)):
#             j = i + 1
#             (emissions_pct_share, user_pct_share) = pct_share
#             print("{millions}m in Harvester_{j} with {AUM_CAP}m AUM gives you:\t 1/{AUM_CAP} * {MINE_PCT:.4f} = {USER_PCT:.2%}".format(
#                 millions=num_mil_user_stakes,
#                 j=j,
#                 AUM_CAP=AUM_CAP_HARVESTER,
#                 MINE_PCT=emissions_pct_share,
#                 USER_PCT=user_pct_share
#             ))
#             print("\nA whale can get a {:.2%} / {:.2%}\n= {:.2f}x improvement in yield".format(
#                 user_pct_share,
#                 user_pct_share_atlas,
#                 user_pct_share / user_pct_share_atlas
#             ))
#             print("for collecting {:.0f} harvester parts, a guild of {:.0f} users, {:.0f} legions".format(parts, members, legions))
#             print("\nNOTE 1: Assumes he can deploy his full amount in the {}m cap harvester".format(AUM_CAP_HARVESTER))
#             print("NOTE 2: Yield may be MUCH, MUCH higher initially before the {}m cap is reached".format(AUM_CAP_HARVESTER))



