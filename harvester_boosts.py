import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

# parameters for configuring boosts
from parameters import PARTS_BOOST_FACTOR, LEGIONS_BOOST_FACTOR
from parameters import ATLAS_MINE_BONUS, EXPECTED_ATLAS_AUM, MAX_HARVESTER_PARTS, MAX_EXTRACTORS
from parameters import MIN_LEGIONS, MAX_LEGIONS
from parameters import TIME_LOCK_BOOST_PARAMS, LEGION_BOOST_PARAMS, LEGION_RANK_PARAMS
from parameters import EXTRACTOR_BOOST_PARAMS, TREASURES_BOOST_PARAMS



def get_treasure_boost(name, boost=3):
    """
        Gets each treasures mining boost, default is multiplied by 3

        boost: adjustable boost parameter for devs to scale the boost
        treasures have when stacking them in the mine
    """
    return treasures_boost_params[name] * boost



def parts_boost_harvester(num_parts, max_parts=MAX_HARVESTER_PARTS, boost_factor=PARTS_BOOST_FACTOR):
    """
        quadratic function in the interval: [1, (1 + boost_factor)] based on number of parts staked.
        exhibits diminishing returns on boosts as more parts are added

        num_parts: number of harvester parts
        max_parts: number of parts to achieve max boost

        boost_factor: the amount of boost you want to apply to parts
        default is 1 = 100% boost (2x) if num_parts = max_parts
    """
    # weight for additional parts has  diminishing gains
    n = num_parts
    return 1 + (2*n - n**2/max_parts) / max_parts * boost_factor



def legions_boost_harvester(num, max=MAX_LEGIONS, avg_legion_rank=1, boost_factor=LEGIONS_BOOST_FACTOR):
    """
        quadratic function in the interval: [1, (1 + boost_factor)] based on number of parts staked.
        exhibits diminishing returns on boosts as more legions are added

        num: number of legions staked on harvester
        max: number of legions where you achieve max boost
        avg_legion_rank: avg legion rank on your harvester

        boost_factor: the amount of boost you want to apply to parts
        default is 1 = 50% boost (1.5x) if num = max
    """

    # if over max, treat as if you have max legions
    if num > max:
        n = max
    else:
        n = num

    legion_rank_modifier = (0.90 + avg_legion_rank/10)
    # if avg rank is commons (rank 1),
    # then 0.9 + 1/10 = 1 so there is no boost

    return 1 + (2*n - n**2/max) / max * legion_rank_modifier * boost_factor



def extractors_boost_harvester(extractors, max_extractors=MAX_EXTRACTORS):
    """
        extractors: ['small_extractor', 'medium_extractor', 'large_extractor']
        max_extractors: maximum number of extractors effective at any point in time
    """

    # assert len(extractors) <= max_parts
    ## don't assert extractor length, allow people to accidentally apply and waste
    ## their extractor boost if they are not careful

    # take the first 5 extractor boosts
    top_five_extractors = extractors[:5]

    extractors_boost = 0
    for d in top_five_extractors:
        dboost = EXTRACTOR_BOOST_PARAMS[d]
        extractors_boost += dboost

    return 1 + extractors_boost



def calculate_avg_legion_rank(legions):
    """
        Calculates the avg rank of a group of legions. Used to determine the avg legion rank of
        legions staked on a harvester.
        Example function call:
            calculate_avg_legion_rank(['gen0_common', 'gen0_common', 'gen0_1_1', 'gen0_rare'])

        legions: ['gen0_common', 'gen1_common', 'gen0_special']
    """
    summed_rank = 0
    for l in legions:
        legion_rank = LEGION_RANK_PARAMS[l]
        summed_rank += legion_rank

    avg_rank = summed_rank / len(legions)
    return avg_rank



def total_harvester_boost(num_parts, num_legions, extractors=[], avg_legion_rank=1, is_atlas=False):
    """calculates both parts_boost * legions_boost together"""

    modifier_legions_boost = legions_boost_harvester(num_legions, MAX_LEGIONS, avg_legion_rank)
    modifier_parts_boost = parts_boost_harvester(num_parts)
    modifier_extractors_boost = extractors_boost_harvester(extractors)

    if (is_atlas) :
        return modifier_legions_boost * modifier_parts_boost * modifier_extractors_boost * ATLAS_MINE_BONUS
    else:
        return modifier_legions_boost * modifier_parts_boost * modifier_extractors_boost



def user_boost_inside_harvester(time_lock_deposit='none', legions=[], treasures=[]):
    """
        Calculates the boost on user's deposit size inside the harvester

        params:
        time_lock_deposits: "none" | "2_weeks" | "1_month" | "3_months" | "6_months"
        legions: ['gen0_common', 'gen0_rare', 'gen0_uncommon']
        treasures: ['honeycomb', 'grin']
    """

    assert len(legions) <= 3
    assert len(treasures) <= 20

    ##### Time lock Boost
    try:
        time_lock_boost = TIME_LOCK_BOOST_PARAMS[time_lock_deposit]
    except KeyError:
        time_lock_boost = TIME_LOCK_BOOST_PARAMS['none']


    ##### Legion Boost
    legions_boost = 0
    for l in legions:
        # additively sum the boosts
        legions_boost += LEGION_BOOST_PARAMS[l]
        # errors if key in dict not found

    ##### Treasures Boost
    treasures_boost = 0
    for t in treasures:
        treasures_boost += get_treasure_boost(name=t, boost=3)

    total_boost = 1 + time_lock_boost + legions_boost + treasures_boost

    print("time_lock_boost: ", time_lock_boost)
    print("legions_boost: ", legions_boost)
    print("treasures_boost: ", treasures_boost)
    print("total_boost: ", total_boost)

    return total_boost


## Example: calling the function
# user_boost_inside_harvester(
#     '2_weeks',
#     legions=['gen0_common', 'gen0_uncommon', 'gen0_rare'],
#     treasures=['honeycomb', 'grin'],
# )
## Example 2: (matches example in Alex's excel)
# user_boost_inside_harvester(
#     '6_months',
#     legions=['gen0_rare', 'gen0_rare', 'gen0_1_1'],
#     treasures=[
#        'honeycomb', 'honeycomb', 'honeycomb', 'honeycomb', 'honeycomb', 'honeycomb', 'honeycomb',
#        'grin',
#        'bottomless_elixir', 'bottomless_elixir', 'bottomless_elixir',
#        'cap_of_invisibility', 'cap_of_invisibility', 'cap_of_invisibility', 'cap_of_invisibility',
#        'ancient_relic', 'ancient_relic',
#        'castle',
#        'thread_of_divine_silk', 'thread_of_divine_silk',
#     ],
# )

# user_boost_inside_harvester(
#     '2_weeks',
#     legions=['gen0_rare', 'gen0_rare'],
#     treasures=['honeycomb', 'honeycomb', 'honeycomb'],
# )











