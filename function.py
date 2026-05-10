from datetime import datetime
import random
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


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

#function to sample return rates
def rate_sampler(investor, years):
    forecast_rates = list(investor.values())[0]
    investor_type = list(investor.keys())[0]
    sample_count = 0
    forecast_samples = {}
    rate_df = [0,0]

    #require the user to enter a minimum of 10 years
    if years < 10:
        return('Please enter a forecast period of at least 10 years')
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
                    column_name = 'Scenario ' + str(sample_count+1)
                    forecast_samples[column_name] = rates.copy()
                    sample_count += 1
            elif investor_type == 'conservative_investor' or investor_type == 'moderate_investor':
                column_name = 'Scenario ' + str(sample_count+1)
                forecast_samples[column_name] = rates.copy()
                sample_count += 1
        else:
            pass
    #create dataframe from the dictionary
    rate_df = pd.DataFrame(forecast_samples)
    return(rate_df)


#second version: random sampling for years < 10, constrained sampling for years >= 10
def rate_sampler_v2(investor, years):
    forecast_rates = list(investor.values())[0]
    investor_type = list(investor.keys())[0]
    sample_count = 0
    forecast_samples = {}

    while sample_count < 5:
        if years < 10:
            rates = random.sample(forecast_rates, years)
            column_name = 'Scenario ' + str(sample_count+1)
            forecast_samples[column_name] = rates.copy()
            sample_count += 1
        else:
            rates = random.sample(forecast_rates, years)
            negative = negative_counter(rates)
            positive_change = positive_change_counter(rates)
            if positive_change >= 40 and positive_change <= 50:
                if investor_type == 'aggressive_investor':
                    if negative >= 10:
                        column_name = 'Scenario ' + str(sample_count+1)
                        forecast_samples[column_name] = rates.copy()
                        sample_count += 1
                elif investor_type == 'conservative_investor' or investor_type == 'moderate_investor':
                    column_name = 'Scenario ' + str(sample_count+1)
                    forecast_samples[column_name] = rates.copy()
                    sample_count += 1

    return pd.DataFrame(forecast_samples)

#function to calculate the geometric mean of the return rates
def geometric_mean(df):
    geometric_return = ((df['Geometric Return'].prod())**(1/len(df)) -1)*100
    return geometric_return


#enter the investor type (aggressive, moderate, conservative or nervous), the initial investment, and the number of years to forecast
#contribution is added at the end of each year after growth is applied
def retirement_forecast(investor, investment, years, contribution=0):
    forecast_df = rate_sampler(investor, years) if years >= 10 else rate_sampler_v2(investor, years)
    #create  year column, starting with the current year and adding a year for each row
    forecast_df['Year'] = datetime.now().year + forecast_df.index
    forecast_df.set_index('Year', inplace=True)
    #create a new dataframe to hold the future value of the investment
    future_value = pd.DataFrame()
    for f in range(5):
        rates = list(forecast_df['Scenario ' + str(f+1)])
        fv = investment
        scenario_values = []
        for rate in rates:
            fv = fv * (1 + rate) + contribution
            scenario_values.append(fv)
        future_value['Scenario ' + str(f+1)] = scenario_values
    future_value.index = forecast_df.index
    #create a column that shows the average return for each year
    future_value['Avg. Return'] = forecast_df.mean(axis=1)
    #adding geometric return
    future_value['Geometric Return'] = (future_value['Avg. Return'] + 1)
    future_value['Year'] = forecast_df.index
    future_value.set_index('Year', inplace=True)
    return future_value

def retirement_forecast_v2(investor, investment, years, contribution=0):
    forecast_df = rate_sampler_v2(investor, years)
    forecast_df['Year'] = datetime.now().year + forecast_df.index
    forecast_df.set_index('Year', inplace=True)
    future_value = pd.DataFrame()
    for f in range(5):
        rates = list(forecast_df['Scenario ' + str(f+1)])
        fv = investment
        scenario_values = []
        for rate in rates:
            fv = fv * (1 + rate) + contribution
            scenario_values.append(fv)
        future_value['Scenario ' + str(f+1)] = scenario_values
    future_value.index = forecast_df.index
    future_value['Avg. Return'] = forecast_df.mean(axis=1)
    future_value['Geometric Return'] = (future_value['Avg. Return'] + 1)
    future_value['Year'] = forecast_df.index
    future_value.set_index('Year', inplace=True)
    return future_value

def retirement_income(investor, investment, contribution, years):
    #use the rate sampler to create a dataframe of future return rates
    forecast_df = rate_sampler(investor, years)
    #create  year column, starting with the current year and adding a year for each row
    forecast_df['Year'] = datetime.now().year + forecast_df.index
    forecast_df.set_index('Year', inplace=True)
    #create a new dataframe that averages the 5 sample columns as one average return rate
    income_df = forecast_df.copy()
    #average the 5 samples
    income_df['Avg. Return'] = forecast_df.mean(axis=1)
    #adding geometric return
    income_df['Geometric Return'] = (income_df['Avg. Return'] + 1)
    income_df.drop(columns=['Scenario 1', 'Scenario 2', 'Scenario 3', 'Scenario 4', 'Scenario 5'], inplace=True)
    #create a column that counts the number of years
    year_count = (income_df.index - income_df.index[0])+1
    #create columns to show the contribution total, the future value of the investment, and the future value with the contribution
    income_df['Contribution']= contribution*year_count
    income_df['Future Value'] = investment*(1 + income_df['Avg. Return']).cumprod()
    income_df['With Contribution'] = (investment + income_df['Contribution'])*(1 + income_df['Avg. Return']).cumprod()
    return income_df

def retirement_plot(data, investment, contribution=0):
    #create a plot of the future values of the investment
    title = f'Future Value of ${investment:,} Investment Portfolio'
    if contribution > 0:
        title += f' + ${contribution:,}/yr Contributions'
    fig = px.line(data.iloc[:, :5], title=title,
                labels={'value':'Portfolio Value', 'Year':'Year'},
                width=900, height=500, markers=True,
                color_discrete_sequence=['#7f3c3c', '#cc9a48', '#3c5139', '#54758e', '#59579e'])
    fig.update_layout(
        title=dict(text=title, pad=dict(l=20), font=dict(size=15, color='#374151')),
        legend_title="Predicted Returns",
        hoverlabel=dict(bgcolor="white"),
        paper_bgcolor='#f7f7f9',
        plot_bgcolor='#f7f7f9',
        margin=dict(t=60, b=40, l=60, r=20),
        font=dict(color='#374151', size=14),
        xaxis=dict(title=dict(text='Year', font=dict(size=14, color='#374151')), tickfont=dict(size=14, color='#374151')),
        yaxis=dict(tickprefix='$', tickformat=',.0f', tickfont=dict(size=14, color='#374151')),
    )
    fig.update_traces(mode='markers+lines', yhoverformat=',.0f', hovertemplate='%{x}: %{y} <extra></extra>')
    return fig

def lifecycle_chart(investor, investment, years, contribution, projected_value, withdrawl_rate, current_income=None, other_income=0, inflation_rate=0.025, post_retirement_years=30):
    current_year = datetime.now().year
    rates = list(investor.values())[0]
    mean_return = float(np.exp(np.mean(np.log([1 + r for r in rates]))) - 1)

    # Pre-retirement accumulation
    pre_years = list(range(current_year, current_year + years))
    pre_income, pre_interest, pre_base = [], [], []
    portfolio = investment
    for i in range(years):
        pre_base.append(portfolio)
        interest = portfolio * mean_return
        pre_interest.append(max(interest, 0))
        pre_income.append(current_income * (1 + inflation_rate) ** i if current_income else 0)
        portfolio = portfolio + interest + contribution

    # Post-retirement distribution
    post_years = list(range(current_year + years, current_year + years + post_retirement_years))
    post_interest, post_withdrawal, post_base, post_other_income = [], [], [], []
    annual_withdrawal = projected_value * withdrawl_rate
    portfolio = projected_value
    for i in range(post_retirement_years):
        post_base.append(max(portfolio, 0))
        post_other_income.append(other_income * 12 * (1 + inflation_rate) ** i if other_income else 0)
        if portfolio <= 0:
            post_interest.append(0)
            post_withdrawal.append(0)
            continue
        interest = portfolio * mean_return
        withdrawal = annual_withdrawal * (1 + inflation_rate) ** i
        post_interest.append(max(interest, 0))
        post_withdrawal.append(withdrawal)
        portfolio = portfolio + interest - withdrawal

    all_years = pre_years + post_years
    all_base = pre_base + post_base
    all_interest = pre_interest + post_interest
    income_vals = pre_income + [0] * post_retirement_years
    withdrawal_vals = [0] * years + post_withdrawal
    other_income_vals = [0] * years + post_other_income

    fig = go.Figure()

    # Stack order (bottom to top): income/pension/withdrawal → portfolio value → growth
    if current_income:
        fig.add_trace(go.Bar(
            x=all_years, y=income_vals,
            name='Income', marker_color='#3c5139', legendrank=1,
            hovertemplate='%{x}: $%{y:,.0f}<extra>Income</extra>'
        ))

    if other_income:
        fig.add_trace(go.Bar(
            x=all_years, y=other_income_vals,
            name='Pension / Social Security', marker_color='#cc9a48', legendrank=2,
            hovertemplate='%{x}: $%{y:,.0f}<extra>Pension / Social Security</extra>'
        ))

    fig.add_trace(go.Bar(
        x=all_years, y=withdrawal_vals,
        name='Annual Withdrawal', marker_color='#7a4646', legendrank=3,
        hovertemplate='%{x}: $%{y:,.0f}<extra>Withdrawal</extra>'
    ))

    fig.add_trace(go.Bar(
        x=all_years, y=all_interest,
        name='Portfolio Growth', marker_color='#54758e', legendrank=4,
        hovertemplate='%{x}: $%{y:,.0f}<extra>Portfolio Growth</extra>'
    ))

    fig.add_trace(go.Bar(
        x=all_years, y=all_base,
        name='Portfolio Value', marker_color='#c7c2d6', legendrank=5,
        hovertemplate='%{x}: $%{y:,.0f}<extra>Portfolio Value</extra>'
    ))

    retirement_year = current_year + years
    fig.update_layout(
        barmode='stack',
        title='',
        xaxis=dict(title=dict(text='Year', font=dict(size=14, color='#374151')), tickfont=dict(size=14, color='#374151')),
        yaxis=dict(tickprefix='$', tickformat=',.0f', tickfont=dict(size=14, color='#374151')),
        shapes=[{
            'type': 'line',
            'x0': retirement_year - 0.5, 'x1': retirement_year - 0.5,
            'y0': 0, 'y1': 1, 'yref': 'paper',
            'line': {'color': '#374151', 'width': 2, 'dash': 'dash'}
        }],
        annotations=[{
            'x': retirement_year - 0.5, 'y': 1, 'yref': 'paper',
            'text': f'  Retirement {retirement_year}',
            'showarrow': False, 'xanchor': 'left',
            'font': {'size': 14, 'color': '#374151'}
        }],
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hoverlabel=dict(bgcolor='white'),
        height=450,
        margin=dict(t=80, b=40, l=60, r=20),
        paper_bgcolor='#f7f7f9',
        plot_bgcolor='#f7f7f9',
    )
    return fig


def retirement_values(data, withdrawl_rate=0.04):
    #print the highest and lowest investment value for the final year, in addition to the average return rate
    final_year = str(data.index[-1])
    highest_value = round(data.iloc[-1, :5].max())
    highest_value_formatted = '${:,}'.format(highest_value)
    lowest_value = round(data.iloc[-1, :5].min())
    lowest_value_formatted = '${:,}'.format(lowest_value)
    average_value = round((highest_value + lowest_value)/2)
    average_value_formatted = '${:,}'.format(average_value)
    geometric = geometric_mean(data)
    geometric_percent = '{:.2f}%'.format(geometric)
    annual_income = average_value * withdrawl_rate
    annual_income_formatted = '${:,.0f}'.format(annual_income)
    monthly_income = annual_income/12
    monthly_income_formatted = '${:,.0f}'.format(monthly_income)
    retirement_df = pd.DataFrame(np.column_stack([final_year, highest_value_formatted, lowest_value_formatted, average_value_formatted, geometric_percent, '{:.0f}%'.format(withdrawl_rate*100), annual_income_formatted, monthly_income_formatted]),
        columns=['Final Year', 'Highest Value', 'Lowest Value', 'Average Value', 'Return Rate', 'Withdrawl Rate', 'Annual Income', 'Monthly Income'])
    retirement_df.set_index('Final Year', inplace=True)
    return retirement_df


