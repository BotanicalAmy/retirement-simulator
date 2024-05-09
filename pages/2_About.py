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
from page_elements import footer, side_content


def about():
    st.markdown('''This retirement simulator is designed to assist investors in visualizing their retirement planning options.
                Users are given a variety of options to forecast their future, the purpose of each option is detailed below.
                ''')

    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Retirement Simulator**")
        st.write("Visualize the variation within investment scenarios, based on probability")


    with col2:
        st.markdown("**AI Forecast**")
        st.write("Forecast the most probable retirement scenario, based on machine learning")

    with col3:
        st.markdown("**Income Planner**")
        st.markdown("Develop a retirement income plan, based on an interactive data table")
    st.divider()
    
    st.markdown("### Exploring the Data")
    st.markdown('''A python function was created to sample data from actual stock market returns. This repeated sampling effort was used to create
                a set of return rate distributions for the forecasting functions. Below, the statistics of each dataset are
                included to show the value ranges of each category of return rates.''')
    st.markdown("##")

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


    st.markdown("**Distribution of returns from the sampled data**")
    st.markdown('''The histogram below visualizes the statistics detailed above. Note that the wider the ranges of values in the 95\% 
                confidence range are reflected in a wider the probability curve.''')
    st.image('images/futures_histogram.jpg')

    st.markdown("### Creating the AI Model")
    st.markdown('''After the initial distribution of return rates were created, a python function was written to model the patterns of historical
                stock market returns. This function was then programmed to create a sample of 10,000 hypothetical returns. This dataset was
                used to train a series of predictive models. The KNN model had the best performance and was therefore utilized in the final
                data application.''')
    st.markdown('''To learn more about the mathematical modeling behind this data app, check out the [Jupyter
                Notebook](https://github.com/BotanicalAmy/Retirement-Forecaster) used for my research and modeling. ''')

    st.markdown("#### Performance trends with the AI model dataset")
    st.markdown('''This retirement simulator was inspired by a business use case for a local wealth management firm. As advisors, 
                one of their challenges is to visualize the impact of retirement decisions for their clients. In particular, when the
                stock market yields negative returns, many nervous investors want to reactively pull out of the market. The nervous
                investor type was programmed into the model to better display the negative impacts of this reactive decision making. ''')
    st.markdown('''Below is a visualization of the performance of the 10,000 sample retirement dataset. Despite being invested similar
                to the aggressive investors, the nervous investors ended up with the worst portfolio performance trends.''')
    st.image('images/future_returns_trends.jpg')



st.set_page_config(page_title="About the Retirement Simulator", page_icon="🐍")
st.markdown("# About the Retirement Simulator")

with st.sidebar:
    side_content()


about()

footer()


