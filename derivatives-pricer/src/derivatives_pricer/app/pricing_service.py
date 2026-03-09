from derivatives_pricer.domain.instruments.options.binary_option import BinaryOption
from derivatives_pricer.domain.instruments.options.european_option import EuropeanOption
from derivatives_pricer.domain.models.black_scholes import BlackScholesModel
from derivatives_pricer.domain.pricers.option_pricer import OptionPricer

class PricingService:

    def __init__(self):
        self.pricer = OptionPricer(BlackScholesModel())

    def price_european_option(self, request: dict) -> float:

        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.price(option)

    def delta_european_option(self, request: dict) -> float:
        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.delta(option)

    def gamma_european_option(self, request: dict) -> float:
        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.gamma(option)

    def speed_european_option(self, request: dict) -> float:
        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.speed(option)

    def vega_european_option(self, request: dict) -> float:
        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.vega(option)

    def theta_european_option(self, request: dict) -> float:
        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.theta(option)

    def rho_rate_european_option(self, request: dict) -> float:
        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.rho_rate(option)

    def rho_dividend_yield_european_option(self, request: dict) -> float:
        option = EuropeanOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
        )

        return self.pricer.rho_dividend_yield(option)

    def price_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.price(option)

    def delta_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.delta(option)

    def gamma_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.gamma(option)

    def speed_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.speed(option)

    def vega_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.vega(option)

    def theta_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.theta(option)

    def rho_rate_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.rho_rate(option)

    def rho_dividend_yield_binary_option(self, request: dict) -> float:
        option = BinaryOption(
            spot=request["spot"],
            strike=request["strike"],
            maturity=request["maturity"],
            rate=request["rate"],
            dividend_yield=request["dividend_yield"],
            volatility=request["volatility"],
            option_type=request["option_type"],
            payout=request.get("payout", 1.0)
        )

        return self.pricer.rho_dividend_yield(option)