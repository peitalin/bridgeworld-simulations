# Harvester Boost Calculations


## Directory Layout
```
├── "README.md"
├── "__init__.py"
├── "harvester_boost_count.py"
├── "harvester_factory.py"
├── "harvester_middleman.py"
├── "master_of_coin.py"
├── "parameters.py"
└── "..."
```

`parameters.py` contains all the configurable parameters

`harvester_boost_count.py` contain the functions that work out harvester boosts

`harvester_factory` creates new harvesters, keeps track of their utilisation

`harvester_middleman` calculates the boost and share of emissions for an arbitrary number of harvesters. It works out the final percentage split of MAGIC emissions coming from MasterOfCoin.

These three files will be most relevant to the emissions splitting middleware in Solidity.

### Harvester Factory + Middleman

run `ipython -i __init__.py` which runs:
```
# 1. Create MasterOfCoin
master_of_coin = MasterOfCoin()

# 2. create HarvesterFactory
harvester_factory = HarvesterFactory()

# 3. create UtilizationMiddleware
# which can pull emissions from MasterOfCoin
# and has access to harvester utilization and boost info from HarvesterFactory
middleman = UtilizationMiddleman(
	master_of_coin=master_of_coin,
	harvester_factory=harvester_factory
)

# 4. Create harvesters one by one, and watch utilization ratios change
harvester_factory.create_harvester(id=0, aum_staked=5_000_000)
harvester_factory.create_harvester(id=1, aum_staked=6_000_000)
harvester_factory.create_harvester(id=2, aum_staked=7_000_000)
harvester_factory.create_harvester(id=3, aum_staked=8_000_000)

# activate harvester, otherwise it has no impact on emission shares
harvester_factory.harvesters[0].activate()
harvester_factory.harvesters[1].activate()
harvester_factory.harvesters[2].activate()
harvester_factory.harvesters[3].activate()

print(middleman)
print(harvester_factory)
```

You can interact with `middleman`, `harvester_factory`, and `harvesters` and print them
to see how their `utilisation` and `Magic emissions shares` change


### Simulation Instructions for Harvesters
Uncomment (remove leading #) the `run_harvester_split_simulation_6()`
or `run_distance_boost_simulation()` function then
run `ipython -i __init__.py` to start simulations

### Simulation Instructions for Questing/Crafting and Treasure inflation/deflation over time
run `ipython -i legions/questing_crafting.py` to start Treasure crafting/questing simulations
and its effect on treasure inflation/deflation
