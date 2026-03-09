from derivatives_pricer.domain.instruments.options.binary_option import BinaryOption
from derivatives_pricer.domain.instruments.options.european_option import EuropeanOption
from derivatives_pricer.domain.models.black_scholes import BlackScholesModel


def test_black_scholes_european_call():

    option = EuropeanOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.02,
        dividend_yield=0.05,
        volatility=0.2,
        option_type="call"
    )

    model = BlackScholesModel()

    price = model.price_european(option)
    delta = model.delta_european(option)
    gamma = model.gamma_european(option)
    speed = model.speed_european(option)
    vega = model.vega_european(option)
    theta = model.theta_european(option)
    rho_rate = model.rho_rate_european(option)
    rho_dividend_yield = model.rho_dividend_yield_european(option)

    assert round(price, 6) == 6.330081
    assert round(delta, 6) == 0.456648
    assert round(gamma, 6) == 0.018951
    assert round(speed, 6) == -0.000142
    assert round(vega, 6) == 37.901158
    assert round(theta, 6) == -2.293569
    assert round(rho_rate, 6) == 39.334753
    assert round(rho_dividend_yield, 6) == -45.664833

def test_black_scholes_european_put():

    option = EuropeanOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.02,
        dividend_yield=0.05,
        volatility=0.2,
        option_type="put"
    )

    model = BlackScholesModel()

    price = model.price_european(option)
    delta = model.delta_european(option)
    gamma = model.gamma_european(option)
    speed = model.speed_european(option)
    vega = model.vega_european(option)
    theta = model.theta_european(option)
    rho_rate = model.rho_rate_european(option)
    rho_dividend_yield = model.rho_dividend_yield_european(option)

    assert round(price, 6) == 9.227006
    assert round(delta, 6) == -0.494581
    assert round(gamma, 6) == 0.018951
    assert round(speed, 6) == -0.000142
    assert round(vega, 6) == 37.901158
    assert round(theta, 6) == -5.089319
    assert round(rho_rate, 6) == -58.685115
    assert round(rho_dividend_yield, 6) == 49.458109

def test_black_scholes_binary_call():

    option = BinaryOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.02,
        dividend_yield=0.05,
        volatility=0.2,
        option_type="call",
        payout=1.0
    )

    model = BlackScholesModel()

    price = model.price_binary(option)
    delta = model.delta_binary(option)
    gamma = model.gamma_binary(option)
    speed = model.speed_binary(option)
    vega = model.vega_binary(option)
    theta = model.theta_binary(option)
    rho_rate = model.rho_rate_binary(option)
    rho_dividend_yield = model.rho_dividend_yield_binary(option)

    assert round(price, 6) == 0.393348
    assert round(delta, 6) == 0.018951
    assert round(gamma, 8) == 0.00004738
    assert round(speed, 8) ==  -0.00004773
    assert round(vega, 6) == 0.094753
    assert round(theta, 6) == 0.055243
    assert round(rho_rate, 6) == 1.501710
    assert round(rho_dividend_yield, 6) == -1.895058

def test_black_scholes_binary_put():

    option = BinaryOption(
        spot=100,
        strike=100,
        maturity=1,
        rate=0.02,
        dividend_yield=0.05,
        volatility=0.2,
        option_type="put",
        payout=1.0
    )

    model = BlackScholesModel()

    price = model.price_binary(option)
    delta = model.delta_binary(option)
    gamma = model.gamma_binary(option)
    speed = model.speed_binary(option)
    vega = model.vega_binary(option)
    theta = model.theta_binary(option)
    rho_rate = model.rho_rate_binary(option)
    rho_dividend_yield = model.rho_dividend_yield_binary(option)

    assert round(price, 6) == 0.586851
    assert round(delta, 6) == -0.018951
    assert round(gamma, 8) == -0.00004738
    assert round(speed, 8) == 0.00004773
    assert round(vega, 6) == -0.094753
    assert round(theta, 6) == -0.035639
    assert round(rho_rate, 6) == -2.481909
    assert round(rho_dividend_yield, 6) == 1.895058
