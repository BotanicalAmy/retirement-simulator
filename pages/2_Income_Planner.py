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

def planner():
    st.write("Add page content")


    with st.form("Select your retirement options", border = False):
      col1, col2 = st.columns(2, gap="medium")

      with col1:
        #select starting investment value
        st.markdown('**What is your initial investment?**')
        investment = st.number_input(label="Enter your initial investment", label_visibility="collapsed", value=None, placeholder='Type a number...', min_value=10000)
        st.write('The initial investment is $',investment)

        #select yearly contributions
        st.markdown('**What will your annual contribution be?**')
        contribution = st.number_input(label="Enter your annual contribution", label_visibility="collapsed", value=None, placeholder='Type a number...', min_value =100)
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
      if submitted and investment is not None:
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
        #add to the dataframe
        income_df = pd.DataFrame(np.column_stack([final_year, investor, '${:,}/yr'.format(contribution), '${:,}'.format(investment), '${:,.0f}'.format(future_value), '%{:.0f}'.format(withdrawl_rate*100), '${:,}/yr'.format(annual_income), '${:,}/mo'.format(monthly_income)]),
            columns=['Final Year', 'Investor', 'Contribution', 'Initial Value', 'Future Value', 'Withdrawl','Income', 'Monthly Inc.'])
        income_df.set_index('Final Year', inplace=True)

        #add values to income_summary dictionary
        income_summary =({'Final Year': final_year, 'Investor': investor, 'Contribution': '${:,}/yr'.format(contribution), 
                               'Initial Value': '${:,}'.format(investment), 'Future Value': '${:,.0f}'.format(future_value), 
                               'Withdrawl': '%{:.0f}'.format(withdrawl_rate*100), 'Income': '${:,}/yr'.format(annual_income), 
                               'Monthly Inc.': '${:,}/mo'.format(monthly_income)})
        

        st.divider()
        #show just the last row of the dataframe
        st.markdown("### Retirement income plan:")
        st.dataframe(income_df)
        #create dataframe from income summary dictionary
        # st.write(income_summary)
        # income_summary = summary_build
        st.write(income_summary)





st.set_page_config(page_title="Retirement Income Planner", page_icon="🗒️")
st.markdown("# Retirement Income Planner")

with st.sidebar:
    side_content()


planner()

footer()