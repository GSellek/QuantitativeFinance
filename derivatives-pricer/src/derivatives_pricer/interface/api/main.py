from fastapi import FastAPI
from pydantic import BaseModel
from derivatives_pricer.app.pricing_service import PricingService

app = FastAPI(title="Derivatives Pricer API")

pricing_service = PricingService()

class EuropeanOptionPricingRequest(BaseModel):
    spot: float = 100.0
    strike: float = 100.0
    maturity: float = 1.0
    rate: float = 0.02
    dividend_yield: float = 0.05
    volatility: float = 0.2
    option_type: str = "call"
    pricing_model: str = "black_scholes"

@app.post("/price/european")
def price_european_option(request: EuropeanOptionPricingRequest):
    price = pricing_service.price_european_option(request.dict())
    delta = pricing_service.delta_european_option(request.dict())
    gamma = pricing_service.gamma_european_option(request.dict())
    speed = pricing_service.speed_european_option(request.dict())
    vega = pricing_service.vega_european_option(request.dict())
    theta = pricing_service.theta_european_option(request.dict())
    rho_rate = pricing_service.rho_rate_european_option(request.dict())
    rho_dividend_yield = pricing_service.rho_dividend_yield_european_option(request.dict())

    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "speed": speed,
        "vega": vega,
        "theta": theta,
        "rho_rate": rho_rate,
        "rho_dividend_yield": rho_dividend_yield
    }


class BinaryOptionPricingRequest(BaseModel):
    spot: float = 100.0
    strike: float = 100.0
    maturity: float = 1.0
    rate: float = 0.02
    dividend_yield: float = 0.05
    volatility: float = 0.2
    option_type: str = "call"
    payout: float = 1.0
    pricing_model: str = "black_scholes"


@app.post("/price/binary")
def price_binary_option(request: BinaryOptionPricingRequest):
    price = pricing_service.price_binary_option(request.dict())
    delta = pricing_service.delta_binary_option(request.dict())
    gamma = pricing_service.gamma_binary_option(request.dict())
    speed = pricing_service.speed_binary_option(request.dict())
    vega = pricing_service.vega_binary_option(request.dict())
    theta = pricing_service.theta_binary_option(request.dict())
    rho_rate = pricing_service.rho_rate_binary_option(request.dict())
    rho_dividend_yield = pricing_service.rho_dividend_yield_binary_option(request.dict())

    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "speed": speed,
        "vega": vega,
        "theta": theta,
        "rho_rate": rho_rate,
        "rho_dividend_yield": rho_dividend_yield
    }

class SwapPricingRequest(BaseModel):
    notional: float
    fixed_rate: float
    payment_dates: list[float]
    rate: float
    floating_spread: float = 0.0
    fixed_rate_payer: bool = True


@app.post("/price/swap")
def price_interest_rate_swap(request: SwapPricingRequest):
    price = pricing_service.price_interest_rate_swap(request.dict())
    return {"price": price}