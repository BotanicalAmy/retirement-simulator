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
from model import retirement_prediction
from page_elements import footer, side_content
from datetime import datetime


st.set_page_config(page_title="AI Forecast", page_icon="🧠")
st.markdown("# Forecast your future with AI 🪄")
st.write("The machine learning model analyzes 10,000 hypothetical returns to develop a customized forecast.")
st.markdown("####")


def ai_forecast():
    input_list = []
    ai_input = [input_list]

    with st.form("Select your retirement options", border = False):
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            #select starting investment value
            st.markdown('**What is your initial investment?**')
            investment = st.number_input(label="Enter your initial investment", label_visibility="collapsed", value=None, placeholder='Type a number...', min_value=10000)
            st.write('The initial investment is $',investment)

            st.markdown('**What type of investor are you?**')
            investor = st.selectbox('What type of investor are you?',
            ('Moderate', 'Aggressive','Conservative', 'Nervous'), label_visibility="collapsed")
        
        with col2:
            #select the number of years to forecast
            st.markdown('**How long will you invest?**')
            years = st.slider('How many years will you invest?', 10, 50, 20, label_visibility="collapsed")
            st.write("I plan to invest for ", years, 'years')

        if investor == 'Aggressive':
          st.markdown('*Aggressive investors have a high risk tolerance and are willing to risk more money for the possibility of better, yet unknown, returns.*')
          investor_code = [1,0,0,0]

        if investor == 'Moderate':
          st.markdown("*Moderate investors want to grow their money without losing too much. Their goal is to weigh opportunities and risks and this investor's approach is sometimes described as a “balanced” strategy.*")
          investor_code = [0,0,1,0]

        if investor == 'Conservative':
          st.markdown('*Conservative investors are willing to accept little to no volatility in their investment portfolios. Retirees or those close to retirement are usually in this category.*')
          investor_code = [0,1,0,0]

        if investor == 'Nervous':
          st.markdown('*Nervous investors have financial anxiety and often react to the market. When the market drops, the nervous investor pulls their money out of the stock market, waiting to reinvest when returns remain positive.*')
          investor_code = [0,0,0,1]
        
        add_inputs = st.form_submit_button("Forecast your Future")
        if add_inputs and investment is not None:
            with st.sidebar:
                with st.status("Forecasting your retirement...", expanded=True) as status:
                    input_list.append(years)
                    input_list.append(investment)
                    input_list.extend(investor_code)

                    st.write("Analyzing your inputs...")
                    prediction = (retirement_prediction(ai_input))

                    status.update(label="Forecast complete!", state="complete", expanded=False)

            annual_income = prediction * 0.04
            monthly_income = annual_income/12
            retirement_year = years + datetime.now().year
            st.markdown(f'In **{years}** years, your investment is predicted to be worth **${prediction[0]:,.0f}**')
            st.markdown(f'Your annual retirement income is predicted to be **\${annual_income[0]:,.0f}**, which is **\${monthly_income[0]:,.0f}** per month.')
            st.markdown(f'*The retirement income is based on a 4% annual withdrawl rate, beginning in {retirement_year}.*')



ai_forecast()

with st.sidebar:
      side_content()

footer()

#add visual for forecast data


