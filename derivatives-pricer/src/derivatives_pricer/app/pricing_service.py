from __future__ import annotations

from dataclasses import dataclass

from derivatives_pricer.domain.instruments.options.binary_option import BinaryOption
from derivatives_pricer.domain.instruments.options.european_option import EuropeanOption
from derivatives_pricer.domain.instruments.swaps.interest_rate_swap import InterestRateSwap
from derivatives_pricer.domain.market.curves import YieldCurve
from derivatives_pricer.domain.models.black_scholes import BlackScholesModel
from derivatives_pricer.domain.models.model_registry import ModelRegistry
from derivatives_pricer.domain.pricers.option_pricer import OptionPricer
from derivatives_pricer.domain.pricers.swap_pricer import SwapPricer

_DEFAULT_MODEL = "black_scholes"


@dataclass
class EuropeanOptionRequest:
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: str
    pricing_model: str = _DEFAULT_MODEL

    @classmethod
    def from_dict(cls, data: dict) -> "EuropeanOptionRequest":
        return cls(
            spot=data["spot"],
            strike=data["strike"],
            maturity=data["maturity"],
            rate=data["rate"],
            dividend_yield=data["dividend_yield"],
            volatility=data["volatility"],
            option_type=data["option_type"],
            pricing_model=data.get("pricing_model", _DEFAULT_MODEL),
        )


@dataclass
class BinaryOptionRequest(EuropeanOptionRequest):
    payout: float = 1.0

    @classmethod
    def from_dict(cls, data: dict) -> "BinaryOptionRequest":
        base = EuropeanOptionRequest.from_dict(data)
        return cls(**vars(base), payout=data.get("payout", 1.0))


@dataclass
class SwapRequest:
    notional: float
    fixed_rate: float
    payment_dates: list
    rate: float
    floating_spread: float = 0.0
    fixed_rate_payer: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "SwapRequest":
        return cls(
            notional=data["notional"],
            fixed_rate=data["fixed_rate"],
            payment_dates=data["payment_dates"],
            rate=data["rate"],
            floating_spread=data.get("floating_spread", 0.0),
            fixed_rate_payer=data.get("fixed_rate_payer", True),
        )


class PricingService:

    def __init__(self, registry: ModelRegistry | None = None):
        if registry is None:
            registry = ModelRegistry()
            registry.register("black_scholes", BlackScholesModel())
        self._registry = registry

    def _get_pricer(self, pricing_model: str) -> OptionPricer:
        return OptionPricer(self._registry.get(pricing_model))

    @staticmethod
    def _build_european_option(request: EuropeanOptionRequest) -> EuropeanOption:
        return EuropeanOption(
            spot=request.spot, strike=request.strike, maturity=request.maturity,
            rate=request.rate, dividend_yield=request.dividend_yield,
            volatility=request.volatility, option_type=request.option_type,
        )

    @staticmethod
    def _build_binary_option(request: BinaryOptionRequest) -> BinaryOption:
        return BinaryOption(
            spot=request.spot, strike=request.strike, maturity=request.maturity,
            rate=request.rate, dividend_yield=request.dividend_yield,
            volatility=request.volatility, option_type=request.option_type,
            payout=request.payout,
        )

    def _compute_option_metric(self, metric: str, request: dict, option_cls: str) -> float:
        pricing_model = request.get("pricing_model", _DEFAULT_MODEL)
        pricer = self._get_pricer(pricing_model)

        if option_cls == "european":
            req = EuropeanOptionRequest.from_dict(request)
            instrument = self._build_european_option(req)
        elif option_cls == "binary":
            req = BinaryOptionRequest.from_dict(request)
            instrument = self._build_binary_option(req)
        else:
            raise ValueError(f"Unknown option class: {option_cls}")

        return pricer._dispatch(metric, instrument)

    def price_european_option(self, request: dict) -> float:
        return self._compute_option_metric("price", request, "european")

    def delta_european_option(self, request: dict) -> float:
        return self._compute_option_metric("delta", request, "european")

    def gamma_european_option(self, request: dict) -> float:
        return self._compute_option_metric("gamma", request, "european")

    def speed_european_option(self, request: dict) -> float:
        return self._compute_option_metric("speed", request, "european")

    def vega_european_option(self, request: dict) -> float:
        return self._compute_option_metric("vega", request, "european")

    def theta_european_option(self, request: dict) -> float:
        return self._compute_option_metric("theta", request, "european")

    def rho_rate_european_option(self, request: dict) -> float:
        return self._compute_option_metric("rho_rate", request, "european")

    def rho_dividend_yield_european_option(self, request: dict) -> float:
        return self._compute_option_metric("rho_dividend_yield", request, "european")

    def price_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("price", request, "binary")

    def delta_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("delta", request, "binary")

    def gamma_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("gamma", request, "binary")

    def speed_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("speed", request, "binary")

    def vega_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("vega", request, "binary")

    def theta_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("theta", request, "binary")

    def rho_rate_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("rho_rate", request, "binary")

    def rho_dividend_yield_binary_option(self, request: dict) -> float:
        return self._compute_option_metric("rho_dividend_yield", request, "binary")

    def price_interest_rate_swap(self, request: dict) -> float:
        req = SwapRequest.from_dict(request)
        swap = InterestRateSwap(
            notional=req.notional, fixed_rate=req.fixed_rate,
            payment_dates=req.payment_dates, floating_spread=req.floating_spread,
            fixed_rate_payer=req.fixed_rate_payer,
        )
        return SwapPricer(YieldCurve(rate=req.rate)).price(swap)