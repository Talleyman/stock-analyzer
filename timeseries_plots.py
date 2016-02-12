# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from grab_data import extract_data

def time_series_format(ticker, column, ttm_remove=False):
    '''
    Grabs the entries from the full fundamentals data frame and arranges them
      into individual time series
    :param ticker: the ticker for the stock under analysis
    :param column: the name of the column from the data frame to reformat
    :param ttm_remove: boolean parameter for removing the TTM (trailing twelve months)
      row from the time series; defaults to False
    :return: a time series for the column specified
    '''
    data = extract_data(ticker)
    if ttm_remove:
        data.drop('TTM',inplace=True)
    test = pd.Series(data[column],index=data.index)
    return test
    
def plot_layout(ticker, plot_style='ggplot'):
    '''
    Produces the time series plots in a 2 by 2 grid for convenient viewing;
      may make these optional or change the columns plotted in the future
    
    :param ticker: the ticker for the stock under analysis
    :param plot_style: the matplotlib style to use for the time series plots;
      defaults to the ggplot style
    '''
    plt.style.use(plot_style)
    fig, axes = plt.subplots(nrows=2,ncols=2)
    eps = time_series_format(ticker, 'Earnings Per Share USD')
    debt_equity_ratio = time_series_format(ticker, 'Debt/Equity')
    net_margin = time_series_format(ticker, 'Net Margin %')
    fcf = time_series_format(ticker, 'Free Cash Flow USD Mil')
    eps.plot(ax=axes[0,0]).set_title('EPS Growth History')
    debt_equity_ratio.plot(ax=axes[0,1]).set_title('Historic Debt/Equity Ratio')
    net_margin.plot(ax=axes[1,0]).set_title('Net Margin History')
    fcf.plot(ax=axes[1,1]).set_title('Free Cash Flow History')