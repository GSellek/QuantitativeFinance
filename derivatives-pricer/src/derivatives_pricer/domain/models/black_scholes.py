import numpy as np
from scipy.stats import norm

from derivatives_pricer.domain.models.pricing_model import PricingModel

_VALID_OPTION_TYPES = {"call", "put"}


def _validate_option_type(option_type: str) -> None:
    if option_type not in _VALID_OPTION_TYPES:
        raise ValueError(f"Invalid option type '{option_type}'. Expected one of {_VALID_OPTION_TYPES}.")

class BlackScholesModel(PricingModel):

    @staticmethod
    def d1(option) -> float:
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma ** 2) * tenor) / (sigma * np.sqrt(tenor))

        return d1

    def d2(self, option) -> float:
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)

        d2 = d1 - sigma * np.sqrt(tenor)

        return d2

    @staticmethod
    def discount_factor(option) -> float:
        tenor = option.maturity
        rate = option.rate

        discount_factor = np.exp(-rate * tenor)

        return discount_factor

    @staticmethod
    def dividend_yield_factor(option) -> float:
        tenor = option.maturity
        dividend_yield = option.dividend_yield

        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        return dividend_yield_factor

    def price_european(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        strike = option.strike

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call":
            price = spot * dividend_yield_factor * norm.cdf(d1) - strike * discount_factor * norm.cdf(d2)
        else:
            price = strike * discount_factor * norm.cdf(-d2) - spot * dividend_yield_factor * norm.cdf(-d1)

        return price

    def delta_european(self, option) -> float:
        _validate_option_type(option.option_type)
        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call":
            delta = dividend_yield_factor * norm.cdf(d1)
        else:
            delta = dividend_yield_factor * (norm.cdf(d1) - 1)

        return delta

    def gamma_european(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        gamma = (dividend_yield_factor * norm.pdf(d1)) / (spot * sigma * np.sqrt(tenor))

        return gamma

    def speed_european(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        speed = -(dividend_yield_factor * norm.pdf(d1)) / (sigma ** 2 * spot ** 2 * tenor) * (d1 + sigma * np.sqrt(tenor))

        return speed

    def vega_european(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        tenor = option.maturity

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        vega = spot * dividend_yield_factor * norm.pdf(d1) * np.sqrt(tenor)

        return vega

    def theta_european(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call":
            theta = -sigma * spot * dividend_yield_factor * norm.pdf(d1) / (2 * np.sqrt(tenor)) + dividend_yield * spot * norm.cdf(d1) * dividend_yield_factor - rate * strike * discount_factor * norm.cdf(d2)
        else:
            theta = -sigma * spot * dividend_yield_factor * norm.pdf(-d1) / (2 * np.sqrt(tenor)) - dividend_yield * spot * norm.cdf(-d1) * dividend_yield_factor + rate * strike * discount_factor * norm.cdf(-d2)

        return theta

    def rho_rate_european(self, option) -> float:
        _validate_option_type(option.option_type)
        strike = option.strike
        tenor = option.maturity

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            rho_rate = strike * tenor * discount_factor * norm.cdf(d2)
        else:
            rho_rate = -strike * tenor * discount_factor * norm.cdf(-d2)

        return rho_rate

    def rho_dividend_yield_european(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        tenor = option.maturity

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call":
            rho_dividend_yield = -tenor * spot * dividend_yield_factor * norm.cdf(d1)
        else:
            rho_dividend_yield = tenor * spot * dividend_yield_factor * norm.cdf(-d1)

        return rho_dividend_yield

    def price_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        payout = option.payout

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            price = payout * discount_factor * norm.cdf(d2)
        else:
            price = payout * discount_factor * norm.cdf(-d2)

        return price

    def delta_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            delta = (discount_factor * norm.pdf(d2)) / (sigma * spot * np.sqrt(tenor))
        else:
            delta = - (discount_factor * norm.pdf(d2)) / (sigma * spot * np.sqrt(tenor))

        return delta

    def gamma_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            gamma = - (discount_factor * d1 * norm.pdf(d2)) / (sigma ** 2 * spot ** 2 * tenor)
        else:
            gamma = (discount_factor * d1 * norm.pdf(d2)) / (sigma ** 2 * spot ** 2 * tenor)

        return gamma

    def speed_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            speed = - (discount_factor * norm.pdf(d2)) / (sigma ** 2 * spot ** 3 * tenor) * (-2 * d1 + (1 - d1 * d2) / (sigma * np.sqrt(tenor)))
        else:
            speed = (discount_factor * norm.pdf(d2)) / (sigma ** 2 * spot ** 3 * tenor) * (-2 * d1 + (1 - d1 * d2) / (sigma * np.sqrt(tenor)))

        return speed

    def vega_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        tenor = option.maturity
        sigma = option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            vega = - discount_factor * norm.pdf(d2) * (np.sqrt(tenor) + d2 / sigma)
        else:
            vega = discount_factor * norm.pdf(d2) * (np.sqrt(tenor) + d2 / sigma)

        return vega

    def theta_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            theta = rate * discount_factor * norm.cdf(d2) + discount_factor * norm.pdf(d2) * (d1 / (2 * tenor) - (rate - dividend_yield) / (sigma * np.sqrt(tenor)))
        else:
            theta = rate * discount_factor * (1 - norm.cdf(d2)) - discount_factor * norm.pdf(d2) * (d1 / (2 * tenor) - (rate - dividend_yield) / (sigma * np.sqrt(tenor)))

        return theta

    def rho_rate_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        tenor = option.maturity
        sigma= option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            rho_rate = - tenor * discount_factor * norm.cdf(d2) + np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)
        else:
            rho_rate = - tenor * discount_factor * (1 - norm.cdf(d2)) - np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)

        return rho_rate

    def rho_dividend_yield_binary(self, option) -> float:
        _validate_option_type(option.option_type)
        tenor = option.maturity
        sigma = option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            rho_dividend_yield = - np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)
        else:
            rho_dividend_yield = np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)

        return rho_dividend_yield