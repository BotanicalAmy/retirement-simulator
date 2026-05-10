import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from function import retirement_forecast_v2 as retirement_forecast, lifecycle_chart
from page_elements import footer, side_content, V_SPACE, retirement_inputs
from datetime import datetime

future_returns = pd.read_csv('data/futurereturns.csv')
aggressive = {'aggressive_investor': list(future_returns['Aggressive Future'])}
moderate = {'moderate_investor': list(future_returns['Moderate Future'])}
conservative = {'conservative_investor': list(future_returns['Conservative Future'])}
investor_returns = {
    'Aggressive': aggressive,
    'Moderate': moderate,
    'Conservative': conservative,
}

st.set_page_config(page_title="Retirement Planner", page_icon="📋")
st.markdown("# Retirement Planner 📋")


def retirement_planner():
    if 'plan_results' not in st.session_state:
        st.session_state.plan_results = None

    st.markdown("### My Savings")
    investment, contribution, investor, years, percent, withdrawl_rate = retirement_inputs()

    st.divider()
    st.markdown("### My Retirement Goals")
    col3, col4 = st.columns(2, gap="medium")

    with col3:
        st.markdown("**What are your expected monthly expenses in retirement?**")
        expenses_str = st.text_input(label="Monthly expenses", label_visibility="collapsed", placeholder="e.g. 3,000")
        monthly_expenses = None
        if expenses_str:
            try:
                monthly_expenses = int(float(expenses_str.replace(',', '').replace('$', '').strip()))
            except ValueError:
                st.error("Please enter a valid number")

        st.markdown("**What is your current income?** *(optional)*")
        current_income_str = st.text_input(label="Current income", label_visibility="collapsed", placeholder="e.g. 120,000")
        current_income = None
        if current_income_str:
            try:
                current_income = int(float(current_income_str.replace(',', '').replace('$', '').strip()))
            except ValueError:
                st.error("Please enter a valid number")

    with col4:
        st.markdown("**Any other monthly income in retirement?** *(e.g. Social Security, pension)*")
        other_income_str = st.text_input(label="Other monthly income", label_visibility="collapsed", placeholder="e.g. 1,500")
        other_income = 0
        if other_income_str:
            try:
                other_income = int(float(other_income_str.replace(',', '').replace('$', '').strip()))
            except ValueError:
                st.error("Please enter a valid number")
                other_income = 0
        run_plan = st.button("Check my Retirement")

    if run_plan and investment is not None and monthly_expenses is not None:
        values = retirement_forecast(investor_returns[investor], investment, years, contribution)
        projected_value = values.iloc[-1, :5].mean()
        total_monthly = (projected_value * withdrawl_rate) / 12 + other_income
        gap = total_monthly - monthly_expenses
        funded_pct = min((total_monthly / monthly_expenses) * 100, 150)
        st.session_state.plan_results = {
            'projected_value': projected_value,
            'total_monthly': total_monthly,
            'gap': gap,
            'monthly_expenses': monthly_expenses,
            'retirement_year': years + datetime.now().year,
            'funded_pct': funded_pct,
            'years': years,
            'percent': percent,
            'investor': investor,
            'investment': investment,
            'contribution': contribution,
            'withdrawl_rate': withdrawl_rate,
            'current_income': current_income,
            'other_income': other_income,
        }

    if st.session_state.plan_results:
        r = st.session_state.plan_results
        gap = r['gap']
        funded_pct = r['funded_pct']

        st.divider()
        st.markdown("### Results")

        st.markdown("""
            <style>
            [data-testid="stMetricValue"] { font-size: 1.2rem; }
            [data-testid="stMetricLabel"] { font-size: 0.85rem; }
            [data-testid="column"] { padding-bottom: 0 !important; }
            </style>""", unsafe_allow_html=True)

        col_metrics, col_gauge = st.columns([1, 1])

        with col_metrics:
            st.metric("Projected Portfolio Value", f"${r['projected_value']:,.0f}")
            st.metric("Projected Monthly Income", f"${r['total_monthly']:,.0f}")
            arrow = "↑" if gap >= 0 else "↓"
            arrow_color = "#21c354" if gap >= 0 else "#ff4b4b"
            gap_display = f"${gap:,.0f}" if gap >= 0 else f"${abs(gap):,.0f}"
            st.markdown(f"""
                <div style="margin-bottom:1rem;">
                    <p style="font-size:0.85rem;color:#808495;margin-bottom:0.25rem;font-family:Source Sans Pro,sans-serif;">Monthly Surplus / Gap</p>
                    <p style="font-size:1.2rem;color:#31333F;margin:0;font-family:Source Sans Pro,sans-serif;">
                        <span style="color:{arrow_color};">{arrow}</span> {gap_display}
                    </p>
                </div>""", unsafe_allow_html=True)

        with col_gauge:
            gauge_color = "#2ecc71" if funded_pct >= 100 else ("#f0a500" if funded_pct >= 75 else "#e74c3c")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=funded_pct,
                number={"suffix": "%", "font": {"size": 20, "color": "#31333F"}},
                gauge={
                    "axis": {"range": [0, 150], "tickvals": [0, 50, 75, 100, 150], "ticktext": ["0%", "50%", "75%", "100%", "150%"], "tickfont": {"size": 13, "color": "#31333F"}},
                    "bar": {"color": gauge_color},
                    "steps": [
                        {"range": [0, 50], "color": "#fde8e8"},
                        {"range": [50, 75], "color": "#fef6e0"},
                        {"range": [75, 100], "color": "#fef6e0"},
                        {"range": [100, 150], "color": "#e8f8ee"},
                    ],
                    "threshold": {"line": {"color": "black", "width": 2}, "thickness": 0.75, "value": 100},
                },
                title={"text": "<b>Goal Funded</b>", "font": {"size": 20, "color": "#31333F", "family": "Source Sans Pro, sans-serif"}},
            ))
            fig.update_layout(
                height=220,
                margin=dict(t=30, b=0, l=50, r=50),
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


        fig_lifecycle = lifecycle_chart(
            investor_returns[r['investor']], r['investment'], r['years'], r['contribution'],
            r['projected_value'], r['withdrawl_rate'], r['current_income'], r['other_income']
        )
        st.plotly_chart(fig_lifecycle, use_container_width=True, theme="streamlit", config={"displayModeBar": False})
        st.markdown("*Income and withdrawal amounts are adjusted for 2.5% annual inflation.*")

    footer()


retirement_planner()

with st.sidebar:
    side_content()
