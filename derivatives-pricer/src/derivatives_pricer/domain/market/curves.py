import numpy as np

class YieldCurve:

    def __init__(self, rate: float):
        self.rate = rate

    def discount(self, t: float) -> float:
        return np.exp(-self.rate * t)

    def forward_rate(self, t1: float, t2: float) -> float:
        return self.rate