from nicegui import ui
from products import (BarrierOptions,
					  BinaryOptions,
					  EuropeanOptions
					  )

input_width = "w-44"

ui.label("Black-Scholes Option Pricer").classes("text-2xl font-bold")

with ui.row():
	option_type = ui.select(
		options=["Vanilla", "Binary", "Barrier"],
		value="Vanilla",
		label="Option Type",
	).classes(input_width)

with ui.row():
	underlying_price = ui.number(label="Underlying Price", value=100.0).classes(input_width)
	strike = ui.number(label="Strike", value=100.0).classes(input_width)
	time_to_maturity = ui.number(label="Time to Maturity (Years)", value=1.0).classes(input_width)

with ui.row():
	interest_rate = ui.number(label="Interest Rate", value=0.02).classes(input_width)
	dividend_yield = ui.number(label="Dividend Yield", value=0.01).classes(input_width)
	volatility = ui.number(label="Volatility", value=0.20).classes(input_width)

with ui.row():
	call_put_flag = ui.select(
		options=["call", "put"],
		value="call",
		label="Call/Put ",
	).classes(input_width)

with ui.row():
	barrier_level = ui.number(label="Barrier Level", value=110).classes(input_width)
	down_up_flag = ui.select(
		options=["down", "up"],
		value="down",
		label="Down/Up ",
	).classes(input_width)
	in_out_flag = ui.select(
		options=["in", "out"],
		value="in",
		label="In/Out ",
	).classes(input_width)

with ui.card().classes("w-64"):
	ui.label("Result").classes("font-bold")
	result_label = ui.label("—").classes("text-lg font-bold")


def calculate_price():
	try:
		if option_type.value == "Vanilla":
			price = EuropeanOptions(
				dividend_yield=dividend_yield.value,
				interest_rate=interest_rate.value,
				strike=strike.value,
				time_to_maturity=time_to_maturity.value,
				underlying_price=underlying_price.value,
				volatility=volatility.value,
				call_put_flag=call_put_flag.value
			).price()
		elif option_type.value == "Binary":
			price = BinaryOptions(
				dividend_yield=dividend_yield.value,
				interest_rate=interest_rate.value,
				strike=strike.value,
				time_to_maturity=time_to_maturity.value,
				underlying_price=underlying_price.value,
				volatility=volatility.value,
				call_put_flag=call_put_flag.value
			).price()
		elif option_type.value == "Barrier":
			price = BarrierOptions(
				barrier_level=barrier_level.value,
				dividend_yield=dividend_yield.value,
				down_up_flag=down_up_flag.value,
				in_out_flag=in_out_flag.value,
				interest_rate=interest_rate.value,
				strike=strike.value,
				time_to_maturity=time_to_maturity.value,
				underlying_price=underlying_price.value,
				volatility=volatility.value,
				call_put_flag=call_put_flag.value
			).price()
		else:
			raise ValueError("Invalid option type")
		result_label.set_text(f"Option Price: {price:.4f}")
	except Exception as e:
		result_label.set_text(f"Error: {e}")


ui.button("Calculate Price", on_click=calculate_price).classes("mt-4")

ui.run()