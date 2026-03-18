class OptionPricer:

    def __init__(self, model):
        self.model = model

    def _dispatch(self, metric: str, option) -> float:
        key = option.instrument_key
        method_name = f"{metric}_{key}"
        method = getattr(self.model, method_name, None)
        if method is None:
            raise ValueError(
                f"Model '{type(self.model).__name__}' does not support "
                f"'{method_name}' for instrument '{type(option).__name__}'"
            )
        return method(option)

    def price(self, option) -> float:
        return self._dispatch(metric="price", option=option)

    def delta(self, option) -> float:
        return self._dispatch(metric="delta", option=option)

    def gamma(self, option) -> float:
        return self._dispatch(metric="gamma", option=option)

    def speed(self, option) -> float:
        return self._dispatch(metric="speed", option=option)

    def vega(self, option) -> float:
        return self._dispatch(metric="vega", option=option)

    def theta(self, option) -> float:
        return self._dispatch(metric="theta", option=option)

    def rho_rate(self, option) -> float:
        return self._dispatch(metric="rho_rate", option=option)

    def rho_dividend_yield(self, option) -> float:
        return self._dispatch(metric="rho_dividend_yield", option=option)