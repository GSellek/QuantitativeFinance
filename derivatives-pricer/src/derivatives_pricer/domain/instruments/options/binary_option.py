from dataclasses import dataclass


@dataclass(frozen=True)
class BinaryOption:
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: str
    payout: float = 1.0

    instrument_key: str = "binary"