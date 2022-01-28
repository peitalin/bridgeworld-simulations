import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

# parameters for configuring boosts
from parameters import PARTS_BOOST_FACTOR, LEGIONS_BOOST_FACTOR
from parameters import ATLAS_MINE_BONUS, ATLAS_AUM, MAX_HARVESTER_PARTS, MAX_EXTRACTORS
from parameters import MIN_LEGIONS, MAX_LEGIONS
from parameters import AUM_CAP_HARVESTER
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS

from harvester_boosts import total_harvester_boost


atlas = {
    'parts': 20,
    # legions: 200,
    # avg_legion_rank: 1,
}

# harvester1 = {
#     'parts': 20,
#     'legions': 200,
#     'avg_legion_rank': 1,
#     'extractors': [],
# }


# def calculate_harvester_splits():


def compare_harvester_yield(harvesters=[], debug=True):

    EXPECTED_AUM_ATLAS = ATLAS_AUM # 60mil in atlas mine, about 80% supply staked
    AUM_CAP_HARVESTER = 10 # 10mil cap in harvesters

    # num_millions_user_stakes = 0.01 # 10k
    num_millions_user_stakes = 1 # 1mil

    harvester_boosts = []

    for harvester in harvesters:

        parts = harvester['parts']
        legions = harvester['legions']
        avg_legion_rank = harvester['avg_legion_rank']
        extractors = harvester['extractors']
        members = legions / 3 # 3 legions per user

        boost = total_harvester_boost(num_parts=parts, num_legions=legions,
            # extractors=['large_extractor','large_extractor','large_extractor','large_extractor','large_extractor'],
            extractors=[],
            avg_legion_rank=avg_legion_rank
        )
        harvester_boosts.append(boost)

    # original atlas mine is treated as a harvester with uncapped AUM
    # it has 0 harvester parts to begin with,
    boost_atlas = total_harvester_boost(num_parts=0, num_legions=0, extractors=[], avg_legion_rank=1, is_atlas=True)


    harvester_points = []
    # set harvester base points = 100
    atlas_points = boost_atlas * 100

    for boost in harvester_boosts:
        hpoints = boost * 100
        harvester_points.append(hpoints)

    points_total = atlas_points + np.sum(harvester_points)

    # Calculate percentage share of total emissions split between Atlas and Harvester 1
    mine_pct_share_atlas = atlas_points / points_total

    mine_pct_shares = []
    for i, p in enumerate(harvester_points):
        mine_pct_share_harvester = p / points_total
        mine_pct_shares.append(mine_pct_share_harvester)

    # a user's share of total emission, staying inside Atlas mine, vs. Harvester 1
    user_pct_share_atlas = num_millions_user_stakes/EXPECTED_AUM_ATLAS * mine_pct_share_atlas
    user_pct_shares = []
    for i, mine_pct_share in enumerate(mine_pct_shares):
        user_pct_share = num_millions_user_stakes/AUM_CAP_HARVESTER * mine_pct_share
        user_pct_shares.append(user_pct_share)



    if debug:
        # harvester params
        for i, harvester in enumerate(harvesters):
            parts = harvester['parts']
            legions = harvester['legions']
            avg_legion_rank = harvester['avg_legion_rank']
            extractors = harvester['extractors']
            members = legions / 3 # 3 legions per user
            print("\n============================================")
            print("Harvester {} has:")
            print("{} parts, {} total legions\n".format(i, parts, legions))


        # boosts
        print("Atlas gets:\t{:.2f}x boost".format(boost_atlas))
        for i, boost in enumerate(harvester_boosts):
            print("Harvester_{} gets:\t{:.2f}x boost\n".format(i, boost))


        # emission shares/splits
        print("Atlas gets:\t{:.2%} of emissions".format(mine_pct_share_atlas))
        for i, p in enumerate(harvester_points):
            print("Harv_{} gets:\t{:.2%} of emissions\n".format(i, mine_pct_share_harvester))


        print("For a whale with {} mil:".format(num_millions_user_stakes))
        print("being in Atlas with {AUM}m AUM gives you:\t 1/{AUM} * {MINE_PCT:.4f} = {USER_PCT:.2%} of emissions".format(
            AUM=EXPECTED_AUM_ATLAS,
            MINE_PCT=mine_pct_share_atlas,
            USER_PCT=user_pct_share_atlas
        ))

        for i, mine_pct_share in enumerate(mine_pct_shares):
            print("{millions}m in Harvester_{i} with 10m AUM gives you:\t 1/{AUM_CAP} * {MINE_PCT:.4f} = {USER_PCT:.2%}".format(
                millions=num_millions_user_stakes,
                i=i,
                AUM_CAP=AUM_CAP_HARVESTER,
                MINE_PCT=mine_pct_share,
                USER_PCT=user_pct_share
            ))
            print("\nAn entrepreneurial whale can potentially get a {:.2%} / {:.2%}\n= {:.2f}x improvement in yield".format(
                user_pct_share,
                user_pct_share_atlas,
                user_pct_share / user_pct_share_atlas
            ))
            print("for collecting {} harvester parts, a guild of {} users, {} legions".format(parts, members, legions))
            print("\nNote: assumes he can deploy his full amount in the 10m cap harvester")
            print("he will get an even better yield initially before the 10m cap is reached")

    return (
        boost_atlas,
        mine_pct_share_atlas,
        user_pct_share_atlas,
        harvester_boosts,
        mine_pct_shares,
        user_pct_shares,
    )





