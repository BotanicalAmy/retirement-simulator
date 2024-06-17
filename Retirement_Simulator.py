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

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
from function import retirement_forecast, retirement_plot, retirement_values
from page_elements import footer, side_content, V_SPACE
from datetime import datetime

LOGGER = get_logger(__name__)

#getting the future returns dataframe
future_returns = pd.read_csv('data/futurereturns.csv')
#pulling the returns from the futures dataframe, preparation for the forecasting function
aggressive = {'aggressive_investor':list(future_returns['Aggressive Future'])}
moderate = {'moderate_investor': list(future_returns['Moderate Future'])}
conservative = {'conservative_investor':list(future_returns['Conservative Future'])}
nervous = {'nervous_investor':list(future_returns['Aggressive Future'])}

def main():
    st.write("# Forecast your financial future 🎲")
    V_SPACE(1)
    st.markdown('''The provided simulator uses historical returns to create a series of probable investment outcomes. Each selection of "Forecast your Future" will 
                create a series of five, hypothetical investment scenarios. *Final values will vary based on each randomized draw from the return distributions*.''')

    with st.form("Select your retirement options"):
      col1, col2 = st.columns(2, gap="medium")

      with col1:
        #select starting investment value
        st.markdown('**What is your initial investment?**')
        investment = st.number_input(label="Enter your initial investment", label_visibility="collapsed", value=None, placeholder='Type a number...', min_value=10000)
        #streamlit limitations do not allow the addition of commas to the number input
        st.write('The initial investment is $',investment)

        #select investor type
        st.markdown('**What type of investor are you?**')
        investor = st.selectbox('What type of investor are you?',
        ('Moderate', 'Aggressive','Conservative', 'Nervous'), label_visibility="collapsed")

      with col2:
        #select the number of years to forecast
        st.markdown('**How long will you invest?**')
        years = st.slider('How many years will you invest?', 10, 50, 20, label_visibility="collapsed")
        st.write("I plan to invest for ", years, 'years')
      
      submitted = st.form_submit_button("Forecast your Future")
      if submitted and investment is not None:
        st.write('You selected:', investor)
        if investor == 'Aggressive':
          st.markdown('*Aggressive investors have a high risk tolerance and are willing to risk more money for the possibility of better, yet unknown, returns.*')
          values = retirement_forecast(aggressive, investment, years)
          plot = retirement_plot(values, investment)

        if investor == 'Moderate':
          st.markdown("*Moderate investors want to grow their money without losing too much. Their goal is to weigh opportunities and risks and this investor's approach is sometimes described as a “balanced” strategy.*")
          values = retirement_forecast(moderate, investment, years)
          plot = retirement_plot(values, investment)

        if investor == 'Conservative':
          st.markdown('*Conservative investors are willing to accept little to no volatility in their investment portfolios. Retirees or those close to retirement are usually in this category.*')
          values = retirement_forecast(conservative, investment, years)
          plot = retirement_plot(values, investment)

        if investor == 'Nervous':
          st.markdown('*Nervous investors have financial anxiety and often react to the market. When the market drops, the nervous investor pulls their money out of the stock market, waiting to reinvest when returns remain positive.*')
          values = retirement_forecast(nervous, investment, years)
          plot = retirement_plot(values, investment)

        st.plotly_chart(plot, use_container_width=True, theme="streamlit")
        return_df = retirement_values(values)
        st.dataframe(return_df)

        retirement_year = years + datetime.now().year
        st.markdown(f'*The retirement income is based on a 4% annual withdrawl rate, beginning in {retirement_year}.*')
        st.markdown('''The return rate uses the [Geometric Mean](https://analystprep.com/cfa-level-1-exam/quantitative-methods/arithmetic-return-vs-geometric-return/).''')

    footer()

#add page title and sidebar 
st.set_page_config(
page_title="Retirement Simulator",
page_icon="💵",
)
with st.sidebar:
  side_content()

if __name__ == "__main__":
    main()
