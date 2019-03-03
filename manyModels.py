import numpy as np
import pandas as pd
import iexfinance.stocks as iex
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import SGDRegressor

from datetime import datetime

def makeLinearModel(ticker, start, end):
    '''
    Given a start, and ending date, we can calculate a linear regressionself.
    '''
    historicalData = iex.get_historical_data(ticker, start, end, output_format = 'pandas')
    historicalData = historicalData.values
    Data_X = []
    Data_Y = []
    for i in range(len(historicalData) - 1):
        Data_X.append([historicalData[i][0], historicalData[i][4]])
        Data_Y.append([historicalData[i+1][0]])
    linear = LinearRegression()
    linear.fit(Data_X, Data_Y)
    stock = iex.Stock(ticker)
    currentDay = [[stock.get_price(),stock.get_volume()]]
    return (linear.predict(Data_X), linear.predict(currentDay))

def randomForestModel(ticker, start, end):
    '''
    Given a start, and ending date, we can calculate a linear regressionself.
    '''
    historicalData = iex.get_historical_data(ticker, start, end, output_format = 'pandas')
    historicalData = historicalData.values
    Data_X = []
    Data_Y = []
    for i in range(len(historicalData) - 1):
        Data_X.append([historicalData[i][0], historicalData[i][4]])
        Data_Y.append([historicalData[i+1][0]])
    Data_X = np.array(Data_X)
    Data_Y = np.array(Data_Y)
    forest = RandomForestRegressor(max_depth=10, n_estimators=100)
    forest.fit(Data_X, Data_Y.ravel())
    stock = iex.Stock(ticker)
    currentDay = [[stock.get_price(),stock.get_volume()]]
    return (forest.predict(Data_X), forest.predict(currentDay))

def makeSGDRegressor(ticker, start, end):
    '''
    Given a start, and ending date, we can calculate a linear regressionself.
    '''
    historicalData = iex.get_historical_data(ticker, start, end, output_format = 'pandas')
    historicalData = historicalData.values
    Data_X = []
    Data_Y = []
    for i in range(len(historicalData) - 1):
        Data_X.append([historicalData[i][0], historicalData[i][4]])
        Data_Y.append([historicalData[i+1][0]])
    Data_X = np.array(Data_X)
    Data_Y = np.array(Data_Y)
    regressor = RandomForestRegressor()
    regressor.fit(Data_X, Data_Y.ravel())
    stock = iex.Stock(ticker)
    currentDay = [[stock.get_price(),stock.get_volume()]]
    return (regressor.predict(Data_X), regressor.predict(currentDay))
