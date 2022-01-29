
# for devs/team to calibrate
PARTS_BOOST_FACTOR = 1
LEGIONS_BOOST_FACTOR = 0.5
# parts boost maxes out at 100%
# legions boosts max out at 50% boost
# they stack together to determine overall boost
# parts_boost should probably be bigger than legions (as a craft item)

ATLAS_MINE_BONUS = 2
# atlas mine gets a default boost
EXPECTED_ATLAS_AUM = 70
# Estimated AUM for Atlas Mine
# generally it will have a much larger AUM than other harvesters, 50mil~80mil vs 10mil

AUM_CAP_HARVESTER = 10
# 10mil cap in harvesters

MIN_LEGIONS = 1
MAX_LEGIONS = 2000
# legions boosts maxes out at 2000 staked legions
MAX_HARVESTER_PARTS = 500
# harvester parts boosts maxes out at 500
MAX_EXTRACTORS = 5
# extractor boosts maxes out at 5


## Double check these MAGIC emission numbers
MAGIC_EMISSIONS_BY_YEAR = {
    1: 43_464_251,
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
    'gen0_1_1': 5,  # 1/1
    'gen1_common': 1,
    'gen1_uncommon': 2,
    'gen1_rare': 3,
}

TREASURES_BOOST_PARAMS = {
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
}

EXTRACTOR_BOOST_PARAMS = {
    'small_extractor': 0.15, #  15%
    'medium_extractor': 0.20, # 20%
    'large_extractor': 0.25, # 25%
}

