import math
from estimators.slates import base
from scipy import stats
from typing import List

class Interval(base.Interval):
    def __init__(self):
        self.data = {'n':0.,'N':0, 'SoS':0}

    def add_example(self, p_logs: List[float], r: float, p_preds: List[float], count: float = 1.0) -> None:
        """Expects lists for logged probabilities and predicted probabilities. These should correspond to each slot.
        This function is implemented under the simplifying assumptions of
        example 4 in the paper 'Off-policy evaluation for slate recommendation'
        where the slate space is a cartesian product and the logging policy is a
        product distribution"""
        if not isinstance(p_logs, list) or not isinstance(p_preds, list):
            raise('Error: p_logs and p_preds must be lists')

        if(len(p_logs) != len(p_preds)):
            raise('Error: p_logs and p_preds must be the same length, found {} and {} respectively'.format(len(p_logs), len(p_preds)))

        self.data['N'] += count
        p_over_ps = 0
        num_slots = len(p_logs)
        for p_log, p_pred in zip(p_logs, p_preds):
            p_over_ps += p_pred/p_log
        p_over_ps -= num_slots - 1

        if r != 0:
            self.data['n'] += r*p_over_ps*count
            self.data['SoS'] += ((r*p_over_ps)**2)*count

    def get(self, alpha: float = 0.05) -> List[float]:
        bounds = []
        num = self.data['n']
        den = self.data['N']
        SoS = self.data['SoS']

        if SoS > 0.0:
            zGaussianCdf = stats.norm.ppf(1-alpha/2)

            variance = (SoS - num * num / den) / (den - 1)
            gaussDelta = zGaussianCdf * math.sqrt(variance/den)
            bounds.append(num / den - gaussDelta)
            bounds.append(num / den + gaussDelta)

        if not bounds:
            bounds = [0, 0]
        return bounds
