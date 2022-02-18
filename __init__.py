from plots.compare_6_harvesters import run_harvester_split_simulation_6
from plots.compare_distance import run_distance_boost_simulation

## contracts
from master_of_coin import MasterOfCoin
from harvester_factory import Harvester, HarvesterFactory
from harvester_middleman import UtilizationMiddleman




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
# activate harvester, otherwise it has no impact on emission shares
harvester_factory.harvesters[0].activate()
harvester_factory.harvesters[1].activate()

print(middleman)
print(harvester_factory)

print("\n\t====================================================")
print("\t************ Creating 2 more Harvesters ************")
print("\t====================================================\n")


harvester_factory.create_harvester(id=2, aum_staked=7_000_000)
harvester_factory.create_harvester(id=3, aum_staked=8_000_000)
#
harvester_factory.harvesters[2].activate()
harvester_factory.harvesters[3].activate()

print(middleman)
print(harvester_factory)










####### Harvesters Yield Wars Simulation #######
# run_harvester_split_simulation_6()

####### Distance Boost Simulation ######
# run_distance_boost_simulation()