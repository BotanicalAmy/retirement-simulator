import streamlit as st
import pandas as pd
from function import retirement_forecast, retirement_plot, retirement_values
from page_elements import footer, side_content, retirement_inputs
from datetime import datetime

st.set_page_config(page_title="Future Forecast", page_icon="🎲", layout="wide")

future_returns = pd.read_csv('data/futurereturns.csv')
aggressive = {'aggressive_investor': list(future_returns['Aggressive Future'])}
moderate = {'moderate_investor': list(future_returns['Moderate Future'])}
conservative = {'conservative_investor': list(future_returns['Conservative Future'])}

investor_descriptions = {
    'Aggressive': '*Aggressive investors have a high risk tolerance and are willing to risk more money for the possibility of better, yet unknown, returns.*',
    'Moderate': '*Moderate investors want to grow their money without losing too much. Their goal is to weigh opportunities and risks and this investor\'s approach is sometimes described as a balanced strategy.*',
    'Conservative': '*Conservative investors are willing to accept little to no volatility in their investment portfolios. Retirees or those close to retirement are usually in this category.*',
}

investor_returns = {
    'Aggressive': aggressive,
    'Moderate': moderate,
    'Conservative': conservative,
}

if 'summary_rows' not in st.session_state:
    st.session_state.summary_rows = []
if 'sim_results' not in st.session_state:
    st.session_state.sim_results = None

st.write("# Forecast your financial future 🎲")
st.markdown("The variability of the stock market leads to a range of future outcomes. Each forecast draws from historical returns to generate five probable scenarios.")

investment, contribution, investor, years, percent, withdrawl_rate, forecast_clicked = retirement_inputs()

if forecast_clicked and investment is not None:
    values = retirement_forecast(investor_returns[investor], investment, years, contribution)
    projected_value = values.iloc[-1, :5].mean()
    monthly_income = (projected_value * withdrawl_rate) / 12
    retirement_year = years + datetime.now().year

    return_df = retirement_values(values, withdrawl_rate)
    row = return_df.reset_index().iloc[0].to_dict()
    row['Investor'] = investor
    row['Initial Inv.'] = '${:,}'.format(investment)
    row['Contribution'] = '${:,}/yr'.format(contribution)
    st.session_state.summary_rows.append(row)

    st.session_state.sim_results = {
        'values': values,
        'investment': investment,
        'contribution': contribution,
        'projected_value': projected_value,
        'monthly_income': monthly_income,
        'years': years,
        'percent': percent,
        'retirement_year': retirement_year,
        'investor': investor,
    }

if st.session_state.sim_results:
    r = st.session_state.sim_results
    st.markdown(investor_descriptions[r['investor']])
    st.markdown(
        f'<div style="background-color:#e2e8f7;border:1px solid #c7c2d6;border-radius:4px;padding:12px;margin-bottom:12px">'
        f'In <b>{r["years"]}</b> years, your portfolio is projected to be worth <b>&#36;{r["projected_value"]:,.0f}</b> and will provide a monthly income of <b>&#36;{r["monthly_income"]:,.0f}</b> at a <b>{r["percent"]}</b> withdrawal rate.'
        f'</div>', unsafe_allow_html=True)

    plot = retirement_plot(r['values'], r['investment'], r['contribution'])
    st.plotly_chart(plot, use_container_width=True, theme="streamlit")
    st.markdown('The return rate uses the [Geometric Mean](https://analystprep.com/cfa-level-1-exam/quantitative-methods/arithmetic-return-vs-geometric-return/).')

if st.session_state.summary_rows:
    st.markdown("### Retirement Plan Comparison")
    summary_df = pd.DataFrame(st.session_state.summary_rows)
    summary_df = summary_df.rename(columns={'Withdrawl Rate': 'Withdrawl', 'Monthly Income': 'Income/mo', 'Annual Income': 'Income/yr'})
    cols = ['Investor', 'Initial Inv.', 'Contribution', 'Return Rate', 'Withdrawl', 'Income/yr', 'Income/mo']
    summary_df = summary_df[['Final Year'] + cols].set_index('Final Year')
    summary_df.index.name = 'Retirement'
    st.dataframe(summary_df)

footer()

with st.sidebar:
    st.markdown("*A retirement plan comparison table will build as varying options are selected.*")
    if st.button("Reset the Data"):
        st.session_state.summary_rows = []
        st.session_state.sim_results = None
        st.rerun()
    side_content()
