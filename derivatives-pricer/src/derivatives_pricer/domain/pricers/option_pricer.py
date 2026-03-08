class OptionPricer:

    def __init__(self, model):
        self.model = model

    def price(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.price_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.price_binary(option)

        raise ValueError("Unsupported instrument type")

    def delta(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.delta_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.delta_binary(option)

        raise ValueError("Unsupported instrument type")

    def gamma(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.gamma_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.gamma_binary(option)

        raise ValueError("Unsupported instrument type")

    def speed(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.speed_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.speed_binary(option)

        raise ValueError("Unsupported instrument type")

    def vega(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.vega_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.vega_binary(option)

        raise ValueError("Unsupported instrument type")

    def theta(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.theta_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.theta_binary(option)

        raise ValueError("Unsupported instrument type")

    def rho_rate(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.rho_rate_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.rho_rate_binary(option)

        raise ValueError("Unsupported instrument type")

    def rho_dividend_yield(self, option):

        if option.__class__.__name__ == "EuropeanOption":
            return self.model.rho_dividend_yield_european(option)

        if option.__class__.__name__ == "BinaryOption":
            return self.model.rho_dividend_yield_binary(option)

        raise ValueError("Unsupported instrument type")
