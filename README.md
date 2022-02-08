# Harvester Boost Calculations


## Directory Layout
```
├── "README.md"
├── "__init__.py"
├── "harvester_boosts.py"
├── "harvester_emission_splits.py"
├── "parameters.py"
├── "plots/"
├── "questing_crafting.py"
└── "summoning.py"
```

`parameters.py` contains all the configurable parameters
`harvester_boosts.py` contain the functions that work out harvester boosts and mining-power
`harvester_emission_splits` contains the logic for calculating the boost/mining-power for an arbitrary number of harvesters to work out how incoming MAGIC emissions should be split.

These three files will probably be relevant to the emissions splitting middelware in Solidity.

### Simulation Instructions for Harvesters
Uncomment (remove leading #) the `run_harvester_split_simulation_6()`
or `run_distance_boost_simulation()` function then
run `ipython -i __init__.py` to start simulations

### Simulation Instructions for Questing/Crafting and Treasure inflation/deflation over time
run `ipython -i questing_crafting.py` to start Treasure crafting/questing simulations
and its effect on treasure inflation/deflation