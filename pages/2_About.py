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
import matplotlib.pyplot as plt
from model import IQR, Q1, Q3, confidence_interval
import numpy as np
import statistics as stat


def about():
    st.write("In Progress")
    st.markdown("### Exploring the Data")
  
    future_returns = pd.read_csv('data/futurereturns.csv')

    statistics = {'Return Rates': ['S&P Future', 'Aggressive Future', 'Moderate Future', 'Conservative Future'],
            'Mean': [np.mean(future_returns['S&P Future']), np.mean(future_returns['Aggressive Future']), np.mean(future_returns['Moderate Future']), np.mean(future_returns['Conservative Future'])],
            'Std Dev': [np.std(future_returns['S&P Future']), np.std(future_returns['Aggressive Future']), np.std(future_returns['Moderate Future']), np.std(future_returns['Conservative Future'])],
            'Variance': [stat.variance(future_returns['S&P Future']), stat.variance(future_returns['Aggressive Future']), stat.variance(future_returns['Moderate Future']), stat.variance(future_returns['Conservative Future'])],
            'IQR': [IQR(future_returns['S&P Future']), IQR(future_returns['Aggressive Future']), IQR(future_returns['Moderate Future']), IQR(future_returns['Conservative Future'])],
            'Q1': [Q1(future_returns['S&P Future']), Q1(future_returns['Aggressive Future']), Q1(future_returns['Moderate Future']), Q1(future_returns['Conservative Future'])],
            'Q3': [Q3(future_returns['S&P Future']), Q3(future_returns['Aggressive Future']), Q3(future_returns['Moderate Future']), Q3(future_returns['Conservative Future'])]}   
                                                                                                      
    statistics_table = pd.DataFrame.from_dict(statistics).set_index('Return Rates')           
    #multiply all the values in the table by 100 to get percentage values
    statistics_table = (statistics_table*100).round(2)
    statistics_table['95% Conf'] = [confidence_interval(future_returns['S&P Future']), confidence_interval(future_returns['Aggressive Future']), confidence_interval(future_returns['Moderate Future']), confidence_interval(future_returns['Conservative Future'])]
    st.dataframe(statistics_table)

    plt.hist(future_returns['S&P Future'], bins=50, alpha=0.7, color='#e9e9ee')
    plt.hist(future_returns['Aggressive Future'], bins=50, alpha=0.7, color='#c7c2d6')
    plt.hist(future_returns['Moderate Future'], bins=50, alpha=0.7, color='#787380')
    plt.hist(future_returns['Conservative Future'], bins=50, alpha=0.7, color='#494351')
    plt.legend(['S&P Future', 'Aggressive Future', 'Moderate Future', 'Conservative Future'])

    st.pyplot(plt)


st.set_page_config(page_title="About the Retirement Simulator", page_icon="🐍")
st.markdown("# About the Retirement Simulator")

with st.sidebar:
    st.write("Add text and links")


about()

st.divider()

st.write(
    """Created by [Denver Data Design](https://denverdatadesign.com/).""")


