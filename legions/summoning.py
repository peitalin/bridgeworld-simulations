
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot

#################################################
#################################################
##### Summoning Calculations
#################################################
#################################################


# x-axis data points
cycles = np.linspace(0, 12, 13) # 1 to 13 cycles - 4 months

# Genesis Legion Counts
# Legions Gen0	Common	1566
# Legions Gen0	Numeraire	711
# Legions Gen0	Riverman	540
# Legions Gen0	Uncommon	376
# Legions Gen0	Rare	275
# Legions Gen0	1 of 1	5
# total: 3473 genesis legions


# a legion can only do one of the follow at a time:
#     1) mine boost
#     2) summon
#     3) quest
#     4) craft

# Ok, so lets say for g0 legions:
# 30~50% of legions are staking
# ~30% are questing/crafting
# ~20% are summoning


def predict_max_legion_population(cycle, num_genesis_legions=3473):
    """cycle: number of summoning cycles into the game a cycle is 1 week"""
    n = cycle
    return (n * (n +1))/2 * num_genesis_legions


def plot_legion_population():
    # if every genesis legion were to summon non stop
    max_population = [predict_max_legion_population(c) for c in cycles]
    # if 20% of legions summon non stop
    pct_20_population = [predict_max_legion_population(c, 695) for c in cycles]
    # if only 1 genesis legion were to summon non stop
    min_population = [predict_max_legion_population(c, 1) for c in cycles]

    plt.plot(cycles, max_population, color="purple", linestyle="-", label="Max population, 3473 g0 legions summoning weekly")
    plt.plot(cycles, pct_20_population, color="purple", linestyle="--", label="~20% of g0 legions summoning weekly (695)")
    plt.plot(cycles, min_population, color="purple", linestyle=":", label="Min population, 1 g0 legions summoning weekly")
    plt.fill_between(cycles, min_population, max_population, facecolor="purple", alpha=0.2)

    plt.xlabel("Week")
    plt.ylabel("Number of Gen1 Legions")
    plt.title("Growth of Gen1 Legions over time")
    plt.grid()
    plt.legend()
    plt.show()


