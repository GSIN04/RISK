import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Step 1: Set up the app title and disclaimer
st.title("Risk Tolerance Assessment Tool")
st.write("""
This Risk Tolerance Assessment Tool is designed to help gauge your tolerance for risk and provide a potential portfolio allocation that meets your tolerance.
""")
st.write("""
**Disclaimer:** This tool is for educational and informational purposes only and does not constitute financial advice. 
The risk assessment and asset allocations are based on general assumptions and may not be suitable for all investors. 
Please consult with a qualified financial advisor before making any investment decisions.
""")

# Initialize session state
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = None
if 'description' not in st.session_state:
    st.session_state.description = ""
if 'show_portfolio' not in st.session_state:
    st.session_state.show_portfolio = False
if 'portfolio_generated' not in st.session_state:
    st.session_state.portfolio_generated = False
if 'start_date' not in st.session_state:
    st.session_state.start_date = None
if 'end_date' not in st.session_state:
    st.session_state.end_date = None
if 'initial_investment' not in st.session_state:
    st.session_state.initial_investment = 10000  


st.header("Answer the following questions to determine your risk tolerance level:")

questions = [
    "What is your primary investment goal?",
    "How long do you plan to keep your investments before you start needing the money?",
    "How often do you expect to adjust or rebalance your portfolio?",
    "How do you feel about short-term fluctuations in your investment value?",
    "What level of return do you expect from your investments?",
    "If your investment portfolio decreased by 25% in one year, how would you likely respond?",
    "How much of a temporary decline in your portfolio could you tolerate without getting anxious?",
    "How experienced are you with investing in financial markets?",
    "What would you prefer if you had to choose between stability and growth?",
    "How often do you review your investment portfolio?"
]

choices = [
    ["Preserve capital with minimal risk", "Generate steady income with limited risk", "Achieve moderate growth with some risk", "Pursue substantial growth with high risk", "Maximize long-term growth with very high risk"],
    ["Less than 1 year", "1 to 3 years", "3 to 5 years", "5 to 10 years", "More than 10 years"],
    ["Never, prefer to set it and forget it", "Rarely, only when absolutely necessary", "Occasionally, based on market conditions", "Regularly, to optimize for performance", "Frequently, to capitalize on short-term market movements"],
    ["Extremely uncomfortable and prefer no fluctuations", "Very uncomfortable, prefer limited fluctuations", "Neutral, can tolerate some fluctuations", "Comfortable, expect moderate fluctuations", "Very comfortable, fluctuations do not bother me"],
    ["Very low returns (1-2%) with minimal risk", "Low returns (3-5%) with minimal to low risk", "Moderate returns (6-8%) with moderate risk", "High returns (9-12%) with high risk", "Very high returns (13% or more) with substantial risk"],
    ["Sell all investments to avoid further losses", "Rebalance to a more conservative portfolio", "Hold steady and wait for recovery", "Invest more to take advantage of lower prices", "Increase exposure to high-risk, high-reward investments"],
    ["Less than 5%", "5% to 10%", "10% to 15%", "15% to 20%", "More than 20%"],
    ["No experience", "Limited experience, mostly in low-risk investments", "Moderate experience, comfortable with a balanced portfolio", "Significant experience, comfortable with a variety of investments", "Extensive experience, comfortable with high-risk investments"],
    ["Maximum stability, even if it means very low growth", "Mostly stability with limited growth potential", "Balance between growth and stability", "Emphasis on growth with some risk", "Maximum growth, regardless of the risk"],
    ["Annually", "Quarterly", "Monthly", "Weekly", "Daily"]
]

user_answers = []
for i, question in enumerate(questions):
    user_answer = st.radio(question, choices[i], key=f"q{i+1}", index=None)
    user_answers.append(user_answer)


investment_duration = user_answers[1]
end_date = datetime.today()
if investment_duration == "Less than 1 year":
    start_date = end_date - timedelta(days=365)
elif investment_duration == "1 to 3 years":
    start_date = end_date - timedelta(days=3*365)
elif investment_duration == "3 to 5 years":
    start_date = end_date - timedelta(days=5*365)
elif investment_duration == "5 to 10 years":
    start_date = end_date - timedelta(days=10*365)
else:
    start_date = end_date - timedelta(days=20*365)  # Assume max 20 years for "More than 10 years"

st.session_state.start_date = start_date
st.session_state.end_date = end_date

# Step 4: Check if all questions are answered and show results
if st.button("See Results"):
    if None in user_answers:
        st.warning("Please answer all the questions before viewing the results.")
    else:
        # Calculate the total score
        total_score = sum(choices[i].index(answer) + 1 for i, answer in enumerate(user_answers))

        # Determine risk tolerance level with enhanced descriptions
        if total_score <= 15:
            st.session_state.risk_level = "Conservative"
            st.session_state.description = (
                "A **Conservative** portfolio aims to preserve capital and minimize risk. "
                "This type of portfolio typically consists of a high percentage of bonds and cash, "
                "with a small allocation to stocks. It is suited for investors who prioritize stability "
                "and capital preservation over high returns. Expected returns are lower, around 3-5% per year, "
                "but the risk of significant losses is minimal."
            )
        elif total_score <= 25:
            st.session_state.risk_level = "Moderately Conservative"
            st.session_state.description = (
                "A **Moderately Conservative** portfolio balances safety with modest growth. "
                "It includes a mix of bonds and dividend-paying stocks to generate steady income "
                "while maintaining some growth potential. This portfolio is suitable for investors who are "
                "cautious but willing to accept limited risk. Expected returns range from 4-6% per year, "
                "with moderate exposure to market volatility."
            )
        elif total_score <= 30:
            st.session_state.risk_level = "Moderate"
            st.session_state.description = (
                "A **Moderate** portfolio seeks a balance between risk and return, aiming for steady growth over time. "
                "This portfolio typically includes a diversified mix of stocks, bonds, and cash, "
                "providing both income and growth opportunities. It is ideal for investors with a medium risk tolerance "
                "who are comfortable with some market fluctuations. Expected returns are around 5-8% per year, "
                "with potential for both moderate gains and losses."
            )
        elif total_score <= 35:
            st.session_state.risk_level = "Moderately Aggressive"
            st.session_state.description = (
                "A **Moderately Aggressive** portfolio focuses on achieving higher returns with increased exposure to risk. "
                "This portfolio has a higher allocation to growth stocks and a smaller percentage in bonds or cash. "
                "It is suitable for investors willing to tolerate significant short-term market volatility in exchange for "
                "potential long-term gains. Expected returns range from 7-10% per year, with a higher risk of losses during "
                "market downturns."
            )
        else:
            st.session_state.risk_level = "Aggressive"
            st.session_state.description = (
                "An **Aggressive** portfolio aims for maximum long-term growth by taking substantial risks. "
                "This portfolio is heavily weighted towards stocks, especially high-growth or speculative stocks, "
                "and may include alternative investments like commodities or cryptocurrencies. It is ideal for investors "
                "with a high-risk tolerance who are comfortable with substantial volatility and potential losses. "
                "Expected returns can be 10% or more per year, but there is a significant risk of loss, especially in bear markets."
            )

        # Enable the portfolio generation button
        st.session_state.show_portfolio = True

# Display the risk level result and description
if st.session_state.risk_level:
    st.subheader(f"Your Risk Tolerance Level: {st.session_state.risk_level}")
    st.write(st.session_state.description)

    # Show recommended asset allocation with a Plotly pie chart
    allocations = {
        "Conservative": [15, 70, 15],
        "Moderately Conservative": [35, 50, 15],
        "Moderate": [55, 35, 10],
        "Moderately Aggressive": [70, 25, 5],
        "Aggressive": [90, 5, 5]
    }

    allocation = allocations[st.session_state.risk_level]
    labels = ['Stocks', 'Bonds', 'Cash']

    # Create a Plotly pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=allocation, hole=0.3)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=15)
    fig.update_layout(title_text='Recommended Asset Allocation', title_x=0.5)

    st.plotly_chart(fig)

# Step 5: User Input for Initial Investment Amount
if st.session_state.show_portfolio:
    st.subheader("Generate Simulated Portfolio")
    st.session_state.initial_investment = st.number_input("Enter Initial Investment Amount ($):", min_value=1000, value=10000, step=100)

    if st.button("Generate Simulated Portfolio"):
        # Define the allocation for simulation with asset descriptions
        allocation = {
            "Conservative": {"SPY": [15, "S&P 500 ETF provides exposure to large-cap U.S. stocks."],
                             "BND": [70, "U.S. Aggregate Bond ETF focuses on investment-grade bonds."],
                             "SHV": [15, "Short Treasury Bond ETF provides stability and liquidity."]},
            "Moderately Conservative": {"SPY": [35, "S&P 500 ETF provides exposure to large-cap U.S. stocks."],
                                        "BND": [50, "U.S. Aggregate Bond ETF focuses on investment-grade bonds."],
                                        "SHV": [15, "Short Treasury Bond ETF provides stability and liquidity."]},
            "Moderate": {"SPY": [35, "S&P 500 ETF provides exposure to large-cap U.S. stocks."],
                         "AAPL": [10, "Apple Inc. is a major tech company with growth potential."],
                         "MSFT": [10, "Microsoft Corp. is a leading technology and cloud computing company."],
                         "BND": [35, "U.S. Aggregate Bond ETF focuses on investment-grade bonds."],
                         "SHV": [10, "Short Treasury Bond ETF provides stability and liquidity."]},
            "Moderately Aggressive": {"AAPL": [25, "Apple Inc. is a major tech company with growth potential."],
                                      "MSFT": [20, "Microsoft Corp. is a leading technology and cloud computing company."],
                                      "TSLA": [15, "Tesla Inc. is a leader in electric vehicles and clean energy."],
                                      "AMZN": [10, "Amazon.com Inc. is a global e-commerce and cloud computing giant."],
                                      "BND": [25, "U.S. Aggregate Bond ETF focuses on investment-grade bonds."],
                                      "SHV": [5, "Short Treasury Bond ETF provides stability and liquidity."]},
            "Aggressive": {"TSLA": [20, "Tesla Inc. is a leader in electric vehicles and clean energy."],
                           "AMZN": [20, "Amazon.com Inc. is a global e-commerce and cloud computing giant."],
                           "NVDA": [15, "NVIDIA Corp. is a leader in graphics processing and AI."],
                           "GOOGL": [15, "Alphabet Inc. is the parent company of Google, known for tech innovation."],
                           "MSFT": [10, "Microsoft Corp. is a leading technology and cloud computing company."],
                           "AAPL": [10, "Apple Inc. is a major tech company with growth potential."],
                           "BND": [5, "U.S. Aggregate Bond ETF focuses on investment-grade bonds."],
                           "SHV": [5, "Short Treasury Bond ETF provides stability and liquidity."]}
        }

        selected_allocation = allocation[st.session_state.risk_level]

        # Display selected allocation details with descriptions
        st.write(f"** Allocation for {st.session_state.risk_level} Portfolio:**")
        for asset, details in selected_allocation.items():
            percentage, description = details
            st.write(f"- {asset}: {percentage}% ({description})")

   
        selected_assets = list(selected_allocation.keys())
        data = yf.download(selected_assets, start=st.session_state.start_date, end=st.session_state.end_date)['Adj Close']

      
        weights = np.array([details[0] for details in selected_allocation.values()]) / 100
        returns = data.pct_change().dropna()
        portfolio_returns = (returns * weights).sum(axis=1)
        cumulative_returns = (1 + portfolio_returns).cumprod() * st.session_state.initial_investment

        # Calculate Key Metrics
        num_years = (st.session_state.end_date - st.session_state.start_date).days / 365.25
        annualized_return = (cumulative_returns[-1] / st.session_state.initial_investment) ** (1/num_years) - 1
        volatility = portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = (annualized_return - 0.02) / portfolio_returns.std()
        portfolio_beta = np.cov(portfolio_returns, returns.mean(axis=1))[0][1] / np.var(returns.mean(axis=1))
        treynor_ratio = (annualized_return - 0.02) / portfolio_beta
        max_drawdown = ((cumulative_returns / cumulative_returns.cummax()) - 1).min() * -1  # Convert to positive percentage

        # Fetch S&P 500 data for comparison
        sp500_data = yf.download('^GSPC', start=st.session_state.start_date, end=st.session_state.end_date)['Adj Close']
        sp500_returns = sp500_data.pct_change().dropna()
        sp500_cumulative_returns = (1 + sp500_returns).cumprod() * st.session_state.initial_investment
        sp500_cagr = (sp500_cumulative_returns[-1] / st.session_state.initial_investment) ** (1/num_years) - 1

        # Display Key Metrics
        st.write(f"**Annualized Return (Portfolio):** {annualized_return:.2%}")
        st.write(f"**Annualized Return (S&P 500):** {sp500_cagr:.2%}")
        st.write(f"**Volatility:** {volatility:.2%}")
        st.write(f"**Sharpe Ratio:** {sharpe_ratio:.2f}")
        st.write(f"**Portfolio Beta:** {portfolio_beta:.2f}")
        st.write(f"**Treynor Ratio:** {treynor_ratio:.2f}")
        st.write(f"**Max Drawdown:** {max_drawdown:.2%}")


        fig = go.Figure(data=go.Scatter(x=cumulative_returns.index, y=cumulative_returns, mode='lines', name='Cumulative Returns'))
        fig.update_layout(title='Simulated Portfolio Performance', xaxis_title='Date', yaxis_title='Value ($)', yaxis_tickformat=',.2f')
        st.plotly_chart(fig)

        # Indicate portfolio has been generated
        st.session_state.portfolio_generated = True
        
        st.write("Created By Gurbaaz Sindhar")
