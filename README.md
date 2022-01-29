# Boosting Yields Calculations

Steps to calculate a user's yield
1. Determine the harvester's share of total emissions (e.g %28 all emissions)
2. Within that harvester, calculate the user's boost share of the pool (e.g. %8.65)
3. Multiply daily emissions with `harvester_share`, then multiply with `user_share`. E.g. 50_000 MAGIC * 0.28 * 0.0865


## Harvester Boosts

We can boost the harvester by
  - adding more harvester parts
  - staking more legions on the harvester
  - staking legions that have higher rarities/rank

Both parts and legions boosts are quadratic, they have diminishing returns as you stake more parts and legions.
When a harvester is boosted, the extra yield comes at the expense of the other harvesters (including Atlas mine).
It works like Curve's veCRV gauge boosts



## Calculating Harvester Share of Emissions
The `total_harvester_boost` function in the `harvestor_boosts.py` script calculates the total boost for a harvester

For each harvester (there may be more than 2) run the `total_harvester_boost` function. Example:
```python
boost_harvester_1 = total_harvester_boost(num_parts=200, num_legions=600, avg_legion_rank=1)

# original atlas mine is treated as a harvester with uncapped AUM
# it has 0 harvester parts to begin with, and can have up to 2000 staked legions to boost its mining (avg legion rank 1)
atlas_parts = 0
boost_atlas = total_harvester_boost(num_parts=atlas_parts, num_legions=2000, avg_legion_rank=1, is_atlas=True) # 7.5x
```

Then calculate the share each harvester gets after applying boost
```python
# let each harvester's base points = 100
points_atlas = boost_atlas * 100
points_h1    = boost_harvester_1 * 100
points_total = points_atlas + points_h1

# Calculate percentage share of total emissions split between Atlas and Harvester 1
mine_pct_share_atlas = points_atlas / points_total
mine_pct_share_h1 = points_h1 / points_total
```

For an example with logs of the calculations, execute the script in ipython, then run:
```python
compare_harvester_yield(parts=20, members=20)
```

Which should give you output something like:
```
============================================
Harvester_1 has:
20 parts, 20 members, 60 total legions

Atlas gets:	7.50x boost
Harv_1 gets:	1.11x boost

Atlas gets:	87.11% of emissions
Harv_1 gets:	12.89% of emissions

For a whale with 1mil:
1m in Atlas with 80m AUM gives you:	 1/80 * 0.8711 = 1.09% of emissions
1m in Harv_1 with 10m AUM gives you:	 1/10 * 0.1289 = 1.29%
```

## Calculating an individuals share within a mine
You can work out boosts at the individual level by calling the `user_boost_inside_harvester` function to work out the boost,
then multiplying the size of the user's deposit
(remember to add the extra AUM to the total AUM when calculating percentage share of pool)

E.g. For a user with 100k in Harvester 1 with a 10m AUM cap:
```python
user_boost =  user_boost_inside_harvester(
    '2_weeks',
    legions=['gen0_common', 'gen0_uncommon', 'gen0_rare'],
    treasures=['honeycomb', 'grin'],
    consumables=['small_extractor']
)

original_deposit_size = 0.1
boosted_deposit_size = original_deposit_size * user_boost

# 100k in Harv_1 with 10m AUM cap gives you:
# boosted_deposit_size / (10m + boosted_deposit_size - original_deposit_size) = user's share of harvester 1's emissions
# we add the extra AUM from the boosted_deposit_size to the denominator AUM

users_share_of_harvester = boosted_deposit_size / (10 + boosted_deposit_size - original_deposit_size)
print("users_share_of_harvester is {:.4%}".format(users_share_of_harvester))
# users_share_of_harvester is 5.2768%

```





If you want to print out the plots of competition in emissions between atlas and the other harvesters, run:
```
# In the beginning Atlas has no parts
plot_atlas_harvest_comparison_1(0)
# Later stage, Atlas may have parts (also may elect another Harvester as "the Atlas mine")
plot_atlas_harvest_comparison_1(400)
```



