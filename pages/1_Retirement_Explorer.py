import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from function import lifecycle_chart
from page_elements import footer, side_content

future_returns = pd.read_csv('data/futurereturns.csv')
investor_returns = {
    'Aggressive': {'aggressive_investor': list(future_returns['Aggressive Future'])},
    'Moderate':   {'moderate_investor':   list(future_returns['Moderate Future'])},
    'Conservative': {'conservative_investor': list(future_returns['Conservative Future'])},
}

st.set_page_config(page_title="Retirement Explorer", page_icon="🎯", layout="wide")
st.markdown("# Retirement Explorer 🎯")
st.markdown("*Explore how different choices affect your retirement future.*")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("**What is your initial investment?**")
    investment_str = st.text_input("Initial investment", label_visibility="collapsed", placeholder="e.g. 50,000")
    initial_investment = 0
    if investment_str:
        try:
            initial_investment = int(float(investment_str.replace(',', '').replace('$', '').strip()))
        except ValueError:
            st.error("Please enter a valid number")

    st.markdown("**What will your annual contribution be?**")
    contribution_str = st.text_input("Annual contribution", label_visibility="collapsed", placeholder="e.g. 5,000 (optional)")
    annual_contribution = 0
    if contribution_str:
        try:
            annual_contribution = int(float(contribution_str.replace(',', '').replace('$', '').strip()))
        except ValueError:
            st.error("Please enter a valid number")

with col2:
    st.markdown("**Monthly income goal?**")
    expenses_str = st.text_input("Monthly income goal", label_visibility="collapsed", placeholder="e.g. 5,000")
    monthly_expenses = 0
    if expenses_str:
        try:
            monthly_expenses = int(float(expenses_str.replace(',', '').replace('$', '').strip()))
        except ValueError:
            st.error("Please enter a valid number")

    st.markdown("**Other retirement income?**")
    other_income_str = st.text_input("Other retirement income", label_visibility="collapsed", placeholder="e.g. Social Security")
    other_income = 0
    if other_income_str:
        try:
            other_income = int(float(other_income_str.replace(',', '').replace('$', '').strip()))
        except ValueError:
            st.error("Please enter a valid number")

with col3:
    st.markdown("**How many years until you retire?**")
    years = st.slider("Years until retirement", 0, 50, 20, label_visibility="collapsed")
    st.markdown("**What is your current annual income?**")
    income_str = st.text_input("Current annual income", label_visibility="collapsed", placeholder="e.g. 120,000 (optional)")
    current_income = None
    if income_str:
        try:
            current_income = int(float(income_str.replace(',', '').replace('$', '').strip()))
        except ValueError:
            st.error("Please enter a valid number")

investor = 'Moderate'

# Deterministic projection using geometric mean — consistent across slider moves
rates = list(investor_returns[investor].values())[0]
mean_return = float(np.exp(np.mean(np.log([1 + r for r in rates]))) - 1)
portfolio = float(initial_investment)
for _ in range(years):
    portfolio = portfolio * (1 + mean_return) + annual_contribution
projected_value = portfolio

portfolio_income = monthly_expenses - (other_income / 12)  # other_income is annual, convert to monthly
implied_rate = (portfolio_income * 12) / projected_value if projected_value > 0 and portfolio_income > 0 else 0
chart_rate = implied_rate if implied_rate > 0 else 0.04
implied_rate_pct = implied_rate * 100

st.divider()

if monthly_expenses > 0:
    display_income = monthly_expenses
    rate_label = f"{implied_rate_pct:.1f}%"
else:
    display_income = projected_value * 0.04 / 12
    rate_label = "4%"

# Check if portfolio depletes within 30 post-retirement years
depletion_year = None
retirement_year = datetime.now().year + years
sim_portfolio = projected_value
annual_withdrawal = projected_value * chart_rate
for i in range(30):
    sim_portfolio = sim_portfolio * (1 + mean_return) - annual_withdrawal * (1.025 ** i)
    if sim_portfolio <= 0:
        depletion_year = retirement_year + i + 1
        break

depletion_text = f' At this rate, <b>your portfolio will run out of money in {depletion_year}</b>.' if depletion_year else ''

st.markdown(
    f'<div style="background-color:#e2e8f7;border:1px solid #c7c2d6;border-radius:4px;padding:12px;margin-bottom:12px">'
    f'In <b>{years}</b> years, your portfolio is projected to be worth <b>&#36;{projected_value:,.0f}</b> '
    f'and will provide a monthly income of <b>&#36;{display_income:,.0f}</b> at a <b>{rate_label}</b> withdrawal rate.'
    f'{depletion_text}'
    f'</div>', unsafe_allow_html=True)

fig_lifecycle = lifecycle_chart(
    investor_returns[investor], initial_investment, years, annual_contribution,
    projected_value, chart_rate, current_income, other_income
)
st.plotly_chart(fig_lifecycle, use_container_width=True, theme="streamlit", config={"displayModeBar": False})
st.markdown("*Income and withdrawal amounts are adjusted for 2.5% annual inflation.*")

footer()

with st.sidebar:
    side_content()
