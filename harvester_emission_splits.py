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

from harvester_boosts import total_harvester_boost



def calculate_harvester_splits(
    harvesters=[],
    expected_atlas_aum=EXPECTED_ATLAS_AUM,
    debug=True,
    num_mil_user_stakes=1, # 1mil
    # num_mil_user_stakes=0.1, # 100k
    ):

    #################################################
    ### 1. Calculate harvester boosts
    #################################################
    atlas_boost = total_harvester_boost(
        num_parts=0,
        num_legions=0,
        avg_legion_rank=1,
        extractors=[],
        is_atlas=True
    )
    harvester_boosts = [
        total_harvester_boost(
            num_parts=h['parts'],
            num_legions=h['legions'],
            avg_legion_rank=h['avg_legion_rank'],
            extractors=h['extractors'],
        )
        if h.is_active
        else 0
        for h in harvesters
    ]

    #################################################
    ### 2. Calculate Mining Power for each mine
    #################################################
    # Set each mine at 100 mining power to begin with
    # then boost it according to their parts + legions + extractors
    atlas_mining_power = atlas_boost * 100
    harvester_mining_powers = [hboost * 100 for hboost in harvester_boosts]
    total_mining_power = atlas_mining_power + np.sum(harvester_mining_powers)


    #################################################
    ### 3. Calculate share of emissions for each mine
    #################################################
    mine_pct_share_atlas = atlas_mining_power / total_mining_power
    mine_pct_shares = [p/total_mining_power for p in harvester_mining_powers]


    #################################################
    ### 4. Calculate a user's share of total emission inside different mines
    #################################################
    # a user's share of total emission, staying inside Atlas mine, vs. another Harvester
    # ASSUMING the user has no individual-level boosts (e.g timeLock boost, etc)
    user_pct_share_atlas = num_mil_user_stakes/expected_atlas_aum  * mine_pct_share_atlas
    user_pct_shares = [
        num_mil_user_stakes/AUM_CAP_HARVESTER * mine_pct_share
        for mine_pct_share in mine_pct_shares
    ]


    _debug_print_harvester_splits(
        debug=True,
        harvesters=harvesters,
        harvester_boosts=harvester_boosts,
        atlas_boost=atlas_boost,
        user_pct_share_atlas=user_pct_share_atlas,
        mine_pct_share_atlas=mine_pct_share_atlas,
        mine_pct_shares=mine_pct_shares,
        user_pct_shares=user_pct_shares,
        num_mil_user_stakes=num_mil_user_stakes,
    )


    return (
        atlas_boost,
        mine_pct_share_atlas,
        user_pct_share_atlas,
        harvester_boosts,
        mine_pct_shares,
        user_pct_shares,
    )



def _debug_print_harvester_splits(
    debug=True,
    harvesters=[],
    harvester_boosts=[],
    atlas_boost=1,
    user_pct_share_atlas=0,
    mine_pct_share_atlas=0,
    mine_pct_shares=[],
    user_pct_shares=[],
    num_mil_user_stakes=0,
):
    ### For printing only
    if debug:
        # harvester params
        for i, harvester in enumerate(harvesters):
            j = i + 1
            parts = harvester['parts']
            legions = harvester['legions']
            avg_legion_rank = harvester['avg_legion_rank']
            extractors = harvester['extractors']
            members = legions / 3 # 3 legions per user
            print("\n\n============================================\n\n")
            print("Harv_{} has {} parts, {} total legions\n".format(j, parts, legions))

        # boosts
        print("Atlas gets:\t{:.2f}x boost".format(atlas_boost))
        for i, boost in enumerate(harvester_boosts):
            j = i + 1
            print("Harv_{} gets:\t{:.2f}x boost\n".format(j, boost))

        # emission shares/splits
        print("Atlas gets:\t{:.2%} of emissions".format(mine_pct_share_atlas))
        for i, mine_pct_share_harvester in enumerate(mine_pct_shares):
            j = i + 1
            print("Harv_{} gets:\t{:.2%} of emissions\n".format(j, mine_pct_share_harvester))

        # user shares of emissions
        print("For a whale with {} mil:".format(num_mil_user_stakes))
        print("being in Atlas with {AUM}m AUM gives you:\t 1/{AUM} * {MINE_PCT:.4f} = {USER_PCT:.2%} of emissions".format(
            AUM=EXPECTED_ATLAS_AUM ,
            MINE_PCT=mine_pct_share_atlas,
            USER_PCT=user_pct_share_atlas
        ))
        for i, pct_share in enumerate(zip(mine_pct_shares, user_pct_shares)):
            j = i + 1
            (mine_pct_share, user_pct_share) = pct_share
            print("{millions}m in Harvester_{j} with {AUM_CAP}m AUM gives you:\t 1/{AUM_CAP} * {MINE_PCT:.4f} = {USER_PCT:.2%}".format(
                millions=num_mil_user_stakes,
                j=j,
                AUM_CAP=AUM_CAP_HARVESTER,
                MINE_PCT=mine_pct_share,
                USER_PCT=user_pct_share
            ))
            print("\nA whale can get a {:.2%} / {:.2%}\n= {:.2f}x improvement in yield".format(
                user_pct_share,
                user_pct_share_atlas,
                user_pct_share / user_pct_share_atlas
            ))
            print("for collecting {:.0f} harvester parts, a guild of {:.0f} users, {:.0f} legions".format(parts, members, legions))
            print("\nNOTE 1: Assumes he can deploy his full amount in the {}m cap harvester".format(AUM_CAP_HARVESTER))
            print("NOTE 2: Yield may be MUCH, MUCH higher initially before the {}m cap is reached".format(AUM_CAP_HARVESTER))



