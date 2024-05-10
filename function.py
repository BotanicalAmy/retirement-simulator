from datetime import datetime
import random
import pandas as pd
import numpy as np
import plotly.express as px


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
    rate_df = pd.DataFrame(forecast_samples)
    return(rate_df)


#enter the investor type (aggressive, moderate, conservative or nervous), the initial investment, and the number of years to forecast
def retirement_forecast(investor, investment, years):
    #use rate sample to create a dataframe of future return rates
    forecast_df = rate_sampler(investor, years)
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
    income_df.drop(columns=['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4', 'Sample 5'], inplace=True)
    #create a column that counts the number of years
    year_count = (income_df.index - income_df.index[0])+1
    #create columns to show the contribution total, the future value of the investment, and the future value with the contribution
    income_df['Contribution']= contribution*year_count
    income_df['Future Value'] = investment*(1 + income_df['Avg. Return']).cumprod()
    income_df['With Contribution'] = (investment + income_df['Contribution'])*(1 + income_df['Avg. Return']).cumprod()
    return income_df

def retirement_plot(data, investment):
    #create a plot of the future values of the investment
    fig = px.line(data.iloc[:, :5], title=f'Future Value of ${investment:,} Investment Portfolio',
                #name the key for the legend
                labels={'value':'Value of Investment', 'Year':'Year'},
                width=900, height=500, markers=True)
    fig.update_layout(
        legend_title="Predicted Returns",
        hoverlabel=dict(bgcolor="white")
        )
    #make the tooltip prettier
    fig.update_traces(mode='markers+lines', xhoverformat='%H:%M', yhoverformat=',.0f', hovertemplate='%{x}: %{y} <extra></extra>')
    fig.update_yaxes(tickprefix="$")
    return fig

def retirement_values(data):
    #print the highest and lowest investment value for the final year, in addition to the average return rate
    final_year = str(data.index[-1])
    highest_value = round(data.iloc[-1, :5].max())
    highest_value_formatted = '${:,}'.format(highest_value)
    lowest_value = round(data.iloc[-1, :5].min())
    lowest_value_formatted = '${:,}'.format(lowest_value)
    average_value = round((highest_value + lowest_value)/2)
    average_value_formatted = '${:,}'.format(average_value)
    return_forecast = (data['Avg. Return'].mean())*100
    return_percent = '%{:.2f}'.format(return_forecast)
    annual_income = average_value * .04
    annual_income_formatted = '${:,.0f}'.format(annual_income)
    monthly_income = annual_income/12
    monthly_income_formatted = '${:,.0f}'.format(monthly_income)
    #put the final_year, highest_value, lowest_value, average_value and return_forecast into a dataframe
    retirement_df = pd.DataFrame(np.column_stack([final_year, highest_value_formatted, lowest_value_formatted ,average_value_formatted, return_percent, annual_income_formatted, monthly_income_formatted]),
        columns=['Final Year', 'Highest Value', 'Lowest Value', 'Average Value', 'Avg. Return Rate', 'Annual Income', 'Monthly Income'])
    retirement_df.set_index('Final Year', inplace=True)

    return retirement_df


