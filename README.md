# Monte Carlo Option Pricing Simulator

This Streamlit application simulates the price of European Call or Put options using the Monte Carlo method based on the Geometric Brownian Motion model for the underlying asset price.

## Features

- Simulates stock price paths using Geometric Brownian Motion.
- Estimates the price of European Call and Put options.
- Visualizes the simulated price paths and the distribution of final prices.
- Allows users to adjust key parameters:
    - Option Type (Call/Put)
    - Initial Stock Price (S₀)
    - Strike Price (K)
    - Volatility (σ)
    - Risk-free Rate (r)
    - Time to Maturity (T)
    - Number of Simulations

## Setup

1.  **Clone the repository or download the files.**
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the Streamlit app, execute the following command in your terminal from the project directory:

```bash
streamlit run monte-carlo-option.py
```

The application will open in your default web browser. Adjust the parameters in the sidebar to see the simulation results update in real-time.
