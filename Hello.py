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
from datetime import datetime
import random
import pandas as pd
import numpy as np

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Retirement Simulator",
        page_icon="🎲",
    )

    st.write("# 🎲 Predict your financial future ")
    st.write("Welcome to my retirement forecaster")

    #selecting investment types
    st.markdown('#### How long will you invest? ####')
    years = st.slider('How many years will you invest?', 10, 50, 20, label_visibility="hidden")
    st.write("I plan to invest for ", years, 'years')
    st.markdown('#### What is your initial investment? ####')
    investment = st.number_input(label="Enter your initial investment", label_visibility="hidden", value=None, placeholder='Type a number...', min_value=10000)
    st.write('The initial investment is $',investment)

    investor = st.selectbox(
      'What type of investor are you?',
      ('Moderate', 'Aggressive', 'Conservative', 'Nervous'))

    st.write('You selected:', investor)
    if investor == 'Aggressive':
     st.markdown('*Aggressive investors have a high risk tolerance and are willing to risk more money for the possibility of better, yet unknown, returns.*')
    if investor == 'Moderate':
      st.markdown("*Moderate investors want to grow their money without losing too much. Their goal is to weigh opportunities and risks and this investor's approach is sometimes described as a “balanced” strategy.*")
    if investor == 'Conservative':
      st.markdown('*Conservative investors are willing to accept little to no volatility in their investment portfolios. Retirees or those close to retirement are usually in this category.*')
    if investor == 'Nervous':
      st.markdown('*Nervous investors have financial anxiety and often react to the market. When the market drops, the nervous investor pulls their money out of the stock market, waiting to reinvest when returns remain positive.*')


    future_returns = pd.read_csv('data/futurereturns.csv')
    #pulling the returns from the futures dataframe, preparation for the forecasting function
    aggressive = {'aggressive_investor':list(future_returns['Aggressive Future'])}
    moderate = {'moderate_investor': list(future_returns['Moderate Future'])}
    conservative = {'conservative_investor':list(future_returns['Conservative Future'])}
    nervous = {'nervous_investor':list(future_returns['Aggressive Future'])}
    # st.dataframe(my_dataframe)
    # forecast_values = retirement_forecast(investor,investment,years)
    # st.dataframe(forecast_values)

    st.sidebar.success("Select a demo above.")


    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
