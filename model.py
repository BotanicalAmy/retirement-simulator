#importing functions for the machine learning model
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np


inputs = [[25, 250000, 0,1,0,0]]

def retirement_prediction(pred_inputs):
    #convert the forecast_results csv file into a dataframe
    forecast_results = pd.read_csv('data/forecast_results.csv')
    forecast_results.drop('Unnamed: 0', axis=1, inplace=True)

    #converting the investor type into a numerical value
    forecast_results_num = pd.get_dummies(forecast_results, columns=['Investor Type'])

    #splitting the data into training and testing sets
    X = forecast_results_num.drop('Final Value', axis=1)
    y = forecast_results_num['Final Value']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #knn pipeline
    k_pipe = Pipeline(steps=[('scaler', StandardScaler()),
                    ('regression', KNeighborsRegressor())])
    k_grid = GridSearchCV(estimator=k_pipe, n_jobs=-1, param_grid={'regression__n_neighbors': [3, 5, 7, 9, 11], 'regression__metric': ['euclidean', 'minkowski','manhattan'], 'regression__weights': ['uniform', 'distance']})
    k_grid = k_grid.fit(X_train, y_train)
    # k_pred = k_grid.predict(X_test)

    prediction = k_grid.predict(pred_inputs)
    return prediction

    # print(f'The predicted final value of the portfolio is: ${prediction[0]:,.0f}')


def IQR(dist):
    return np.percentile(dist, 75) - np.percentile(dist, 25)

def Q1(dist):
    return np.percentile(dist, 25)

def Q3(dist):
    return np.percentile(dist, 75)

def confidence_interval(dist):
  dist_avg = np.mean(dist)
  dist_std = np.std(dist)
  conf_top = ((dist_avg + (2 * dist_std))*100)
  conf_bottom = ((dist_avg - (2 * dist_std))*100)
  return round(conf_bottom,2), round(conf_top,2)
