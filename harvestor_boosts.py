
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

# x-axis data points
x_parts = np.linspace(0, 500, 501) # 1 to 500 parts
x_legions = np.linspace(0, 3000, 3001) # 1 to 3000 legions

# for devs/team to calibrate
PARTS_BOOST_FACTOR = 1
LEGIONS_BOOST_FACTOR = 0.5
# parts boost maxes out at 100%
# legions boosts max out at 50% boost
# they stack together to determine overall boost
# parts_boost should probably be bigger than legions (as a craft item)
ATLAS_MINE_BONUS = 2
ATLAS_AUM = 80
# atlas mine gets a default 5x boost
# (generally it will have a much larger AUM than other harvesters, 50mil~80mil vs 10mil)

min_legions = 1
max_legions = 2000
# legions boosts maxes out at 2000 staked legions

time_lock_boost_params = dict({
    'none': 0, # 0% bonus
    '2_weeks': 0.1, # 10%
    '1_month': 0.25, # 25%
    '3_months': 0.80, # 80%
    '6_months': 1.8, # 180%
    '12_months': 4, # 400%
})

legion_boost_params = dict({
    'gen0_common': 0.5, # commons
    'gen0_special': 0.75, # includes riverman, Numeraire 50%
    'gen0_uncommon': 1, # Assasin etc 100%
    'gen0_rare': 2, # all-class 200%
    'gen0_1_1': 6, # 1/1 600%
    'gen1_common': 0.05, # 5%
    'gen1_uncommon': 0.1, # 10%
    'gen1_rare': 0.25, # 25%
})

legion_rank_params = dict({
    'gen0_common': 1, # commons
    'gen0_special': 2, # includes riverman, Numeraire 50%
    'gen0_uncommon': 3, # Assasin etc 100%
    'gen0_rare': 4, # all-class 200%
    'gen0_1_1': 5,  # 1/1
    'gen1_common': 1,
    'gen1_uncommon': 2,
    'gen1_rare': 3,
})


def get_treasure_boost(name, boost=3):
    """
        get treasure boost, default multiplied by 3
        boost: adjustable boost parameter for devs to scale the boost
        treasures have when stacking them in the mine
    """
    return treasures_boost_params[name] * boost

treasures_boost_params = dict({
    # buffed honeycomb + grin by 2x
    "honeycomb":	0.02631*2,
    "grin":	0.02619*2,
    "bottomless_elixir":	0.02536,
    "cap_of_invisibility":	0.02536,
    "ancient_relic":	0.02508,
    "castle":	0.02443,
    "thread_of_divine_silk":	0.02443,
    "mollusk_shell":	0.02240,
    "bait_for_monsters":	0.02433,
    "immovable_stone":	0.02412,
    "snow_white_feather":	0.02134,
    "red_feather":	0.02126,
    "ivory_breastpin":	0.02122,
    "divine_hourglass":	0.02114,
    "military_stipend":	0.02076,
    "bag_of_rare_mushrooms":	0.02053,
    "carriage":	0.02024,
    "small_bird":	0.01995,
    "score_of_ivory":	0.01985,
    "unbreakable_pocketwatch":	0.01978,
    "framed_butterfly":	0.01947,
    "cow":	0.01934,
    "pot_of_gold":	0.01930,
    "divine_mask":	0.01904,
    "common_bead":	0.01879,
    "favor_from_the_gods":	0.01848,
    "jar_of_fairies":	0.01776,
    "witches_broom":	0.01691,
    "common_feather":	0.01126,
    "green_rupee":	0.01090,
    "grain":	0.01073,
    "lumber":	0.01006,
    "common_relic":	0.00718,
    "ox":	0.00529,
    "blue_rupee":	0.00509,
    "donkey":	0.00406,
    "half-penny":	0.00262,
    "silver_coin":	0.00261,
    "diamond":	0.00260,
    "pearl":	0.00258,
    "dragon_tail":	0.00257,
    "red_rupee":	0.00257,
    "gold_coin":	0.00256,
    "emerald":	0.00253,
    "beetle_wing":	0.00251,
    "quarter_penny":	0.00250,
})

drill_boost_params = dict({
    'small_extractor': 0.15, #  15%
    'medium_extractor': 0.20, # 20%
    'large_extractor': 0.25, # 25%
})







def parts_boost_harvester(num_parts, max_parts=500, boost_factor=PARTS_BOOST_FACTOR):
    """
        quadratic function in the interval: [1, (1 + boost_factor)] based on number of parts staked.

        num_parts: number of harvestor parts
        max_parts: number of parts to achieve max boost

        boost_factor: the amount of boost you want to apply to parts
        default is 1 = 100% boost (2x) if num_parts = max_parts
    """
    # weight for additional parts has  diminishing gains
    n = num_parts
    return 1 + (2*n - n**2/max_parts) / max_parts * boost_factor



def legions_boost_harvester(num, max=500, avg_legion_rank=1, boost_factor=LEGIONS_BOOST_FACTOR):
    """
        quadratic function in the interval: [1, (1 + boost_factor)] based on number of parts staked.
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



def drill_boost_harvester(drills, max_parts=5):
    """
        drills: ['small_extractor', 'medium_extractor', 'large_extractor']
        max_parts: number of drill bits to achieve max boost
    """
    assert len(drills) <= max_parts

    drills_boost = 0
    for d in drills:
        dboost = drill_boost_params[d]
        drills_boost += dboost

    return 1 + drills_boost


def total_harvester_boost(num_parts, num_legions, drills=[], avg_legion_rank=1, is_atlas=False):
    """calculates both parts_boost * legions_boost together"""

    modifier_legions_boost = legions_boost_harvester(num_legions, max_legions, avg_legion_rank)
    modifier_parts_boost = parts_boost_harvester(num_parts)
    modifier_drills_boost = drill_boost_harvester(drills)

    if (is_atlas) :
        return modifier_legions_boost * modifier_parts_boost * modifier_drills_boost * ATLAS_MINE_BONUS
    else:
        return modifier_legions_boost * modifier_parts_boost * modifier_drills_boost



def user_boost_inside_harvester(time_lock_deposit='none', legions=[], treasures=[]):
    """
        Calculates the boost on user's deposit size inside the harvester

        params:
        time_lock_deposits: "none" | "2_weeks" | "1_month" | "3_months" | "6_months"
        legions: ['gen0_common', 'gen0_rare', 'gen0_uncommon']
        treasures: ['honeycomb', 'grin']
        # consumables: ['small_extractor']
    """

    assert len(legions) <= 3
    # assert len(consumables) <= 5
    assert len(treasures) <= 20

    ##### Time lock Boost
    try:
        time_lock_boost = time_lock_boost_params[time_lock_deposit]
    except KeyError:
        time_lock_boost = time_lock_boost_params['none']


    ##### Legion Boost
    legions_boost = 0
    for l in legions:
        # additively sum the boosts
        legions_boost += legion_boost_params[l]
        # errors if key in dict not found

    ##### Treasures Boost
    treasures_boost = 0
    for t in treasures:
        treasures_boost += get_treasure_boost(name=t, boost=3)

    # ##### Consumables Boost
    # consumables_boost = 0
    # for c in consumables:
    #     consumables_boost += consumables_boost_params[c]

    total_boost = 1 + time_lock_boost + legions_boost + treasures_boost
        # + consumables_boost

    print("time_lock_boost: ", time_lock_boost)
    print("legions_boost: ", legions_boost)
    print("treasures_boost: ", treasures_boost)
    # print("consumables_boost: ", consumables_boost)
    print("total_boost: ", total_boost)

    return total_boost


## Example: calling the function
# user_boost_inside_harvester(
#     '2_weeks',
#     legions=['gen0_common', 'gen0_uncommon', 'gen0_rare'],
#     treasures=['honeycomb', 'grin'],
#     consumables=['small_extractor']
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
#     consumables=[
#         'small_extractor',
#         'medium_extractor', 'medium_extractor',
#         'large_extractor', 'large_extractor',
#     ]
# )

# user_boost_inside_harvester(
#     '2_weeks',
#     legions=['gen0_rare', 'gen0_rare'],
#     treasures=['honeycomb', 'honeycomb', 'honeycomb'],
#     consumables=[]
# )


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
        legion_rank = legion_rank_params[l]
        summed_rank += legion_rank

    avg_rank = summed_rank / len(legions)
    print("avg_rank", avg_rank)
    return avg_rank











#################################
####### PLOTS
#################################

################ Varying legion numbers, fixed parts
def graph_total_harvester_boost_varying_legions():

    x1_num_parts = np.linspace(0,500,501)
    x2_num_legions = np.linspace(0,2000,501)

    total_boosted_max_hi_legion_rank = [total_harvester_boost(500, x2, [], 4) for x2 in x2_num_legions]
    total_boosted_max = [total_harvester_boost(500, x2, [], 1) for x2 in x2_num_legions]
    total_boosted_min = [total_harvester_boost(1, x2, [], 1)   for x2 in x2_num_legions]

    plt.plot(x2_num_legions, total_boosted_max_hi_legion_rank, label="Harvester with 500 parts; high legion rank", color="orange", linestyle=":")
    plt.plot(x2_num_legions, total_boosted_max, label="Harvester with 500 parts", color="orange", linestyle="-")
    plt.plot(x2_num_legions, total_boosted_min, label="Harvester with 1 part", color="orange", linestyle="--")
    # fill between upper and lower bound
    plt.fill_between(x2_num_legions, total_boosted_min, total_boosted_max, facecolor="orange", alpha=0.2)

    plt.xlabel("Number of legions staked")
    plt.ylabel("Emissions Boost (x)")
    plt.title("Harvester Emissions Boost (parts x legions boost)")
    plt.legend()
    plt.show()


# ###################################
# ###### Parts Boost Graph
# ###################################
def graph_parts_boost():
    parts_boosted = [parts_boost_harvester(x) for x in x_parts]

    plt.plot(parts_boosted)
    plt.xlabel("number of parts")
    plt.ylabel("Boost multiplier")
    plt.title("Harvester Parts Boost")
    plt.grid(color='black', alpha=0.1)
    plt.show()
    # the marginal contribution of each peice of harvestor part:
    # marginal_contribution = np.diff(parts_boosted)
    # starts at 2, then works it way down to 0
    # basically the first few parts count for 2, then steadily/linearly approachs 0 as we approach the 500th part

#################################
####### COMPARISON TO ATLAS MINE
#################################

# So I compared how boosts affect the split of emissions between the Atlas mine
# and auxiliary harvester.
#
# In the beginning there will only be 1 aux harvester, with low parts and legions
# over time, the harvester will get larger boosts (more parts + legions)
# and more harvesters may come online

# This section models out the early stages of when 1 or 2 harvesters come online
# and can be generalized for when more and more harvesters come online


# The Atlas mine will initially have 0 parts
# Atlas mine can have parts-boosts, maybe Governance votes for outperforming harvesters to
# "become the Atlas mine" where it'll retain the number of parts/boost
# In this instance the choice between staying in the Atlas mine, and creating another Harvester
# is ambiguous, sometimes its better to be in Atlas, but if you are entrepreneurial, starting another
# harvester may be better



### Example Emissions 1
def compare_harvester_yield(parts=20, members=20, atlas_parts=0, debug=True):

    EXPECTED_AUM_ATLAS = ATLAS_AUM # 80mil in atlas mine, about 80% supply staked
    AUM_CAP_HARVESTER = 10 # 10mil cap in harvesters
    avg_legion_rank = 1
    num_legions = members * 3 # 3 legions max per user

    # num_millions_user_stakes = 0.01 # 10k
    num_millions_user_stakes = 1 # 1mil

    if debug:
        print("\n============================================")
        print("Harvester_1 has:")
        print("{} parts, {} members, {} total legions\n".format(parts, members, members*3))

    boost_h1 = total_harvester_boost(num_parts=parts, num_legions=num_legions,
        # drills=['large_extractor','large_extractor','large_extractor','large_extractor','large_extractor'],
        drills=[],
        avg_legion_rank=avg_legion_rank
    )
    # original atlas mine is treated as a harvester with uncapped AUM
    # it has 0 harvester parts to begin with, and can have up to 2000 staked legions to boost its mining (avg legion rank 1)
    boost_atlas = total_harvester_boost(num_parts=atlas_parts, num_legions=2000, drills=[], avg_legion_rank=1, is_atlas=True) # 6x boost by default
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



## Atlas vs 1 Harvester
def plot_atlas_harvest_comparison_1(atlas_parts=0):

    ## Array of x-axis data points
    x_boost_h1 = []
    x_boost_atlas = []

    x_mine_pct_share_h1 = []
    x_mine_pct_share_atlas = []

    x_user_pct_share_h1 = []
    x_user_pct_share_atlas = []


    num_obs = 501
    _x_parts = np.linspace(0, 500, num_obs) # 1 to 500 parts
    _x_members = np.linspace(0, 666.66, num_obs) # 1 to 666 users, 666.6 users * 3 legions = 2000 legions


    for parts,members in zip(_x_parts, _x_members):

        (
            boost_h1,
            boost_atlas,
            mine_pct_share_h1,
            mine_pct_share_atlas,
            user_pct_share_h1,
            user_pct_share_atlas,
        ) = compare_harvester_yield(parts=parts, members=members, atlas_parts=atlas_parts, debug=True)

        x_boost_h1.append(boost_h1)
        x_boost_atlas.append(boost_atlas)
        x_mine_pct_share_h1.append(mine_pct_share_h1)
        x_mine_pct_share_atlas.append(mine_pct_share_atlas)
        x_user_pct_share_atlas.append(user_pct_share_atlas)
        x_user_pct_share_h1.append(user_pct_share_h1)

        # print("boost_h1: ", boost_h1)
        # print("boost_atlas: ", boost_atlas)
        # print("mine_pct_share_h1: ", mine_pct_share_h1)
        # print("mine_pct_share_atlas: ", mine_pct_share_atlas)
        print("user_pct_share_atlas: ", user_pct_share_atlas)
        print("user_pct_share_h1: ", user_pct_share_h1)


    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Emission Splits: Atlas vs. 1 Harvester')

    #### Plot 1
    ax1.plot(x_boost_h1, label="H1 boost ranges from 1x to {:.1f}x max".format(x_boost_h1[-1]))
    ax1.plot([], label="Atlas is {}x boost by default (configurable)".format(ATLAS_MINE_BONUS), color='red')
    ax1.set(xlabel='(parts, legions)', ylabel='Boost Multiplier')
    ax1.set_xticks([0, 100, 200, 300, 400, 500])
    ax1.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=7)
    ax1.set_title('Harvest Boost', size=9)
    ax1.legend()
    ax1.grid(color='black', alpha=0.1)

    #### Plot 2
    ax2.plot(x_mine_pct_share_h1, label="H1 Share")
    ax2.plot(x_mine_pct_share_atlas, label="Atlas Share", color='red')
    ax2.set(xlabel='Boost (x)', ylabel='% share of emissions')
    # plot 2 x-ticks
    boost_xticks = ["{:.1f}x".format(b) for b in [x_boost_h1[0], x_boost_h1[100], x_boost_h1[200], x_boost_h1[300], x_boost_h1[400], x_boost_h1[500]]]
    ax2.set_xticks([0, 100, 200, 300, 400, 500])
    ax2.set_xticklabels(boost_xticks, fontsize=7)
    # plot 2 y-ticks
    yticks_pct = [0, 0.2, 0.4, 0.6, 0.8, 1]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax2.set_yticks(yticks_pct)
    ax2.set_yticklabels(yticks_label, fontsize=7)
    ax2.set_title('Share of emissions between Mines', size=9)
    ax2.legend()
    ax2.grid(color='black', alpha=0.1)

    #### Plot 3
    ax3.plot(x_user_pct_share_h1, label='$1m in H1')
    ax3.plot(x_user_pct_share_atlas, label='$1m in Atlas', color='red')
    # plot 3 x-ticks
    ax3.set_xticks([0, 100, 200, 300, 400, 500])
    ax3.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=8)
    ax3.set(xlabel='Boost (x)', ylabel='% share of emissions')
    ax3.set_xticklabels(boost_xticks, fontsize=7)
    # plot 3 y-ticks
    yticks_pct = [0, 0.01, 0.02, 0.03, 0.04, 0.05]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax3.set_yticks(yticks_pct)
    ax3.set_yticklabels(yticks_label, fontsize=7)
    ax3.set_title("User with 1m: their share of total emission in different Mines", size=9)
    ax3.legend()
    ax3.grid(color='black', alpha=0.1)

    plt.subplots_adjust(hspace=0.5)
    plt.show()








def compare_harvester_yield_2harvesters(parts1=20, members1=20, parts2=20, members2=20, atlas_parts=0, debug=True):
    """
        parts1, members1 for harvester 1
        parts2, members2 for harvester 2
    """

    EXPECTED_AUM_ATLAS = ATLAS_AUM # 80mil in atlas mine, about 80% supply staked
    AUM_CAP_HARVESTER = 10 # 10mil cap in harvesters
    avg_legion_rank = 2

    # num_millions_user_stakes = 0.01 # 10k
    num_millions_user_stakes = 0.1 # 100k
    # num_millions_user_stakes = 1 # 1mil

    num_legions1 = members1*3 # 3 legions per user
    num_legions2 = members2*3

    if debug:
        print("\n============================================")
        print("Harvester_1 has:")
        print("{} parts, {} members, {} total legions\n".format(parts1, members1, members1*3))
        print("Harvester_2 has:")
        print("{} parts, {} members, {} total legions\n".format(parts2, members2, members2*3))

    boost_h1 = total_harvester_boost(num_parts=parts1, num_legions=num_legions1, drills=[], avg_legion_rank=avg_legion_rank)
    boost_h2 = total_harvester_boost(num_parts=parts2, num_legions=num_legions2, drills=[], avg_legion_rank=avg_legion_rank)
    # original atlas mine is treated as a harvester with uncapped AUM
    # it has 0 harvester parts to begin with, and can have up to 2000 staked legions to boost its mining (avg legion rank 1)
    boost_atlas = total_harvester_boost(num_parts=atlas_parts, num_legions=2000, drills=[], avg_legion_rank=1, is_atlas=True) # 6x boost by default
    if debug:
        print("Atlas gets:\t{:.2f}x boost".format(boost_atlas))
        print("Harv_1 gets:\t{:.2f}x boost\n".format(boost_h1))

    # set harvester base points = 100
    points_atlas = boost_atlas * 100
    points_h1    = boost_h1 * 100
    points_h2    = boost_h2 * 100
    points_total = points_atlas + points_h1 + points_h2

    # Calculate percentage share of total emissions split between Atlas and Harvester 1 and Harvester 2
    mine_pct_share_atlas = points_atlas / points_total
    mine_pct_share_h1 = points_h1 / points_total
    mine_pct_share_h2 = points_h2 / points_total
    if debug:
        print("Atlas gets:\t{:.2%} of emissions".format(mine_pct_share_atlas))
        print("Harv_1 gets:\t{:.2%} of emissions\n".format(mine_pct_share_h1))
        print("Harv_2 gets:\t{:.2%} of emissions\n".format(mine_pct_share_h2))

    # a user's share of total emission, staying inside Atlas mine, vs. Harvester 1 and Harvester 2
    user_pct_share_atlas = num_millions_user_stakes/EXPECTED_AUM_ATLAS * mine_pct_share_atlas
    user_pct_share_h1 = num_millions_user_stakes/10 * mine_pct_share_h1
    user_pct_share_h2 = num_millions_user_stakes/10 * mine_pct_share_h2

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
        print("1m in Harv_2 with 10m AUM gives you:\t 1/{AUM_CAP} * {MINE_PCT:.4f} = {USER_PCT:.2%}".format(
            AUM_CAP=AUM_CAP_HARVESTER,
            MINE_PCT=mine_pct_share_h2,
            USER_PCT=user_pct_share_h2
        ))
        print("\nAn entrepreneurial whale can potentially get a {:.2%} / {:.2%}\n= {:.2f}x improvement in yield".format(
            user_pct_share_h1,
            user_pct_share_atlas,
            user_pct_share_h1 / user_pct_share_atlas
        ))
        print("for collecting {} harvester parts, a guild of {} users, {} legions".format(parts1, members1, members1*3))
        print("\nNote: assumes he can deploy his full 1m in the 10m cap harvester 1 alongside other guild members")
        print("he will get an even better yield initially before the 10m cap is reached")

    return (
        boost_h1,
        boost_h2,
        boost_atlas,
        mine_pct_share_h1,
        mine_pct_share_h2,
        mine_pct_share_atlas,
        user_pct_share_h1,
        user_pct_share_h2,
        user_pct_share_atlas,
    )







## Atlas vs 2 Harvesters
def plot_atlas_harvest_comparison_2(atlas_parts=0):

    ## Array of x-axis data points
    x_boost_h1 = []
    x_boost_h2 = []
    x_boost_atlas = []

    x_mine_pct_share_h1 = []
    x_mine_pct_share_h2 = []
    x_mine_pct_share_atlas = []

    x_user_pct_share_h1 = []
    x_user_pct_share_h2 = []
    x_user_pct_share_atlas = []


    num_obs = 501
    _x_parts = np.linspace(0, 500, num_obs) # 1 to 500 parts
    _x_members = np.linspace(0, 666.66, num_obs) # 1 to 666 users, 666.6 users * 3 legions = 2000 legions


    for parts,members in zip(_x_parts, _x_members):

        (
            boost_h1,
            boost_h2,
            boost_atlas,
            mine_pct_share_h1,
            mine_pct_share_h2,
            mine_pct_share_atlas,
            user_pct_share_h1,
            user_pct_share_h2,
            user_pct_share_atlas,
        ) = compare_harvester_yield_2harvesters(
            parts1=parts,
            members1=members,
            parts2=parts/2,
            members2=members*0.5,
            # members2=members,
            atlas_parts=atlas_parts,
            debug=False
        )

        x_boost_h1.append(boost_h1)
        x_boost_h2.append(boost_h2)
        x_boost_atlas.append(boost_atlas)

        x_mine_pct_share_h1.append(mine_pct_share_h1)
        x_mine_pct_share_h2.append(mine_pct_share_h2)
        x_mine_pct_share_atlas.append(mine_pct_share_atlas)

        x_user_pct_share_h1.append(user_pct_share_h1)
        x_user_pct_share_h2.append(user_pct_share_h2)
        x_user_pct_share_atlas.append(user_pct_share_atlas)

        print("boost_h1: ", boost_h1)
        print("boost_h2: ", boost_h2)
        print("boost_atlas: ", boost_atlas)

        print("mine_pct_share_h1: ", mine_pct_share_h1)
        print("mine_pct_share_h2: ", mine_pct_share_h2)
        print("mine_pct_share_atlas: ", mine_pct_share_atlas)

        print("user_pct_share_h1: ", user_pct_share_h1)
        print("user_pct_share_h2: ", user_pct_share_h2)
        print("user_pct_share_atlas: ", user_pct_share_atlas)


    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Emission Splits: Atlas vs. 2 Harvesters')

    #### Plot 1
    ax1.plot(x_boost_h1, label="H1 boost ranges from 1x to ~3.3x boost")
    ax1.plot(x_boost_h2, label="H2 boost ranges from 1x to 2.6x boost")
    ax1.plot([], label="Atlas has {}x Atlas boost by default".format(ATLAS_MINE_BONUS), color='red')
    ax1.set(xlabel='(parts, legions)', ylabel='Boost Multiplier')
    ax1.set_xticks([0, 100, 200, 300, 400, 500])
    ax1.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=7)
    ax1.set_title('Harvest Boost', size=9)
    ax1.legend()
    ax1.grid(color='black', alpha=0.1)

    #### Plot 2
    ax2.plot(x_mine_pct_share_h1, label="H1 Share")
    ax2.plot(x_mine_pct_share_h2, label="H2 Share")
    ax2.plot(x_mine_pct_share_atlas, label="Atlas Share", color='red')
    ax2.set(xlabel='Boost (x)', ylabel='% share of emissions')
    # plot 2 x-ticks
    boost_xticks = ["{:.1f}x".format(b) for b in [x_boost_h1[0], x_boost_h1[100], x_boost_h1[200], x_boost_h1[300], x_boost_h1[400], x_boost_h1[500]]]
    ax2.set_xticks([0, 100, 200, 300, 400, 500])
    ax2.set_xticklabels(boost_xticks, fontsize=7)
    # plot 2 y-ticks
    yticks_pct = [0, 0.2, 0.4, 0.6, 0.8, 1]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax2.set_yticks(yticks_pct)
    ax2.set_yticklabels(yticks_label, fontsize=7)
    ax2.set_title('Share of emissions between Mines', size=9)
    ax2.legend()
    ax2.grid(color='black', alpha=0.1)

    #### Plot 3
    ax3.plot(x_user_pct_share_h1, label='$100k in H1')
    ax3.plot(x_user_pct_share_h2, label='$100k in H2')
    ax3.plot(x_user_pct_share_atlas, label='$100k in Atlas', color='red')
    # plot 3 x-ticks
    ax3.set_xticks([0, 100, 200, 300, 400, 500])
    ax3.set_xticklabels(['(0,0)', '(100, 400)', '(200, 800)', '(300, 1200)', '(400, 1600)', '(500, 2000)'], fontsize=8)
    ax3.set(xlabel='Boost (x)', ylabel='% share of emissions')
    ax3.set_xticklabels(boost_xticks, fontsize=7)
    # plot 3 y-ticks
    yticks_pct = [0, 0.0010, 0.0020, 0.0030, 0.0040, 0.0050]
    yticks_label = ["{:.2%}".format(b) for b in yticks_pct]
    ax3.set_yticks(yticks_pct)
    ax3.set_yticklabels(yticks_label, fontsize=7)
    ax3.set_title("User with $100k: their share of total emission in different Mines", size=9)
    ax3.legend()
    ax3.grid(color='black', alpha=0.1)

    plt.subplots_adjust(hspace=0.5)
    plt.show()




#################################
####### SIMULATES USERS YIELD INSIDE HARVESTER WITH VARIOUS BOOSTS
#################################


def plot_yield_inside_mine(treasure_multiplier=1, legion_boost=1, linestyle='-', color='blue'):

    # # staking boosts for treasures
    m = treasure_multiplier
    honeycomb = 0.02631 * m
    quarter_penny = 0.0025 * m

    rank0 = 1+0.05 # common gen 1: 5% boost
    rank3 = 1+1 # uncommon: 100% boost
    rank4 = 1+2 # all-class 200% boost
    rank5 = 1+6 # 1/1 600% boost


    x1_num_treasures = np.linspace(0,50,51)
    # let daily emissions to atlas mine be 50,000
    daily_magic_emissions = 50000

    (
        boost_h1,
        boost_atlas,
        mine_pct_share_h1,
        mine_pct_share_atlas,
        user_pct_share_h1,
        user_pct_share_atlas,
    ) = compare_harvester_yield(parts=500, members=1000, atlas_parts=0, debug=False)


    x3_num_magic_daily_atlas = user_pct_share_atlas * daily_magic_emissions
    x3_num_magic_daily_h1_max = user_pct_share_h1 * daily_magic_emissions

    # honeycomb boost as you stack more and more honeycombs (up to 200)
    honeycomb_boosts = [(1+honeycomb)**n for n in x1_num_treasures]
    honeycomb_boosts2 = [(1+honeycomb*n) for n in x1_num_treasures]
    # quarter_pennny boost as you stack more and more (up to 200)
    quarter_penny_boosts = [(1+quarter_penny)**n for n in x1_num_treasures]
    # quarter_penny_boosts = [(1+quarter_penny*n) for n in x1_num_treasures]

    # plt.plot(x1_num_treasures, honeycomb_boosts, label="Stacking honeycombs, multiplicately", color="red", linestyle="-.")
    # plt.plot(x1_num_treasures, honeycomb_boosts2, label="Stacking honeycombs, sum", color="blue", linestyle="--")
    honeycomb_legion_boosts = [(1+honeycomb)**n * legion_boost for n in x1_num_treasures]
    honeycomb2_legion_boosts = [(1+honeycomb*n) * legion_boost for n in x1_num_treasures]
    quarter_penny_boosts = [(1+quarter_penny)**n * legion_boost for n in x1_num_treasures]

    # plt.plot(x1_num_treasures, honeycomb_legion_boosts, label="honeycombs (multiplicative), legion boost {}x".format(legion_boost), linestyle=linestyle, color=color)
    plt.plot(x1_num_treasures, honeycomb2_legion_boosts, label="honeycombs (sum), legion boost {}x".format(legion_boost), linestyle='-', color=color)
    plt.xlabel("#treasures staked")
    plt.ylabel("boost (x)")


    x4_no_treasures_h1_max = [x3_num_magic_daily_atlas * legion_boost for h in honeycomb_boosts]

    # Number of magic earned daily after boosting with n staked honeycombs
    x4_honeycomb_boosted_atlas = [x3_num_magic_daily_atlas * h * legion_boost for h in honeycomb_boosts]
    x4_honeycomb_boosted_h1_max = [x3_num_magic_daily_h1_max * h * legion_boost for h in honeycomb_boosts]

    x4_honeycomb_boosted_atlas2 = [x3_num_magic_daily_atlas * h * legion_boost for h in honeycomb_boosts2]
    x4_honeycomb_boosted_h1_max2 = [x3_num_magic_daily_h1_max * h * legion_boost for h in honeycomb_boosts2]

    # Number of magic earned daily after boosting with n staked quarter_penny
    x4_quarter_penny_boosted_atlas = [x3_num_magic_daily_atlas * h * legion_boost for h in quarter_penny_boosts]
    x4_quarter_penny_boosted_h1_max = [x3_num_magic_daily_h1_max * h * legion_boost for h in quarter_penny_boosts]


    ##### Comparing growth rates of stacking up to 20 treasures
    # # plt.plot(x1_num_treasures, x4_honeycomb_boosted_atlas, label="Stacking honeycombs", color="orange", linestyle="-.")
    # plt.plot(x1_num_treasures, x4_no_treasures_h1_max , label="No treasures staked, boosted mine", color="blue", linestyle="-")
    #
    # plt.plot(x1_num_treasures, x4_honeycomb_boosted_atlas, label="Stacking honeycombs, unboosted mine", color="red", linestyle="-.")
    # plt.plot(x1_num_treasures, x4_quarter_penny_boosted_atlas, label="Stacking quarter-pennies, unboosted mine", color="red", linestyle="--")
    # # fill between upper and lower bound
    # plt.fill_between(x1_num_treasures, x4_quarter_penny_boosted_atlas, x4_honeycomb_boosted_atlas, facecolor="red", alpha=0.2)
    #
    # plt.plot(x1_num_treasures, x4_honeycomb_boosted_h1_max, label="Stacking honeycombs, boosted mine", color="purple", linestyle="-.")
    # plt.plot(x1_num_treasures, x4_quarter_penny_boosted_h1_max, label="Stacking quarter-pennies, boosted mine", color="purple", linestyle="--")
    # # fill between upper and lower bound
    # plt.fill_between(x1_num_treasures, x4_quarter_penny_boosted_h1_max, x4_honeycomb_boosted_h1_max, facecolor="purple", alpha=0.2)


    baseline_magic = x4_no_treasures_h1_max[-1] # 5.51 magic/day on 10k
    penny_cost = 83
    honey_cost = 3200
    num = len(x1_num_treasures) - 1 # 20

    # incremental income from staking 20 pennies
    penny_income_20 = x4_quarter_penny_boosted_h1_max[-1] - baseline_magic
    penny_income_1 = x4_quarter_penny_boosted_h1_max[0] - baseline_magic

    honey_income_20 = x4_honeycomb_boosted_h1_max[-1] - baseline_magic
    honey_income_1 = x4_honeycomb_boosted_h1_max[0] - baseline_magic


    payback_pennies = [penny_cost*n / income for n,income in enumerate(x4_quarter_penny_boosted_h1_max)]
    payback_honey = [honey_cost*n / income for n,income in enumerate(x4_honeycomb_boosted_h1_max)]
    payback_honey2 = [honey_cost*n / income for n,income in enumerate(x4_honeycomb_boosted_h1_max2)]

    ##### Payback period plots
    # plt.plot(x1_num_treasures, payback_honey,
    #         label="Payback (days) honeycombs, {}x treasure, {}x legion boost".format(m, legion_boost),
    #         color="orange",
    #         linestyle=linestyle)
    # plt.plot(x1_num_treasures, payback_honey,
    #         label="Payback (days) honeycombs, multiplicative".format(m, legion_boost),
    #         color="orange",
    #         linestyle=linestyle)
    # plt.plot(x1_num_treasures, payback_honey2,
    #         label="Payback (days) honeycombs, additive".format(m, legion_boost),
    #         color="blue",
    #         linestyle=linestyle)
    # plt.plot(x1_num_treasures, payback_pennies,
    #          label="Payback (days) pennies, {}x treasure, {}x legion boost".format(m, legion_boost),
    #          color="black",
    #          linestyle=linestyle)

    # plt.xlabel("Varying number of parts staked")
    # plt.ylabel("Boost multiplier")
    # plt.title("Total Harvester Boost (parts x legions boost)")
    # plt.text(150, 2.0, "guilds will have boosts\n in this region")





# # varying legions
# plot_yield_inside_mine(3, legion_boost=1, linestyle=":", color="blue")
# # common: 50% boost
# plot_yield_inside_mine(3, legion_boost=(1 + 0.5*3), linestyle=":", color="purple")
# # all-class: 200% boost
# plot_yield_inside_mine(3, legion_boost=(1 + 2*3), linestyle=":", color="red")
#
# plt.legend()
# plt.show()

# # varying treasure boosts
# plot_yield_inside_mine(1, legion_boost=2*2*2, linestyle=":")
# plot_yield_inside_mine(3, legion_boost=2*2*2, linestyle="-.")



#### Plot competition dynamics between Atlas mine and other harvesters
## uncomment the function calls below and run them in ipython

# # In the beginning Atlas has no parts
plot_atlas_harvest_comparison_1(0)
# # Later stage, Atlas may have parts (also may elect another Harvester as "the Atlas mine")
# plot_atlas_harvest_comparison_1(400)
#
#
# # In the beginning Atlas has no parts
# plot_atlas_harvest_comparison_2(0)
# # Later stage, Atlas may have parts (also may elect another Harvester as "the Atlas mine")
# plot_atlas_harvest_comparison_2(400)



