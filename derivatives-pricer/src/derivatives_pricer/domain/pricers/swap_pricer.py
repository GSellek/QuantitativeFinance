class SwapPricer:

    def __init__(self, yield_curve):
        self.yield_curve = yield_curve

    def price(self, swap):

        fixed_leg = 0.0
        float_leg = 0.0

        dates = swap.payment_dates

        for i in range(1, len(dates)):
            t_previous = dates[i - 1]
            t_current = dates[i]
            tau = t_current - t_previous

            discount_factor = self.yield_curve.discount(t_current)

            fixed_leg += swap.notional * swap.fixed_rate * tau * discount_factor

            forward_rate = self.yield_curve.forward_rate(t_previous, t_current)
            float_leg += swap.notional * (forward_rate + swap.floating_spread) * tau * discount_factor

        if swap.fixed_rate_payer:
            return float_leg - fixed_leg
        else:
            return fixed_leg - float_leg