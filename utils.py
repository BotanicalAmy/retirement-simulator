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

import inspect
import textwrap
from datetime import datetime
import random
import pandas as pd
import numpy as np

import streamlit as st


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

#based on the rate distribution patterns, the negative counter function is only used for the aggressive return rates
#function to calculate the percentage of negative return rates
def negative_counter(list):
    neg_counter = 0
    for r in range(len(list)):
        if list[r] < 0:
            neg_counter += 1
    percent_negative = (neg_counter/len(list))*100
    return percent_negative

#function to calculate the percentage of positive change in the return rates
def positive_change_counter(list):
    pos_change_counter = 0
    for i in range(len(list)-1):
        if list[i] < list[i+1]:
            pos_change_counter += 1
    percent_pos_change = (pos_change_counter/len(list))*100
    return percent_pos_change


#enter the investor type (aggressive, moderate, conservative or nervous), the initial investment, and the number of years to forecast
def retirement_forecast(investor, investment, years):
    forecast_rates = list(investor.values())[0]
    investor_type = list(investor.keys())[0]
    sample_count = 0
    forecast_samples = {}
    forecast_df = [0,0]

    #require the user to enter a minimum of 10 years
    if years < 10:
        return('Please enter a forecast period of at least 10 years')
    else:
        pass
    #creating a sample that follows the same patterns of positive and negative change, as well as negative returns 
    while sample_count < 5:
        rates = random.sample(forecast_rates, years)
        negative = negative_counter(rates)
        positive_change = positive_change_counter(rates)
        if positive_change >= 40 and positive_change <= 50:
            if investor_type == 'aggressive_investor':
                if negative < 10:
                    pass
                else:
                    agg_rates = rates.copy() 
                    column_name = 'Sample ' + str(sample_count+1)
                    forecast_samples[column_name] = agg_rates
                    sample_count += 1
            #creating nervous investor, zero rates signify pulling out of the market
            if investor_type == 'nervous_investor':
                #this statement is pushing the zeroed values into my aggressive return dataframe
                if negative < 10:
                    pass
                else:
                    #if investor is nervous, replace the three consecutive returns after a negative rate with a zero
                    nervous_rates = rates.copy()
                    for i in range(len(nervous_rates)-3):
                        if nervous_rates[i] < 0:
                            nervous_rates[i+1] = 0
                            nervous_rates[i+2] = 0
                            nervous_rates[i+3] = 0
                    zero_rates = nervous_rates
                    column_name = 'Sample ' + str(sample_count+1)
                    forecast_samples[column_name] = zero_rates
                    sample_count += 1
            #conservative or moderate investor
            if investor_type == 'conservative_investor' or investor_type == 'moderate_investor':
                con_mod_rates = rates.copy()
                column_name = 'Sample ' + str(sample_count+1)
                forecast_samples[column_name] = con_mod_rates
                sample_count += 1
            else:
                pass
        else:
            pass
    #create dataframe from the dictionary
    forecast_df = pd.DataFrame(forecast_samples)
    #create  year column, starting with the current year and adding a year for each row
    forecast_df['Year'] = datetime.now().year + forecast_df.index
    forecast_df.set_index('Year', inplace=True)
    #pull in initial investment
    initial_investment = investment
    #create a new dataframe to hold the future value of the investment  
    future_value = pd.DataFrame()   
    for f in range(5):
        future_value['Sample ' + str(f+1)] = initial_investment*(1 + forecast_df['Sample ' + str(f+1)]).cumprod()
    #create a column that shows the average return for each year
    future_value['Avg. Return'] = forecast_df.mean(axis=1)
    future_value['Year'] = forecast_df.index
    future_value.set_index('Year', inplace=True)
    return future_value