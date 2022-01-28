import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

# parameters for configuring boosts
from parameters import PARTS_BOOST_FACTOR, LEGIONS_BOOST_FACTOR
from parameters import ATLAS_MINE_BONUS, ATLAS_AUM, MAX_HARVESTER_PARTS, MAX_EXTRACTORS
from parameters import MIN_LEGIONS, MAX_LEGIONS
from parameters import AUM_CAP_HARVESTER,
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS

from harvester_boosts import total_harvester_boost


harvester1 = {
    parts: 20,
    legions: 200,
    avg_legion_rank: 1,
}


# def calculate_harvester_splits():


def compare_harvester_yield(parts=20, members=20, atlas_parts=0, debug=True):

    EXPECTED_AUM_ATLAS = ATLAS_AUM # 60mil in atlas mine, about 80% supply staked
    AUM_CAP_HARVESTER = 10 # 10mil cap in harvesters
    avg_legion_rank = 1
    num_legions = members * 3 # 3 legions max per user

    # num_millions_user_stakes = 0.01 # 10k
    num_millions_user_stakes = 1 # 1mil

    if debug:
        print("\n============================================")
        print("Harvester_1 has:")
        print("{} parts, {} total legions\n".format(parts, members*3))

    boost_h1 = total_harvester_boost(num_parts=parts, num_legions=num_legions,
        # extractors=['large_extractor','large_extractor','large_extractor','large_extractor','large_extractor'],
        extractors=[],
        avg_legion_rank=avg_legion_rank
    )
    # original atlas mine is treated as a harvester with uncapped AUM
    # it has 0 harvester parts to begin with, and can have up to 2000 staked legions to boost its mining (avg legion rank 1)
    boost_atlas = total_harvester_boost(num_parts=atlas_parts, num_legions=2000, extractors=[], avg_legion_rank=1, is_atlas=True) # 6x boost by default
    if debug:
        print("Atlas gets:\t{:.2f}x boost".format(boost_atlas))
        print("Harv_1 gets:\t{:.2f}x boost\n".format(boost_h1))

    # set harvester base points = 100
    points_atlas = boost_atlas * 100
    points_h1    = boost_h1 * 100
    points_total = points_atlas + points_h1

    # Calculate percentage share of total emissions split between Atlas and Harvester 1
    mine_pct_share_atlas = points_atlas / points_total
    mine_pct_share_h1 = points_h1 / points_total
    if debug:
        print("Atlas gets:\t{:.2%} of emissions".format(mine_pct_share_atlas))
        print("Harv_1 gets:\t{:.2%} of emissions\n".format(mine_pct_share_h1))

    # a user's share of total emission, staying inside Atlas mine, vs. Harvester 1
    user_pct_share_atlas = num_millions_user_stakes/EXPECTED_AUM_ATLAS * mine_pct_share_atlas
    user_pct_share_h1 = num_millions_user_stakes/10 * mine_pct_share_h1
    if debug:
        print("For a whale with 1mil:")
        print("1m in Atlas with {AUM}m AUM gives you:\t 1/{AUM} * {MINE_PCT:.4f} = {USER_PCT:.2%} of emissions".format(
            AUM=EXPECTED_AUM_ATLAS,
            MINE_PCT=mine_pct_share_atlas,
            USER_PCT=user_pct_share_atlas
        ))
        print("1m in Harv_1 with 10m AUM gives you:\t 1/{AUM_CAP} * {MINE_PCT:.4f} = {USER_PCT:.2%}".format(
            AUM_CAP=AUM_CAP_HARVESTER,
            MINE_PCT=mine_pct_share_h1,
            USER_PCT=user_pct_share_h1
        ))
        print("\nAn entrepreneurial whale can potentially get a {:.2%} / {:.2%}\n= {:.2f}x improvement in yield".format(
            user_pct_share_h1,
            user_pct_share_atlas,
            user_pct_share_h1 / user_pct_share_atlas
        ))
        print("for collecting {} harvester parts, a guild of {} users, {} legions".format(parts, members, members*3))
        print("\nNote: assumes he can deploy his full 1m in the 10m cap harvester 1 alongside other guild members")
        print("he will get an even better yield initially before the 10m cap is reached")

    return (
        boost_h1,
        boost_atlas,
        mine_pct_share_h1,
        mine_pct_share_atlas,
        user_pct_share_h1,
        user_pct_share_atlas,
    )





