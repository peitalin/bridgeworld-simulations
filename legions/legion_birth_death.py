import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation


from params import QUEST_TIMES, CRAFT_TIMES, PR_DROP_LOOT_FROM_QUEST
from legion import Legion


def legion_growth_rate(
    N = 100,
    k = 100,
    b = 1,
    d = 0,
    f = lambda N,k: N/k
):
    """
        N: summoning population size
        b: birth rate
        d: death rate
        k: carrying capacity (crafting population)
    """
    return (b * f(N, k) - d) * N


def linear(N = 100, k = 100):
    return (1 - N/k)

def inverse_linear(N = 100, k = 100):
    return 1 / (1 + N/k)

def inverse_quad(N = 100, k = 100, s=1):
    return 1 / (1 + (N/(k*s))**2)

def inverse_exp(N = 100, k = 100):
    return np.exp(-np.log(2) * N / k)


ax1 = 1
ax2 = 1
FRAMES = 100


def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return


def draw_legion_paths(i):

    num_craftor = 8 + i * 8 # each i-frame is 8 craftors
    num_summoners = 16 + i * 16 # each i-frame is 8 craftors

    # clear plots to redraw
    ax2.clear()
    ax1.clear()
    # ax2.clear()

    colors = [
        'crimson',
        'mediumorchid',
        'royalblue',
        'black',
    ]

    N = np.linspace(0, 2000, 2001)
    N_k200 = [n/200 for n in N]
    N_k400 = [n/400 for n in N]
    N_k800 = [n/800 for n in N]

    growth_rate_1 = [legion_growth_rate(N=n, k=200, f=inverse_exp) for n in N]
    growth_rate_2 = [legion_growth_rate(N=n, k=400, f=inverse_exp) for n in N]
    growth_rate_3 = [legion_growth_rate(N=n, k=800, f=inverse_exp) for n in N]

    success_rate_1 = [inverse_quad(N=n, k=200) for n in N]
    success_rate_2 = [inverse_quad(N=n, k=400) for n in N]
    success_rate_3 = [inverse_quad(N=n, k=800) for n in N]

    # array index for the growth_rate of current num_summoners
    index_growth_num_summoners = np.argmin(np.abs(np.subtract(N, num_summoners)))

    legion_birth_yvalue = {
        '1': growth_rate_1[index_growth_num_summoners],
        '2': growth_rate_2[index_growth_num_summoners],
        '3': growth_rate_3[index_growth_num_summoners],
    }
    success_rate_yvalue = {
        '1': success_rate_1[index_growth_num_summoners],
        '2': success_rate_2[index_growth_num_summoners],
        '3': success_rate_3[index_growth_num_summoners],
    }

    ############## PLOTS ##################

    ####### change in summoning success rate, vs population
    ax1.plot(N, success_rate_1 , color=colors[0])
    ax1.plot(N, success_rate_2 , color=colors[1])
    ax1.plot(N, success_rate_3 , color=colors[2])

    ax2.set(xlabel='#summoners', ylabel='Number of legions born/period (~7days) ')
    ax1.set(xlabel='#summoners', ylabel='Summoning Success Rate')

    ax1.plot([num_summoners], [success_rate_yvalue['1']],
        label=r"Pr(summon|craftors=200): %{:.1%}".format(success_rate_yvalue['1']),
        color=colors[0], linestyle="-", marker="*")

    ax1.plot([num_summoners], [success_rate_yvalue['2']],
        label=r"Pr(summon|craftors=400): %{:.1%}".format(success_rate_yvalue['2']),
        color=colors[1], linestyle="-", marker="*")

    ax1.plot([num_summoners], [success_rate_yvalue['3']],
        label=r"Pr(summon|craftors=800): %{:.1%}".format(success_rate_yvalue['3']),
        color=colors[2], linestyle="-", marker="*")

    ####### change in growth rate, vs population
    ax2.plot(N, growth_rate_1, color=colors[0])
    ax2.plot([num_summoners], [legion_birth_yvalue['1']],
        label="200 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['1']),
        color=colors[0], marker="*")

    ax2.plot(N, growth_rate_2, color=colors[1])
    ax2.plot([num_summoners], [legion_birth_yvalue['2']],
        label="400 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['2']),
        color=colors[1], marker="*")

    ax2.plot(N, growth_rate_3, color=colors[2])
    ax2.plot([num_summoners], [legion_birth_yvalue['3']],
        label="800 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['3']),
        color=colors[2], marker="*")

    ########################

    ax2.axvline(x=num_summoners, color='black', linestyle=':', alpha=0.5)
    ax1.axvline(x=num_summoners, color='black', linestyle=':', alpha=0.5)

    ax2.set_title('Legions Birth Rate per Period (~7days) | {} Summoners'.format(num_summoners), size=10)
    ax1.set_title('%Summon Success Rate | {} Summoners'.format(num_summoners), size=10)

    ax2.legend()
    ax1.legend()

    ax1.legend(bbox_to_anchor=(1.42, 1), loc="upper right")
    ax2.legend(bbox_to_anchor=(1.48, 1), loc="upper right")

    ax2.grid(which='minor', alpha=0.2)
    ax2.grid(which='major', alpha=0.4)
    ax1.grid(which='minor', alpha=0.2)
    ax1.grid(which='major', alpha=0.4)






def run_legion_growth_simulation():

    global fig
    global ax2
    global ax1

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Dynamic Legion Summoning Rates')
    fig.set_size_inches(12, 9)

    ani = FuncAnimation(
        fig,
        draw_legion_paths,
        frames=FRAMES,
        interval=100,
        repeat=False,
        init_func=init_plot,
    )

    plt.subplots_adjust(left=0.08, right=0.7, top=0.9, bottom=0.1, hspace=0.4)
    plt.show()

run_legion_growth_simulation()





## Prices are a function of supply and demand
prices = [
    1000,
    400,
    315,
    75,
    10,
]

def pr_weighted_price_of_treasures(lvl='easy'):
    # pr: probabilities of dropping t1, t2, t3, t4, t5 loot
    # in percentages
    if lvl=='easy':
        pr = [0.0, 0.025, 0.05, 0.15, 0.775]
    if lvl=='medium':
        pr = [0.015, 0.05, 0.07, 0.17, 0.695]
    if lvl=='hard':
        pr = [0.025, 0.09, 0.08, 0.022, 0.0585]
    return np.sum([price*prob for price,prob in zip(prices,pr)])



## Weekly expected ROI on differnet legion pathways
def expected_roi_questing(lvl='easy', days=7):
    # Er[questing] = PR_DROP_LOOT_FROM_QUEST * drop_rate_weighted_price of treasures
    # [drop_rate * price for drop_rate, price in [t1, t2, t3, t4, t5 treasure tiers]]

    nquests = 24 / QUEST_TIMES[lvl] * days
    roi = PR_DROP_LOOT_FROM_QUEST * nquests * pr_weighted_price_of_treasures(lvl)
    return roi
    # return 1 / population_questing


def expected_roi_mining(aum=50_000, nftBoost=0.75):
    # Er[mining] = NFTBoost * user_wealth
    # legions are more useful in the mine for richer users
    weeks = 52
    return aum * nftBoost / weeks


def expected_roi_summoning():
    # Er[summoning] = -500MAGIC - opportunity_cost_of_questing_1_week + Er[questing at t+1...]
    # sacrifice 1 period of questing/mining and 500 MAGIC for 1x  lifetime value of a legion
    # which is an income stream of questing 1 period from now = Er_t+1[questing]

    opportunity_cost_of_questing_1_week = expected_roi_questing()
    ltv_questing = expected_roi_questing() / 0.08 # assume 8% discount rate or roughly 12 week return
    return -500 - opportunity_cost_of_questing_1_week + ltv_questing


# print('expected_roi_questing', expected_roi_questing() * 12)
# print('expected_roi_mining' , expected_roi_mining())
# print('expected_roi_summoning' , expected_roi_summoning())

