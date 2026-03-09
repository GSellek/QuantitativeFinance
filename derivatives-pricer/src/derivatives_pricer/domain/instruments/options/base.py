from dataclasses import dataclass

@dataclass(frozen=True)
class Option:
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: str