
# for devs/team to calibrate
PARTS_BOOST_FACTOR = 0.5 # 50% is 1.5x boost (1 + 50%)
LEGIONS_BOOST_FACTOR = 1 # 100% is 2x boost (1 + 100%)
DISTANCE_BOOST_FACTOR = 1 # 100% is 2x boost (1 + 100%)
# these boosts stack together multiplicatively to determine overall boost
# parts_boost should probably be bigger than legions (as a craft item)

ATLAS_MINE_BONUS = 5
# atlas mine gets a default boost

EXPECTED_ATLAS_AUM = 80
# Estimated AUM for Atlas Mine in millions
# 85mil locked, 45mil MAGIC locked for 1 year
# generally it will have a much larger AUM than other harvesters, 50mil~80mil vs 10mil

AUM_CAP_HARVESTER = 6
# 6mil cap in harvesters

MIN_LEGIONS = 1
MAX_LEGIONS = 1000
# MAX_LEGIONS = 2400

# legions boosts maxes out at 2000 staked legions
MAX_HARVESTER_PARTS = 500
# harvester parts boosts maxes out at 500
MAX_EXTRACTORS = 10
# extractor boosts maxes out at N

# Geographical Map params
MAX_MAP_HEIGHT = 100
MAX_MAP_WIDTH = 100

# total circulating magic supply
TOTAL_MAGIC_SUPPLY = 140_000_000

# A cap on total AUM a user can deposit in a harvester
DEPOSIT_AMOUNT_PER_PART = 30_000
MAX_PARTS_PER_ADDRESS = 800
## should be 40, relax this assumption for simulation purposes only
# MAX_PARTS_PER_ADDRESS = 40


## Double check these MAGIC emission numbers
MAGIC_EMISSIONS_BY_YEAR = {
    # 1: 43_464_251,
    1: 23_464_251, # 20mil already mined for atlas
    2: 21_732_125,
    3: 10_866_063,
    4: 5_433_031,
    5: 2_716_516,
    6: 1_358_258,
    7: 679_129,
    8: 339_564,
    9: 169_782,
    10: 84_891,
    11: 42_446,
    12: 21_223,
}

TIME_LOCK_BOOST_PARAMS = {
    'none': 0, # 0% bonus
    '2_weeks': 0.1, # 10%
    '1_month': 0.25, # 25%
    '3_months': 0.80, # 80%
    '6_months': 1.8, # 180%
    '12_months': 4, # 400%
}

LEGION_BOOST_PARAMS = {
    'gen0_common': 0.5, # commons
    'gen0_special': 0.75, # includes riverman, Numeraire 50%
    'gen0_uncommon': 1, # Assasin etc 100%
    'gen0_rare': 2, # all-class 200%
    'gen0_1_1': 6, # 1/1 600%
    'gen1_common': 0.05, # 5%
    'gen1_uncommon': 0.1, # 10%
    'gen1_rare': 0.25, # 25%
}

LEGION_RANK_PARAMS = {
    'gen0_common': 1, # commons
    'gen0_special': 2, # includes riverman, Numeraire 50%
    'gen0_uncommon': 3, # Assasin etc 100%
    'gen0_rare': 4, # all-class 200%
    'gen0_1_1': 4,  # 1/1
    'gen1_common': 1,
    'gen1_uncommon': 2,
    'gen1_rare': 3,
}

TREASURES_BOOST_PARAMS = {
    "honeycomb":	0.15785,
    "grin":	0.15712,
    "bottomless_elixir":	0.07609,
    "cap_of_invisibility":	0.07609,
    "ancient_relic":	0.07525,
    "castle":	0.07330,
    "thread_of_divine_silk":	0.07330,
    "mollusk_shell":	0.06720,
    "bait_for_monsters":	0.07298,
    "immovable_stone":	0.07236,
    "snow_white_feather":	0.06403,
    "red_feather":	0.06379,
    "ivory_breastpin":	0.06367,
    "divine_hourglass":	0.06343,
    "military_stipend":	0.06227,
    "bag_of_rare_mushrooms":	0.06159,
    "carriage":	0.06071,
    "small_bird":	0.05985,
    "score_of_ivory":	0.05954,
    "unbreakable_pocketwatch":	0.05933,
    "framed_butterfly":	0.05841,
    "cow":	0.05801,
    "pot_of_gold":	0.05791,
    "divine_mask":	0.05713,
    "common_bead":	0.05637,
    "favor_from_the_gods":	0.05545,
    "jar_of_fairies":	0.05328,
    "witches_broom":	0.05073,
    "common_feather":	0.03377,
    "green_rupee":	0.03270,
    "grain":	0.03220,
    "lumber":	0.03017,
    "common_relic":	0.02153,
    "ox":	0.01587,
    "blue_rupee":	0.01527,
    "donkey":	0.01218,
    "half_penny":	0.00785,
    "silver_coin":	0.00784,
    "diamond":	0.00781,
    "pearl":	0.00775,
    "dragon_tail":	0.00771,
    "red_rupee":	0.00770,
    "gold_coin":	0.00769,
    "emerald":	0.00758,
    "beetle_wing":	0.00752,
    "quarter_penny":	0.00750,
}

EXTRACTOR_BOOST_PARAMS = {
    'small_extractor': 0.15,
    'medium_extractor': 0.20,
    'large_extractor': 0.25,
    # 'small_extractor': 0.20,
    # 'medium_extractor': 0.25,
    # 'large_extractor': 0.30,
}

LEGION_WEIGHTS = {
    # Genesis Legions
    'gen0_1_1': 120, # 1/1 120kg
    'gen0_rare': 40, # all-class 40kg
    'gen0_uncommon': 21, # Assasin etc 20kg
    'gen0_special': 16, # includes riverman, Numeraire 15kg
    'gen0_common': 11, # commons 10kg
    # Aux legions
    'gen1_rare': 5.5, #
    'gen1_uncommon': 4, #
    'gen1_common': 2.5, #
}

