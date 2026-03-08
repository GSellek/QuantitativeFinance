import math

from functools import cache
from scipy.stats import norm

class Products:
    def __init__(self):
        pass


class Equities(Products):
    pass


class Bonds(Products):
    pass


class Derivatives(Products):
    def __init__(self):
        super().__init__()


class Swap(Derivatives):
    def __init__(self):
        super().__init__()


class Options(Derivatives):
    def __init__(self, dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility):
        super().__init__()
        self.dividend_yield = dividend_yield
        self.interest_rate = interest_rate
        self.strike = strike
        self.time_to_maturity = time_to_maturity
        self.underlying_price = underlying_price
        self.volatility = volatility

    @cache
    def get_d_1(self) -> float:
        d_1 = (math.log(self.underlying_price / self.strike) + (self.interest_rate - self.dividend_yield + self.volatility**2 / 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        return d_1

    @cache
    def get_d_2(self) -> float:
        d_2 = self.get_d_1() - (self.volatility * math.sqrt(self.time_to_maturity))
        return d_2

    def price(self) -> float:
        pass

    def delta(self) -> float:
        pass

    def gamma(self) -> float:
        pass

    def speed(self) -> float:
        pass

    def vega(self) -> float:
        pass

    def theta(self) -> float:
        pass

    def rho_rate(self) -> float:
        pass

    def rho_dividend_yield(self) -> float:
        pass

    def get_greeks(self) -> dict[str,float]:
        greeks = {
            "delta": float(self.delta()),
            "gamma": float(self.gamma()),
            "speed": float(self.speed()),
            "vega": float(self.vega()),
            "theta": float(self.theta()),
            "rho_rate": float(self.rho_rate()),
            "rho_dividend_yield": float(self.rho_dividend_yield())
        }
        return greeks


class EuropeanOptions(Options):
    def __init__(self, dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility, call_put_flag):
        super().__init__(dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility)
        self.call_put_flag = call_put_flag

    def price(self) -> float:
        d_1 = self.get_d_1()
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.time_to_maturity <= 0:
            raise ValueError("Time to maturity must be positive")
        if self.volatility <= 0:
            raise ValueError("Volatility must be positive")
        if self.strike <= 0:
            raise ValueError("Strike price must be positive")
        if self.underlying_price <= 0:
            raise ValueError("Underlying price must be positive")
        if self.call_put_flag == "call":
            price = self.underlying_price * dividend_yield_factor * norm.cdf(d_1) - self.strike * discount_factor * norm.cdf(d_2)
        elif self.call_put_flag == "put":
            price = self.strike * discount_factor * norm.cdf(-d_2) - self.underlying_price * dividend_yield_factor * norm.cdf(-d_1)
        else:
            raise ValueError("Invalid call/put flag")
        return price

    def delta(self) -> float:
        d_1 = self.get_d_1()
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.call_put_flag == "call":
            delta = dividend_yield_factor * norm.cdf(d_1)
        elif self.call_put_flag == "put":
            delta = dividend_yield_factor * (norm.cdf(d_1) - 1)
        else:
            raise ValueError("Invalid call/put flag")
        return delta

    def gamma(self) -> float:
        d_1 = self.get_d_1()
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.call_put_flag == "call":
            gamma = (dividend_yield_factor * norm.pdf(d_1)) / (self.underlying_price * self.volatility * math.sqrt(self.time_to_maturity))
        elif self.call_put_flag == "put":
            gamma = (dividend_yield_factor * norm.pdf(d_1)) / (self.underlying_price * self.volatility * math.sqrt(self.time_to_maturity))
        else:
            raise ValueError("Invalid call/put flag")
        return gamma

    def speed(self) -> float:
        d_1 = self.get_d_1()
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.call_put_flag == "call":
            speed = -(dividend_yield_factor * norm.pdf(d_1)) / (self.volatility ** 2 * self.underlying_price ** 2 * self.time_to_maturity) * (d_1 + self.volatility * math.sqrt(self.time_to_maturity))
        elif self.call_put_flag == "put":
            speed = -(dividend_yield_factor * norm.pdf(d_1)) / (self.volatility ** 2 * self.underlying_price ** 2 * self.time_to_maturity) * (d_1 + self.volatility * math.sqrt(self.time_to_maturity))
        else:
            raise ValueError("Invalid call/put flag")
        return speed

    def vega(self) -> float:
        d_1 = self.get_d_1()
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.call_put_flag == "call":
            vega = self.underlying_price * dividend_yield_factor * norm.pdf(d_1) * math.sqrt(self.time_to_maturity)
        elif self.call_put_flag == "put":
            vega = self.underlying_price * dividend_yield_factor * norm.pdf(d_1) * math.sqrt(self.time_to_maturity)
        else:
            raise ValueError("Invalid call/put flag")
        return vega

    def theta(self) -> float:
        d_1 = self.get_d_1()
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.call_put_flag == "call":
            theta = -self.volatility * self.underlying_price * dividend_yield_factor * norm.pdf(d_1) / (2 * math.sqrt(self.time_to_maturity)) + self.dividend_yield * self.underlying_price * norm.cdf(d_1) * dividend_yield_factor - self.interest_rate * self.strike * discount_factor * norm.cdf(d_2)
        elif self.call_put_flag == "put":
            theta = -self.volatility * self.underlying_price * dividend_yield_factor * norm.pdf(-d_1) / (2 * math.sqrt(self.time_to_maturity)) - self.dividend_yield * self.underlying_price * norm.cdf(-d_1) * dividend_yield_factor + self.interest_rate * self.strike * discount_factor * norm.cdf(-d_2)
        else:
            raise ValueError("Invalid call/put flag")
        return theta

    def rho_rate(self) -> float:
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            rho_rate = self.strike * self.time_to_maturity * discount_factor * norm.cdf(d_2)
        elif self.call_put_flag == "put":
            rho_rate = -self.strike * self.time_to_maturity * discount_factor * norm.cdf(-d_2)
        else:
            raise ValueError("Invalid call/put flag")
        return rho_rate

    def rho_dividend_yield(self) -> float:
        d_1 = self.get_d_1()
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.call_put_flag == "call":
            rho_dividend_yield = -self.time_to_maturity * self.underlying_price * dividend_yield_factor * norm.cdf(d_1)
        elif self.call_put_flag == "put":
            rho_dividend_yield = self.time_to_maturity * self.underlying_price * dividend_yield_factor * norm.cdf(-d_1)
        else:
            raise ValueError("Invalid call/put flag")
        return rho_dividend_yield


class BinaryOptions(Options):
    def __init__(self, dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility, call_put_flag):
        super().__init__(dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility)
        self.call_put_flag = call_put_flag


    def price(self) -> float:
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            price = discount_factor * norm.cdf(d_2)
        elif self.call_put_flag == "put":
            price = discount_factor *  norm.cdf(-d_2)
        else:
            raise ValueError("Invalid call/put flag")
        return price

    def delta(self) -> float:
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            delta = (discount_factor * norm.pdf(d_2)) / (self.volatility * self.underlying_price * math.sqrt(self.time_to_maturity))
        elif self.call_put_flag == "put":
            delta = - (discount_factor * norm.pdf(d_2)) / (self.volatility * self.underlying_price * math.sqrt(self.time_to_maturity))
        else:
            raise ValueError("Invalid call/put flag")
        return delta

    def gamma(self) -> float:
        d_1 = self.get_d_1()
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            gamma = - (discount_factor * d_1 * norm.pdf(d_2)) / (self.volatility ** 2 * self.underlying_price ** 2 * self.time_to_maturity)
        elif self.call_put_flag == "put":
            gamma = (discount_factor * d_1 * norm.pdf(d_2)) / (self.volatility ** 2 * self.underlying_price ** 2 * self.time_to_maturity)
        else:
            raise ValueError("Invalid call/put flag")
        return gamma

    def speed(self) -> float:
        d_1 = self.get_d_1()
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            speed = - (discount_factor * norm.pdf(d_2)) / (self.volatility ** 2 * self.underlying_price ** 3 * self.time_to_maturity) * (-2 * d_1 + (1 - d_1 * d_2)/(self.volatility * math.sqrt(self.time_to_maturity)))
        elif self.call_put_flag == "put":
            speed = (discount_factor * norm.pdf(d_2)) / (self.volatility ** 2 * self.underlying_price ** 3 * self.time_to_maturity) * (-2 * d_1 + (1 - d_1 * d_2)/(self.volatility * math.sqrt(self.time_to_maturity)))
        else:
            raise ValueError("Invalid call/put flag")
        return speed

    def vega(self) -> float:
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            vega = - discount_factor * norm.pdf(d_2) * (math.sqrt(self.time_to_maturity) + d_2 /self.volatility)
        elif self.call_put_flag == "put":
            vega = discount_factor * norm.pdf(d_2) * (math.sqrt(self.time_to_maturity) + d_2 /self.volatility)
        else:
            raise ValueError("Invalid call/put flag")
        return vega

    def theta(self) -> float:
        d_1 = self.get_d_1()
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            theta = self.interest_rate * discount_factor * norm.cdf(d_2) + discount_factor * norm.pdf(d_2) * (d_1 / (2 * self.time_to_maturity) - (self.interest_rate - self.dividend_yield) / (self.volatility * math.sqrt(self.time_to_maturity)))
        elif self.call_put_flag == "put":
            theta = self.interest_rate * discount_factor * (1 - norm.cdf(d_2)) - discount_factor * norm.pdf(d_2) * (d_1 / (2 * self.time_to_maturity) - (self.interest_rate - self.dividend_yield) / (self.volatility * math.sqrt(self.time_to_maturity)))
        else:
            raise ValueError("Invalid call/put flag")
        return theta

    def rho_rate(self) -> float:
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            rho_rate = - self.time_to_maturity * discount_factor * norm.cdf(d_2) + math.sqrt(self.time_to_maturity) / self.volatility * discount_factor * norm.pdf(d_2)
        elif self.call_put_flag == "put":
            rho_rate = - self.time_to_maturity * discount_factor * ( 1 - norm.cdf(d_2)) - math.sqrt(self.time_to_maturity) / self.volatility * discount_factor * norm.pdf(d_2)
        else:
            raise ValueError("Invalid call/put flag")
        return rho_rate

    def rho_dividend_yield(self) -> float:
        d_2 = self.get_d_2()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        if self.call_put_flag == "call":
            rho_dividend_yield = - math.sqrt(self.time_to_maturity) / self.volatility * discount_factor * norm.pdf(d_2)
        elif self.call_put_flag == "put":
            rho_dividend_yield = math.sqrt(self.time_to_maturity) / self.volatility * discount_factor * norm.pdf(d_2)
        else:
            raise ValueError("Invalid call/put flag")
        return rho_dividend_yield


class AsianOptions(Options):
    def __init__(self, dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility, call_put_flag):
        super().__init__(dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility)
        self.call_put_flag = call_put_flag


class LookbackOptions(Options):
    def __init__(self, dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility, call_put_flag):
        super().__init__(dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility)
        self.call_put_flag = call_put_flag


class BarrierOptions(Options):
    def __init__(self, barrier_level, dividend_yield, down_up_flag, in_out_flag, interest_rate, strike, time_to_maturity, underlying_price, volatility, call_put_flag):
        super().__init__(dividend_yield, interest_rate, strike, time_to_maturity, underlying_price, volatility)
        self.barrier_level = barrier_level
        self.call_put_flag = call_put_flag
        self.down_up_flag = down_up_flag
        self.in_out_flag = in_out_flag

    def get_d_3(self) -> float:
        d_3 = (math.log(self.underlying_price / self.barrier_level) + (self.interest_rate - self.dividend_yield + self.volatility ** 2 / 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        return d_3

    def get_d_4(self) -> float:
        d_4 = (math.log(self.underlying_price / self.barrier_level) + (self.interest_rate - self.dividend_yield - self.volatility ** 2 / 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        return d_4

    def get_d_5(self) -> float:
        d_5 = (math.log(self.underlying_price / self.barrier_level) - (self.interest_rate - self.dividend_yield - self.volatility ** 2 / 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        return d_5

    def get_d_6(self) -> float:
        d_6 = (math.log(self.underlying_price / self.barrier_level) - (self.interest_rate - self.dividend_yield + self.volatility ** 2 / 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        return d_6

    def get_d_7(self) -> float:
        d_7 = (math.log(self.underlying_price * self.strike / self.barrier_level ** 2) - (self.interest_rate - self.dividend_yield - self.volatility ** 2 / 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        return d_7

    def get_d_8(self) -> float:
        d_8 = (math.log(self.underlying_price * self.strike / self.barrier_level ** 2) - (self.interest_rate - self.dividend_yield + self.volatility ** 2 / 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        return d_8

    def get_a(self):
        a = (self.barrier_level / self.underlying_price) ** (-1 + (2*(self.interest_rate - self.dividend_yield) / self.volatility ** 2))
        return a

    def get_b(self):
        b = (self.barrier_level / self.underlying_price) ** (1 + (2*(self.interest_rate - self.dividend_yield) / self.volatility ** 2))
        return b

    def price(self) -> float:
        d_1 = self.get_d_1()
        d_2 = self.get_d_2()
        d_3 = self.get_d_3()
        d_4 = self.get_d_4()
        d_5 = self.get_d_5()
        d_6 = self.get_d_6()
        d_7 = self.get_d_7()
        d_8 = self.get_d_8()
        a = self.get_a()
        b = self.get_b()
        discount_factor = math.exp(-self.interest_rate * self.time_to_maturity)
        dividend_yield_factor = math.exp(-self.dividend_yield * self.time_to_maturity)
        if self.call_put_flag == "call":
            if self.down_up_flag == "up":
                if self.in_out_flag == "in":
                    price = self.underlying_price * dividend_yield_factor * (norm.cdf(d_3) + b * (norm.cdf(d_6) - norm.cdf(d_8))) - self.strike * discount_factor * (norm.cdf(d_4) + a * (norm.cdf(d_5) - norm.cdf(d_7)))
                elif self.in_out_flag == "out":
                    price = self.underlying_price * dividend_yield_factor * (norm.cdf(d_1) - norm.cdf(d_3) - b * (norm.cdf(d_6) - norm.cdf(d_8))) - self.strike * discount_factor * (norm.cdf(d_2) - norm.cdf(d_4) - a * (norm.cdf(d_5) - norm.cdf(d_7)))
                else:
                    raise ValueError("Invalid in/out flag")
            elif self.down_up_flag == "down":
                if self.in_out_flag == "in":
                    if self.strike > self.barrier_level:
                        price = self.underlying_price * dividend_yield_factor * b * (1 - norm.cdf(d_8)) - self.strike * discount_factor * a * (1 - norm.cdf(d_7))
                    elif self.strike < self.barrier_level:
                        price = self.underlying_price * dividend_yield_factor * (norm.cdf(d_1) - norm.cdf(d_3) + b * (1 - norm.cdf(d_6))) - self.strike * discount_factor * (norm.cdf(d_2) - norm.cdf(d_4) + a * (1 - norm.cdf(d_5)))
                    else:
                        raise ValueError("Strike must be different than barrier level")
                elif self.in_out_flag == "out":
                    if self.strike > self.barrier_level:
                        price = self.underlying_price * dividend_yield_factor * (norm.cdf(d_1) - b * (1 - norm.cdf(d_8))) - self.strike * discount_factor * (norm.cdf(d_2) - a * (1 - norm.cdf(d_7)))
                    elif self.strike < self.barrier_level:
                        price = self.underlying_price * dividend_yield_factor * (norm.cdf(d_3) - b * (1 - norm.cdf(d_6))) - self.strike * discount_factor * (norm.cdf(d_4) - a * (1 - norm.cdf(d_5)))
                    else:
                        raise ValueError("Strike must be different than barrier level")
                else:
                    raise ValueError("Invalid in/out flag")
            else:
                raise ValueError("Invalid down/up flag")
        elif self.call_put_flag == "put":
            if self.down_up_flag == "up":
                if self.in_out_flag == "in":
                    if self.strike > self.barrier_level:
                        price = -self.underlying_price * dividend_yield_factor * (norm.cdf(d_3) - norm.cdf(d_1) + b * norm.cdf(d_6)) + self.strike * discount_factor * (norm.cdf(d_4) - norm.cdf(d_2) + a * norm.cdf(d_5))
                    elif self.strike < self.barrier_level:
                        price = -self.underlying_price * dividend_yield_factor * b * norm.cdf(d_8) + self.strike * discount_factor * a * norm.cdf(d_7)
                    else:
                        raise ValueError("Strike must be different than barrier level")
                elif self.in_out_flag == "out":
                    if self.strike > self.barrier_level:
                        price = -self.underlying_price * dividend_yield_factor * (1 - norm.cdf(d_3) - b * norm.cdf(d_6)) + self.strike * discount_factor * (1 - norm.cdf(d_4) - a * norm.cdf(d_5))
                    elif self.strike < self.barrier_level:
                        price = -self.underlying_price * dividend_yield_factor * (1 - norm.cdf(d_1) - b * norm.cdf(d_8)) + self.strike * discount_factor * (1 - norm.cdf(d_2) - a * norm.cdf(d_7))
                    else:
                        raise ValueError("Strike must be different than barrier level")
                else:
                    raise ValueError("Invalid in/out flag")
            elif self.down_up_flag == "down":
                if self.in_out_flag == "in":
                    price = -self.underlying_price * dividend_yield_factor * (1 - norm.cdf(d_3) + b * (norm.cdf(d_8) - norm.cdf(d_6))) -+self.strike * discount_factor * (1 - norm.cdf(d_4) + a * (norm.cdf(d_7) - norm.cdf(d_5)))
                elif self.in_out_flag == "out":
                    price = -self.underlying_price * dividend_yield_factor * (norm.cdf(d_3) - norm.cdf(d_1) - b * (norm.cdf(d_8) - norm.cdf(d_6))) + self.strike * discount_factor * (norm.cdf(d_4) - norm.cdf(d_2) - a * (norm.cdf(d_7) - norm.cdf(d_5)))
                else:
                    raise ValueError("Invalid in/out flag")
            else:
                raise ValueError("Invalid down/up flag")
        else:
            raise ValueError("Invalid call/put flag")
        return price


call_option = EuropeanOptions(dividend_yield=0.05, interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Call price: {call_option.price()}")
print(f"Call Greeks: {call_option.get_greeks()}")

put_option = EuropeanOptions(dividend_yield=0.05, interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Put price: {put_option.price()}")
print(f"Put Greeks: {put_option.get_greeks()}")

call_binary_option = BinaryOptions(dividend_yield=0.05, interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Binary call price: {call_binary_option.price()}")
print(f"Binary call Greeks: {call_binary_option.get_greeks()}")

put_binary_option = BinaryOptions(dividend_yield=0.05, interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Binary put price: {put_binary_option.price()}")
print(f"Binary put Greeks: {put_binary_option.get_greeks()}")

up_out_call_barrier_option = BarrierOptions(barrier_level=110, dividend_yield=0.05, down_up_flag="up", in_out_flag="out", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Barrier up-and-out call price: {up_out_call_barrier_option.price()}")

up_in_call_barrier_option = BarrierOptions(barrier_level=110, dividend_yield=0.05, down_up_flag="up", in_out_flag="in", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Barrier up-and-in call price: {up_in_call_barrier_option.price()}")

above_strike_down_out_call_barrier_option = BarrierOptions(barrier_level=120, dividend_yield=0, down_up_flag="down", in_out_flag="out", interest_rate=0.05, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Barrier above-strike-down-and-out call price: {above_strike_down_out_call_barrier_option.price()}")

below_strike_down_out_call_barrier_option = BarrierOptions(barrier_level=80, dividend_yield=0.05, down_up_flag="down", in_out_flag="out", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Barrier below-strike-down-and-out call price: {below_strike_down_out_call_barrier_option.price()}")

above_strike_down_in_call_barrier_option = BarrierOptions(barrier_level=110, dividend_yield=0.05, down_up_flag="down", in_out_flag="in", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Barrier above-strike-down-and-in call price: {above_strike_down_in_call_barrier_option.price()}")

below_strike_down_in_call_barrier_option = BarrierOptions(barrier_level=90, dividend_yield=0.05, down_up_flag="down", in_out_flag="in", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="call")
print(f"Barrier below-strike-down-and-in call price: {below_strike_down_in_call_barrier_option.price()}")

down_out_put_barrier_option = BarrierOptions(barrier_level=50, dividend_yield=0.05, down_up_flag="down", in_out_flag="out", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Barrier down-and-out put price: {down_out_put_barrier_option.price()}")

down_in_put_barrier_option = BarrierOptions(barrier_level=90, dividend_yield=0.05, down_up_flag="down", in_out_flag="in", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Barrier down-and-in put price: {down_in_put_barrier_option.price()}")

above_strike_up_out_put_barrier_option = BarrierOptions(barrier_level=110, dividend_yield=0.05, down_up_flag="up", in_out_flag="out", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Barrier above-strike-up-and-out put price: {above_strike_up_out_put_barrier_option.price()}")

below_strike_up_out_put_barrier_option = BarrierOptions(barrier_level=90, dividend_yield=0.05, down_up_flag="up", in_out_flag="out", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Barrier below-strike-up-and-out put price: {below_strike_up_out_put_barrier_option.price()}")

above_strike_up_in_put_barrier_option = BarrierOptions(barrier_level=110, dividend_yield=0.05, down_up_flag="up", in_out_flag="in", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Barrier above-strike-up-and-in put price: {above_strike_up_in_put_barrier_option.price()}")

below_strike_up_in_put_barrier_option = BarrierOptions(barrier_level=90, dividend_yield=0.05, down_up_flag="up", in_out_flag="in", interest_rate=0.02, strike=100, time_to_maturity=1, underlying_price=100, volatility=0.2, call_put_flag="put")
print(f"Barrier below-strike-up-and-in put price: {below_strike_up_in_put_barrier_option.price()}")
