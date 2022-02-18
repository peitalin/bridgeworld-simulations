import numpy as np
from parameters import MAGIC_EMISSIONS_BY_YEAR


class MasterOfCoin:
    """Mock MasterOfCoin for emissions"""

    def __init__(self):
        self.emissions = MAGIC_EMISSIONS_BY_YEAR.copy()

    def __repr__(self):
        ### Prints Harvester Details
        return """
        === MasterOfCoin ==========
        Emissions
        yr 1:\t{}
        yr 2:\t{}
        yr 3:\t{}
        yr 4:\t{}
        yr 5:\t{}
        """.format(
            self.emissions[1],
            self.emissions[2],
            self.emissions[3],
            self.emissions[4],
            self.emissions[5],
        )

    def get_emissions_for_bridgeworld(self, amount=None, year=1):
        ### https://treasuredao.freeflarum.com/d/16-tip-08-liquidity-bootstrapping-program
        ### assume 90% goes to BW (TIP-08)
        if amount == None:
            # print('pulling full amount for this year')
            amount = 0.9 * MAGIC_EMISSIONS_BY_YEAR[year]
        if self.emissions[year] >= amount:
            self.emissions[year] -= amount
            return amount
        else:
            print('insufficient balance for this year')

