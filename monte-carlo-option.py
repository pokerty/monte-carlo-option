import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import math

# Function to calculate the option payoff based on option type
def calculate_option_payoff(option_type, stock_price, strike_price):
    if option_type == "Call":
        return max(stock_price - strike_price, 0)
    elif option_type == "Put":
        return max(strike_price - stock_price, 0)

# Function to perform Monte Carlo simulation for option pricing and visualize results
def monte_carlo_option_pricing(option_type, stock_price, strike_price, volatility, risk_free_rate, time_to_maturity, num_simulations):
    dt = time_to_maturity / 252  # Assuming 252 trading days in a year
    option_payoffs = []
    price_paths = []

    for _ in range(num_simulations):
        price_path = []
        stock_price_copy = stock_price

        for _ in range(int(252 * time_to_maturity)):
            drift = (risk_free_rate - 0.5 * volatility**2) * dt
            shock = volatility * math.sqrt(dt) * np.random.normal(0, 1)
            stock_price_copy *= math.exp(drift + shock)
            price_path.append(stock_price_copy)

        price_paths.append(price_path)
        option_payoff = calculate_option_payoff(option_type, stock_price_copy, strike_price)
        option_payoffs.append(option_payoff)

    option_price = np.exp(-risk_free_rate * time_to_maturity) * np.mean(option_payoffs)
    return option_price, price_paths

# set layout to wide
st.set_page_config(layout="wide")

st.title("Monte Carlo Simulation for Option Pricing")
st.write("This app performs Monte Carlo simulation for option pricing and visualizes the simulated price paths.")

# Sidebar for input parameters
st.sidebar.header("Input Parameters")
option_type = st.sidebar.selectbox(
    "Option Type", ("Call", "Put"), help="Select Call or Put option"
)
stock_price = st.sidebar.number_input(
    "Stock Price (S₀)", value=100.0, min_value=0.1, step=1.0, format="%.2f", help="Initial asset price"
)
strike_price = st.sidebar.number_input(
    "Strike Price (K)", value=100.0, min_value=0.1, step=1.0, format="%.2f", help="Option's strike price"
)
volatility = st.sidebar.slider(
    "Volatility (σ)", min_value=0.01, max_value=1.0, value=0.2, step=0.01, format="%.2f", help="Annual volatility"
)
risk_free_rate = st.sidebar.slider(
    "Risk-free Rate (r)", min_value=0.0, max_value=0.2, value=0.05, step=0.005, format="%.3f", help="Annual risk-free rate"
)
time_to_maturity = st.sidebar.slider(
    "Time to Maturity (T, years)", min_value=0.1, max_value=5.0, value=1.0, step=0.1, format="%.1f", help="Time until expiration"
)
num_simulations = st.sidebar.slider(
    "Number of Simulations", min_value=10, max_value=5000, value=10, step=10, help="Number of Monte Carlo paths"
)

# Run simulation and display results
if stock_price > 0 and strike_price > 0 and time_to_maturity > 0 and num_simulations > 0:
    with st.spinner("Running simulations..."):
        option_price, price_paths = monte_carlo_option_pricing(
            option_type,
            stock_price,
            strike_price,
            volatility,
            risk_free_rate,
            time_to_maturity,
            num_simulations,
        )
    st.metric(
        f"Estimated {option_type} Option Price", f"${option_price:.2f}"
    )
    # Prepare plots side by side
    final_prices = [path[-1] for path in price_paths]
    col1, col2 = st.columns([0.4, 0.6], gap="large")
    with col1:
        st.markdown("#### Distribution of Final Prices")
        fig_hist = px.histogram(
            x=final_prices,
            nbins=50,
            labels={"x": "Final Stock Price"},
        )
        fig_hist.add_vline(
            x=strike_price,
            line_dash="dash",
            line_color="red",
            annotation_text="Strike Price",
            annotation_position="top right",
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    with col2:
        st.markdown("#### Simulated Price Paths")
        df_paths = pd.DataFrame(price_paths).T
        df_paths.index.name = "Time Step"
        fig_paths = px.line(
            df_paths,
            labels={"index": "Time Step", "value": "Stock Price"},
        )
        fig_paths.add_hline(
            y=strike_price,
            line_dash="dash",
            line_color="red",
            annotation_text="Strike Price",
            annotation_position="bottom right",
        )
        fig_paths.update_layout(showlegend=False)
        st.plotly_chart(fig_paths, use_container_width=True)
else:
    st.warning("Enter valid parameters (>0) to run the simulation.")