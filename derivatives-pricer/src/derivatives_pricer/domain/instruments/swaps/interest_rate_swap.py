from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class InterestRateSwap:
    notional: float
    fixed_rate: float
    payment_dates: List[float]
    floating_spread: float = 0.0
    fixed_rate_payer: bool = True
