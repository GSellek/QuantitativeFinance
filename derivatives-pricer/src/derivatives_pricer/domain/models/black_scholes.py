import numpy as np
from scipy.stats import norm

from derivatives_pricer.domain.instruments.european_option import EuropeanOption


class BlackScholesModel:

    @staticmethod
    def d1(option):
        spot = option.spot
        strike = option.strike
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * sigma ** 2) * tenor) / (sigma * np.sqrt(tenor))

        return d1

    def d2(self, option):
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)

        d2 = d1 - sigma * np.sqrt(tenor)

        return d2

    def discount_factor(self, option):
        tenor = option.maturity
        rate = option.rate

        discount_factor = np.exp(-rate * tenor)

        return discount_factor

    def dividend_yield_factor(self, option):
        tenor = option.maturity
        dividend_yield = option.dividend_yield

        dividend_yield_factor = np.exp(-dividend_yield * tenor)

        return dividend_yield_factor

    def price_european(self, option):
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

    def delta_european(self, option):
        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call":
            delta = dividend_yield_factor * norm.cdf(d1)
        else:
            delta = dividend_yield_factor * (norm.cdf(d1) - 1)

        return delta

    def gamma_european(self, option):
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        gamma = (dividend_yield_factor * norm.pdf(d1)) / (spot * sigma * np.sqrt(tenor))

        return gamma

    def speed_european(self, option):
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        speed = -(dividend_yield_factor * norm.pdf(d1)) / (sigma ** 2 * spot ** 2 * tenor) * (d1 + sigma * np.sqrt(tenor))

        return speed

    def vega_european(self, option):
        spot = option.spot
        tenor = option.maturity

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        vega = spot * dividend_yield_factor * norm.pdf(d1) * np.sqrt(tenor)

        return vega

    def theta_european(self, option):
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

    def rho_rate_european(self, option):
        strike = option.strike
        tenor = option.maturity

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            rho_rate = strike * tenor * discount_factor * norm.cdf(d2)
        else:
            rho_rate = -strike * tenor * discount_factor * norm.cdf(-d2)

        return rho_rate

    def rho_dividend_yield_european(self, option):
        spot = option.spot
        tenor = option.maturity

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

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