

class TreasureAccounting:
    """ Treasures minting/breaking accounting history object """

    def __init__(self):
        # Balances for net treasures created and broken at a given point in time
        self.created_treasures = {
            't1': 0,
            't2': 0,
            't3': 0,
            't4': 0,
            't5': 0,
        }
        self.broken_treasures = {
            't1': 0,
            't2': 0,
            't3': 0,
            't4': 0,
            't5': 0,
        }
        # timeseries of treasure created/broken balances over time
        # cumulative balances
        self.created_treasures_history = {
            't1': [],
            't2': [],
            't3': [],
            't4': [],
            't5': [],
        }
        self.broken_treasures_history = {
            't1': [],
            't2': [],
            't3': [],
            't4': [],
            't5': [],
        }
        self.net_diff_treasures_history = {
            't1': [],
            't2': [],
            't3': [],
            't4': [],
            't5': [],
        }

    def add_to_created(self, treasures=[]):
        """treasures=['t1', 't2', 't1']"""
        for t in treasures:
            self.created_treasures[t] += 1

    def add_to_broken(self, treasures=[]):
        """treasures=['t1', 't2', 't1']"""
        for t in treasures:
            self.broken_treasures[t] += 1

    def take_snapshot_of_treasure_balances(self):
        # takes the current balances, takes a snapshot, then appends to history
        broken_treasures = self.broken_treasures
        created_treasures = self.created_treasures

        self.broken_treasures_history['t1'].append(broken_treasures['t1'])
        self.broken_treasures_history['t2'].append(broken_treasures['t2'])
        self.broken_treasures_history['t3'].append(broken_treasures['t3'])
        self.broken_treasures_history['t4'].append(broken_treasures['t4'])
        self.broken_treasures_history['t5'].append(broken_treasures['t5'])

        self.created_treasures_history['t1'].append(created_treasures['t1'])
        self.created_treasures_history['t2'].append(created_treasures['t2'])
        self.created_treasures_history['t3'].append(created_treasures['t3'])
        self.created_treasures_history['t4'].append(created_treasures['t4'])
        self.created_treasures_history['t5'].append(created_treasures['t5'])

        self.net_diff_treasures_history['t1'].append(created_treasures['t1'] - broken_treasures['t1'])
        self.net_diff_treasures_history['t2'].append(created_treasures['t2'] - broken_treasures['t2'])
        self.net_diff_treasures_history['t3'].append(created_treasures['t3'] - broken_treasures['t3'])
        self.net_diff_treasures_history['t4'].append(created_treasures['t4'] - broken_treasures['t4'])
        self.net_diff_treasures_history['t5'].append(created_treasures['t5'] - broken_treasures['t5'])








