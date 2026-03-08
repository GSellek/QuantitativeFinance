from fastapi import FastAPI
from pydantic import BaseModel
from derivatives_pricer.app.pricing_service import PricingService

app = FastAPI(title="Derivatives Pricer API")

pricing_service = PricingService()

class PricingRequest(BaseModel):
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: str

@app.post("/price/european")
def price_option(request: PricingRequest):
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


class BinaryPricingRequest(BaseModel):
    spot: float
    strike: float
    maturity: float
    rate: float
    dividend_yield: float
    volatility: float
    option_type: str
    payout: float = 1.0


@app.post("/price/binary")
def price_binary_option(request: BinaryPricingRequest):
    price = pricing_service.price_binary_option(request.dict())
    return {
        "price": price
    }