import numpy as np
from scipy.stats import norm


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

    @staticmethod
    def discount_factor(option):
        tenor = option.maturity
        rate = option.rate

        discount_factor = np.exp(-rate * tenor)

        return discount_factor

    @staticmethod
    def dividend_yield_factor(option):
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
        elif option.option_type == "put":
            price = strike * discount_factor * norm.cdf(-d2) - spot * dividend_yield_factor * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type")

        return price

    def delta_european(self, option):
        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call":
            delta = dividend_yield_factor * norm.cdf(d1)
        elif option.option_type == "put":
            delta = dividend_yield_factor * (norm.cdf(d1) - 1)
        else:
            raise ValueError("Invalid option type")

        return delta

    def gamma_european(self, option):
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call" or option.option_type == "put":
            gamma = (dividend_yield_factor * norm.pdf(d1)) / (spot * sigma * np.sqrt(tenor))
        else:
            raise ValueError("Invalid option type")

        return gamma

    def speed_european(self, option):
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call" or option.option_type == "put":
            speed = -(dividend_yield_factor * norm.pdf(d1)) / (sigma ** 2 * spot ** 2 * tenor) * (d1 + sigma * np.sqrt(tenor))
        else:
            raise ValueError("Invalid option type")

        return speed

    def vega_european(self, option):
        spot = option.spot
        tenor = option.maturity

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call" or option.option_type == "put":
            vega = spot * dividend_yield_factor * norm.pdf(d1) * np.sqrt(tenor)
        else:
            raise ValueError("Invalid option type")

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
        elif option.option_type == "put":
            theta = -sigma * spot * dividend_yield_factor * norm.pdf(-d1) / (2 * np.sqrt(tenor)) - dividend_yield * spot * norm.cdf(-d1) * dividend_yield_factor + rate * strike * discount_factor * norm.cdf(-d2)
        else:
            raise ValueError("Invalid option type")

        return theta

    def rho_rate_european(self, option):
        strike = option.strike
        tenor = option.maturity

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            rho_rate = strike * tenor * discount_factor * norm.cdf(d2)
        elif option.option_type == "put":
            rho_rate = -strike * tenor * discount_factor * norm.cdf(-d2)
        else:
            raise ValueError("Invalid option type")

        return rho_rate

    def rho_dividend_yield_european(self, option):
        spot = option.spot
        tenor = option.maturity

        d1 = self.d1(option)
        dividend_yield_factor = self.dividend_yield_factor(option)

        if option.option_type == "call":
            rho_dividend_yield = -tenor * spot * dividend_yield_factor * norm.cdf(d1)
        elif option.option_type == "put":
            rho_dividend_yield = tenor * spot * dividend_yield_factor * norm.cdf(-d1)
        else:
            raise ValueError("Invalid option type")

        return rho_dividend_yield

    def price_binary(self, option) -> float:
        payout = option.payout

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            price = payout * discount_factor * norm.cdf(d2)
        elif option.option_type == "put":
            price = payout * discount_factor * norm.cdf(-d2)
        else:
            raise ValueError("Invalid option type")

        return price

    def delta_binary(self, option) -> float:
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            delta = (discount_factor * norm.pdf(d2)) / (sigma * spot * np.sqrt(tenor))
        elif option.option_type == "put":
            delta = - (discount_factor * norm.pdf(d2)) / (sigma * spot * np.sqrt(tenor))
        else:
            raise ValueError("Invalid option type")

        return delta

    def gamma_binary(self, option):
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            gamma = - (discount_factor * d1 * norm.pdf(d2)) / (sigma ** 2 * spot ** 2 * tenor)
        elif option.option_type == "put":
            gamma = (discount_factor * d1 * norm.pdf(d2)) / (sigma ** 2 * spot ** 2 * tenor)
        else:
            raise ValueError("Invalid option type")

        return gamma

    def speed_binary(self, option):
        spot = option.spot
        tenor = option.maturity
        sigma = option.volatility

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            speed = - (discount_factor * norm.pdf(d2)) / (sigma ** 2 * spot ** 3 * tenor) * (-2 * d1 + (1 - d1 * d2) / (sigma * np.sqrt(tenor)))
        elif option.option_type == "put":
            speed = (discount_factor * norm.pdf(d2)) / (sigma ** 2 * spot ** 3 * tenor) * (-2 * d1 + (1 - d1 * d2) / (sigma * np.sqrt(tenor)))
        else:
            raise ValueError("Invalid option type")

        return speed

    def vega_binary(self, option):
        tenor = option.maturity
        sigma = option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            vega = - discount_factor * norm.pdf(d2) * (np.sqrt(tenor) + d2 / sigma)
        elif option.option_type == "put":
            vega = discount_factor * norm.pdf(d2) * (np.sqrt(tenor) + d2 / sigma)
        else:
            raise ValueError("Invalid option type")

        return vega

    def theta_binary(self, option):
        tenor = option.maturity
        rate = option.rate
        dividend_yield = option.dividend_yield
        sigma = option.volatility

        d1 = self.d1(option)
        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            theta = rate * discount_factor * norm.cdf(d2) + discount_factor * norm.pdf(d2) * (d1 / (2 * tenor) - (rate - dividend_yield) / (sigma * np.sqrt(tenor)))
        elif option.option_type == "put":
            theta = rate * discount_factor * (1 - norm.cdf(d2)) - discount_factor * norm.pdf(d2) * (d1 / (2 * tenor) - (rate - dividend_yield) / (sigma * np.sqrt(tenor)))
        else:
            raise ValueError("Invalid option type")

        return theta

    def rho_rate_binary(self, option):
        tenor = option.maturity
        sigma= option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            rho_rate = - tenor * discount_factor * norm.cdf(d2) + np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)
        elif option.option_type == "put":
            rho_rate = - tenor * discount_factor * (1 - norm.cdf(d2)) - np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)
        else:
            raise ValueError("Invalid option type")

        return rho_rate

    def rho_dividend_yield_binary(self, option):
        tenor = option.maturity
        sigma = option.volatility

        d2 = self.d2(option)
        discount_factor = self.discount_factor(option)

        if option.option_type == "call":
            rho_dividend_yield = - np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)
        elif option.option_type == "put":
            rho_dividend_yield = np.sqrt(tenor) / sigma * discount_factor * norm.pdf(d2)
        else:
            raise ValueError("Invalid option type")

        return rho_dividend_yield