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
from page_elements import footer, side_content
from function import retirement_income
import pandas as pd
import numpy as np
from datetime import datetime

#getting the future returns dataframe
future_returns = pd.read_csv('data/futurereturns.csv')
#pulling the returns from the futures dataframe, preparation for the forecasting function
aggressive = {'aggressive_investor':list(future_returns['Aggressive Future'])}
moderate = {'moderate_investor': list(future_returns['Moderate Future'])}
conservative = {'conservative_investor':list(future_returns['Conservative Future'])}
nervous = {'nervous_investor':list(future_returns['Aggressive Future'])}


final_year_li = []
investor_li = []
contribution_li = []
initial_value_li = []
future_value_li = []
withrdawl_li = []
income_li = []
monthly_li = []

#fragment needed to isolate the planner functioning and prevent the lists from resetting
@st.experimental_fragment()
def planner():
    st.markdown('''Experiment with different retirement scenarios to plan for your future. The forecasts below are created from the probability based
                retirement simulator. *Final values will vary based on each randomized draw from the return distributions*.''')

    with st.form("Select your retirement options", border = False):
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            #select starting investment value
            st.markdown('**What is your initial investment?**')
            investment = st.number_input(label="Enter your initial investment", label_visibility="collapsed", value=None, placeholder='Type a number...', min_value=10000)
            st.write('The initial investment is $',investment)
            #select yearly contributions
            st.markdown('**What will your annual contribution be?**')
            contribution = st.number_input(label="Enter your annual contribution", label_visibility="collapsed", value=None, placeholder='Type a number...', min_value =0)
            st.write('The annual contribution is $',contribution)
            #select investor type
            st.markdown('**What type of investor are you?**')
            investor = st.selectbox('What type of investor are you?',
            ('Moderate', 'Aggressive','Conservative', 'Nervous'), label_visibility="collapsed")
        with col2:
            #select the number of years to forecast
            st.markdown('**How long will you invest?**')
            years = st.slider('How many years will you invest?', 10, 50, 20, label_visibility="collapsed")
            st.write("I plan to invest for ", years, 'years')
            st.markdown('##')
            #select retirement withrawl rate
            st.markdown('**Select a retirement withdrawl rate**')
            percent = st.radio('Percent withdrawl',['3%', '4% *~recommended*', '5%', '6%'], index=1, label_visibility="collapsed")
            if percent == '3%':
                withdrawl_rate = 0.03
            if percent == '4% *~recommended*':
                withdrawl_rate = 0.04
            if percent == '5%':
                withdrawl_rate = 0.05
            if percent == '6%':
                withdrawl_rate = 0.06
            
        submitted = st.form_submit_button("Plan your Retirement")
        if submitted and investment is not None and contribution is not None:
            if investor == 'Aggressive':
                income = retirement_income(aggressive, investment, contribution, years)
            if investor == 'Moderate':
                income = retirement_income(moderate, investment, contribution, years)
            if investor == 'Conservative':
                income = retirement_income(conservative, investment, contribution, years)
            if investor == 'Nervous':
                income = retirement_income(nervous, investment, contribution, years)
                    
            #make a pretty table of information
            final_year = str(years + datetime.now().year)
            #get last row value of income['With Contribution]
            future_value = income['With Contribution'].iloc[-1]
            annual_income = round(future_value * withdrawl_rate)
            monthly_income = round(annual_income/12)
            column_names=['Final Year', 'Investor', 'Contribution', 'Initial Value', 'Future Value', 'Withdrawl','Income', 'Monthly Inc.']
            #add to the dataframe
            income_df = pd.DataFrame(np.column_stack([final_year, investor, '${:,}/yr'.format(contribution), '${:,}'.format(investment), '${:,.0f}'.format(future_value), '%{:.0f}'.format(withdrawl_rate*100), '${:,}'.format(annual_income), '${:,}'.format(monthly_income)]),
                columns=column_names)
            income_df.set_index('Final Year', inplace=True)

            final_year_li.append(final_year)
            investor_li.append(investor)
            contribution_li.append('${:,}/yr'.format(contribution))
            initial_value_li.append('${:,}'.format(investment))
            future_value_li.append('${:,.0f}'.format(future_value))
            withrdawl_li.append('%{:.0f}'.format(withdrawl_rate*100))
            income_li.append('${:,}'.format(annual_income))
            monthly_li.append('${:,}'.format(monthly_income))
            
            #combine the summary_columns and summary_lists into one dictionary
            st.divider()
            #show just the last row of the dataframe
            st.markdown("### Retirement Plan:")
            #put values to income_summary dictionary
            income_summary =({'Final Year': final_year_li, 'Investor': investor_li, 'Contribution': contribution_li, 
                                'Initial Value':initial_value_li, 'Future Value': future_value_li, 
                                'Withdrawl': withrdawl_li, 'Annual Income': income_li, 
                                'Income/mo.': monthly_li})
            
            #convert income_summary dictionary to dataframe new = pd.DataFrame.from_dict(data)
            income_summary_df = pd.DataFrame.from_dict(income_summary)
            income_summary_df.set_index('Final Year', inplace=True)
            st.dataframe(income_summary_df)



st.set_page_config(page_title="Retirement Income Planner", page_icon="🗒️")
st.markdown("# Retirement Income Planner 🗒️")

with st.sidebar:
    if st.button("Reset the Data"):
        st.session_state.value = "Reset the Data"
        st.rerun()
     # create a download for the data

    side_content()


planner()

footer()