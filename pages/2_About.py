# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import streamlit as st
from model import IQR, Q1, Q3, confidence_interval
import numpy as np
import statistics as stat
from page_elements import footer, side_content, V_SPACE


def about():

    st.markdown("### How Forecasting Works")
    st.markdown("""
Each forecast runs *5 independent scenarios* by sampling from a dataset of historical and projected return rates.
The scenarios are averaged to produce a single projected outcome, giving a more stable estimate than any single run alone.

**Investor types** reflect different risk tolerances:""")

    future_returns_preview = pd.read_csv('data/futurereturns.csv')
    investor_types = pd.DataFrame({
        'Investor Type': ['Aggressive', 'Moderate', 'Conservative'],
        'Description': [
            'Comfortable with volatility, with the benefit of potentially higher returns.',
            'Prefer a balanced approach, seeking growth while managing risk.',
            'Prioritize capital preservation, accepting lower returns for reduced risk.',
        ],
        'Avg Return Rate': [
            f"{(np.exp(np.mean(np.log(1 + future_returns_preview['Aggressive Future']))) - 1) * 100:.1f}%",
            f"{(np.exp(np.mean(np.log(1 + future_returns_preview['Moderate Future']))) - 1) * 100:.1f}%",
            f"{(np.exp(np.mean(np.log(1 + future_returns_preview['Conservative Future']))) - 1) * 100:.1f}%",
        ],
    })
    st.dataframe(investor_types, hide_index=True, use_container_width=True)

    st.markdown("""
**Sampling methods**:

- **10+ years**: Utilizes a *constrained* sampling method that mirrors the patterns found in historical market data.
Each scenario is checked to ensure a realistic proportion of year-over-year gains and losses. This produces scenarios 
that align more closely with historical long-term market cycles (image below).

- **< 10 years**: Utilizes a *random* sampling method from the return rate distribution. Enforcing long-term pattern constraints would
distort results with the narrow time frame. Random draws better reflect the higher uncertainty of near-term forecasts.
""")
    st.divider()
    st.markdown("""                
#### Constrained sampling for 10+ year forecasts:
""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Positive Change Constraint** *(all investor types)*")
        st.markdown("""
- Between 40–50% of consecutive year-pairs must show a year-over-year increase
- Mimics historical stock market patterns
""")

    with col2:
        st.markdown("**Negative Returns Constraint** *(aggressive only)*")
        st.markdown("""
- At least 10% of sampled years must have negative returns
- Skipped for conservative and moderate
""")

    st.markdown("""
The sampler loops until 5 valid scenarios are found. There is no cap on negative years, only a minimum of 10% negative values for aggressive
investors. A sample could theoretically contain many more down years as long as the *positive-change* constraint is also satisfied.

*In both cases, results are projections based on historical patterns and are not guarantees of future performance.*
""")

    hist_returns = pd.read_csv('data/historical_returns.csv')
    # Include 1929 so 1930 has a valid year-over-year comparison
    sp_full = hist_returns[hist_returns['Year'] <= 2019][['Year', 'S&P 500']].copy()
    sp_full = sp_full.sort_values('Year')
    sp_full['prev_return'] = sp_full['S&P 500'].shift(1)
    sp_full['is_up'] = sp_full['S&P 500'] > sp_full['prev_return']
    sp = sp_full[sp_full['Year'] >= 1930].copy()
    sp['Decade'] = (sp['Year'] // 10 * 10).astype(str) + "'s"
    sp['Year_in_Decade'] = sp['Year'] % 10

    decade_order = ["1930's", "1940's", "1950's", "1960's", "1970's", "1980's", "1990's", "2000's", "2010's"]
    pivot_vals = sp.pivot(index='Decade', columns='Year_in_Decade', values='S&P 500')
    pivot_vals = (pivot_vals * 100).round(1)
    pivot_vals = pivot_vals.loc[decade_order]
    pivot_vals.columns.name = None
    pivot_vals.index.name = None

    pivot_color = sp.pivot(index='Decade', columns='Year_in_Decade', values='is_up')
    pivot_color = pivot_color.loc[decade_order]
    pivot_color.columns.name = None
    pivot_color.index.name = None

    green_bg, green_fg = '#c6efce', '#276221'
    red_bg, red_fg = '#ffc7ce', '#9c0006'
    header_style = 'background:#f0f0f0; padding:6px 12px; text-align:center;'
    index_style = 'background:#f0f0f0; padding:6px 12px; white-space:nowrap;'

    header_html = f'<th style="{header_style}"></th>'
    for c in pivot_vals.columns:
        header_html += f'<th style="{header_style}">{c}</th>'

    rows_html = ''
    for decade in decade_order:
        row_html = f'<td style="{index_style}">{decade}</td>'
        for c in pivot_vals.columns:
            val = pivot_vals.loc[decade, c]
            if pd.isna(val):
                row_html += '<td style="padding:6px 12px;"></td>'
            else:
                bg = green_bg if pivot_color.loc[decade, c] else red_bg
                fg = green_fg if pivot_color.loc[decade, c] else red_fg
                row_html += f'<td style="background:{bg}; color:{fg}; padding:6px 12px; text-align:center;">{val:.1f}%</td>'
        rows_html += f'<tr style="border-top:3px solid white;">{row_html}</tr>'

    table_html = f'''
    <table style="border-collapse:separate; border-spacing:0 3px; width:100%; font-size:14px;">
        <thead><tr>{header_html}</tr></thead>
        <tbody>{rows_html}</tbody>
    </table>'''

    st.markdown("**Historical S&P 500 Returns**")
    st.markdown(
        '<span style="display:inline-block; background-color:#c6efce; width:16px; height:16px; border-radius:3px; vertical-align:middle; margin-right:6px;"></span>'
        'Return rate higher than previous year &nbsp;&nbsp;&nbsp;'
        '<span style="display:inline-block; background-color:#ffc7ce; width:16px; height:16px; border-radius:3px; vertical-align:middle; margin-right:6px;"></span>'
        'Return rate lower than previous year',
        unsafe_allow_html=True
    )
    st.markdown(table_html, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Exploring the Data")
    st.markdown('''A python function was created to sample data from historical stock market returns. A repeated sampling method was used to create
                a set of return rate distributions for the forecasting functions. Below, the statistics of each dataset are
                included to show the value ranges of each category of return rates.''')
    V_SPACE(1)

    future_returns = pd.read_csv('data/futurereturns.csv')

    statistics = {'Return Rates': ['S&P Future', 'Aggressive Future', 'Moderate Future', 'Conservative Future'],
            'Mean': [np.mean(future_returns['S&P Future']), np.mean(future_returns['Aggressive Future']), np.mean(future_returns['Moderate Future']), np.mean(future_returns['Conservative Future'])],
            'Std Dev': [np.std(future_returns['S&P Future']), np.std(future_returns['Aggressive Future']), np.std(future_returns['Moderate Future']), np.std(future_returns['Conservative Future'])],
            'Variance': [stat.variance(future_returns['S&P Future']), stat.variance(future_returns['Aggressive Future']), stat.variance(future_returns['Moderate Future']), stat.variance(future_returns['Conservative Future'])],
            'IQR': [IQR(future_returns['S&P Future']), IQR(future_returns['Aggressive Future']), IQR(future_returns['Moderate Future']), IQR(future_returns['Conservative Future'])],
            'Q1': [Q1(future_returns['S&P Future']), Q1(future_returns['Aggressive Future']), Q1(future_returns['Moderate Future']), Q1(future_returns['Conservative Future'])],
            'Q3': [Q3(future_returns['S&P Future']), Q3(future_returns['Aggressive Future']), Q3(future_returns['Moderate Future']), Q3(future_returns['Conservative Future'])]}

    statistics_table = pd.DataFrame.from_dict(statistics).set_index('Return Rates')
    statistics_table = (statistics_table*100).round(2)
    statistics_table['95% Conf'] = [confidence_interval(future_returns['S&P Future']), confidence_interval(future_returns['Aggressive Future']), confidence_interval(future_returns['Moderate Future']), confidence_interval(future_returns['Conservative Future'])]
    st.dataframe(statistics_table, use_container_width=True)

    st.markdown("### The Mathematical Model")
    st.markdown('''After developing a large distribution of return rates, a Python function was written to model the patterns of historical
                stock market returns. A set of 10,000 hypothetical returns was generated from this function to create a dataset for the
                predictive models. For the original simulator version, a machine learning process using KNN model had the best performance and
                was therefore utilized in the initial data application.''')
    st.markdown('''To learn more about the mathematical modeling behind this data app, check out the [Jupyter
                Notebook](https://github.com/BotanicalAmy/Retirement-Forecaster) used for the development process.''')

    st.divider()
    st.markdown("### Release Notes")
    st.markdown("""

**Version 1.1**
Removed the previous KNN model option, relying entirely on constrained statistical sampling and a supplemental random component for short term investors.
Added the Retirement Explorer, updated branding, and improved the user interface.
                                
**Version 1.0**
Original release, built as a final project for the AI and Machine Learning course at UC Berkeley.
The predictive model used a K-Nearest Neighbors (KNN) algorithm trained on a dataset of 10,000 hypothetical returns.
""")

    footer()


#page title and sidebar content
st.set_page_config(page_title="About", page_icon="🐍", layout="wide")
st.markdown("# About this App 🐍")

with st.sidebar:
    side_content()


about()
