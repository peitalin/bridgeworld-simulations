
from plots.boosts import graph_total_harvester_boost_varying_legions
from plots.boosts import graph_parts_boost

from plots.compare_harvesters_1 import plot_atlas_harvest_comparison_1
from plots.compare_harvesters_2 import plot_atlas_harvest_comparison_2
from plots.user_boosts import plot_yield_inside_mine


# graph_parts_boost()

# # varying legions
plot_yield_inside_mine(3, legion_boost=1, linestyle=":", color="blue")
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
plot_atlas_harvest_comparison_2(0)
# # Later stage, Atlas may have parts (also may elect another Harvester as "the Atlas mine")
# plot_atlas_harvest_comparison_2(400)



