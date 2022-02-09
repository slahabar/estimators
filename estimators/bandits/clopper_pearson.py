import math
from scipy.stats import beta
from estimators.bandits import base
from typing import List

class Interval(base.Interval):

    def __init__(self):
        ################################# Aggregates quantities #########################################
        #
        # 'n':   IPS of numerator
        # 'N':   total number of samples in bin from log (IPS = n/N)
        # 'c':   max abs. value of numerator's items (needed for Clopper-Pearson confidence intervals)
        #
        #################################################################################################

        self.data = {'n':0.,'N':0,'c':0.}

    def add_example(self, p_log: float, r: float, p_pred: float, count: float = 1.0) -> None:
        self.data['N'] += count
        if p_pred > 0:
            p_over_p = p_pred/p_log
            if r != 0:
                self.data['n'] += r*p_over_p*count
                self.data['c'] = max(self.data['c'], r*p_over_p)

    def get(self, alpha: float = 0.05) -> List[float]:
        bounds = []
        num = self.data['n']
        den = self.data['N']
        max_weighted_cost = self.data['c']

        if max_weighted_cost > 0.0:
            successes = num / max_weighted_cost
            n = den / max_weighted_cost
            bounds.append(beta.ppf(alpha / 2, successes, n - successes + 1))
            bounds.append(beta.ppf(1 - alpha / 2, successes + 1, n - successes))

        if not bounds:
            bounds = [0, 0]
        return bounds
