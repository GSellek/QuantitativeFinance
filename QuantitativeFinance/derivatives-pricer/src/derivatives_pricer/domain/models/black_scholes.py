import numpy as np
from scipy.stats import norm

class BlackScholesModel:

    @staticmethod
    def price_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))
        d2 = d1 - sigma * np.sqrt(tenor)

        discount_factor = np.exp(-rate * tenor)
        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        if option.option_type == "call":
            price = spot * dividend_yield_factor * norm.cdf(d1) - strike * discount_factor * norm.cdf(d2)
        else:
            price = strike * discount_factor * norm.cdf(-d2) - spot * dividend_yield_factor * norm.cdf(-d1)

        return price

    @staticmethod
    def delta_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))

        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        if option.option_type == "call":
            delta = dividend_yield_factor * norm.cdf(d1)
        else:
            delta = dividend_yield_factor * (norm.cdf(d1) - 1)

        return delta

    @staticmethod
    def gamma_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))

        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        gamma = (dividend_yield_factor * norm.pdf(d1)) / (spot * sigma * np.sqrt(tenor))

        return gamma

    @staticmethod
    def speed_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))

        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        speed = -(dividend_yield_factor * norm.pdf(d1)) / (sigma ** 2 * spot ** 2 * tenor) * (d1 + sigma * np.sqrt(tenor))

        return speed

    @staticmethod
    def vega_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))

        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        vega = spot * dividend_yield_factor * norm.pdf(d1) * np.sqrt(tenor)

        return vega

    @staticmethod
    def theta_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))
        d2 = d1 - sigma * np.sqrt(tenor)

        discount_factor = np.exp(-rate * tenor)
        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        if option.option_type == "call":
            theta = -sigma * spot * dividend_yield_factor * norm.pdf(d1) / (2 * np.sqrt(tenor)) + dividend_yield * spot * norm.cdf(d1) * dividend_yield_factor - rate * strike * discount_factor * norm.cdf(d2)
        else:
            theta = -sigma * spot * dividend_yield_factor * norm.pdf(-d1) / (2 * np.sqrt(tenor)) - dividend_yield * spot * norm.cdf(-d1) * dividend_yield_factor + rate * strike * discount_factor * norm.cdf(-d2)

        return theta

    @staticmethod
    def rho_rate_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))
        d2 = d1 - sigma * np.sqrt(tenor)

        discount_factor = np.exp(-rate * tenor)

        if option.option_type == "call":
            rho_rate = strike * tenor * discount_factor * norm.cdf(d2)
        else:
            rho_rate = -strike * tenor * discount_factor * norm.cdf(-d2)

        return rho_rate

    @staticmethod
    def rho_dividend_yield_european(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma**2) * tenor) / (sigma * np.sqrt(tenor))

        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        if option.option_type == "call":
            rho_dividend_yield = -tenor * spot * dividend_yield_factor * norm.cdf(d1)
        else:
            rho_dividend_yield = tenor * spot * dividend_yield_factor * norm.cdf(-d1)

        return rho_dividend_yield

    @staticmethod
    def price_binary(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility
        payout = option.payout

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma ** 2) * tenor) / (sigma * np.sqrt(tenor))
        d2 = d1 - sigma * np.sqrt(tenor)

        discount_factor = np.exp(-rate * tenor)

        if option.option_type == "call":
            price = payout * discount_factor * norm.cdf(d2)
        else:
            price = payout * discount_factor * norm.cdf(-d2)

        return price