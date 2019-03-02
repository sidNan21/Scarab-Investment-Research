import iexfinance.stocks as iex
import re

def informationMap(ticker):
    '''
    Input: Ticker (ie TSLA)
    Output: A list of tuples, that contain all the basic informaiton of the stock.
    '''
    stock = iex.Stock(ticker)
    financials = ['reportDate','totalRevenue', 'grossProfit', 'currentAssets']
    infoMap = []
    infoMap.append(('Company Name', stock.get_company_name()))
    infoMap.append(('Sector', stock.get_sector()))
    infoMap.append(('Market Cap','$'+str(stock.get_market_cap())))
    infoMap.append(('Volume',(stock.get_market_cap())))
    infoMap.append(('Most Recent EPS',stock.get_latest_eps() ))
    for metric in financials:
        if(metric == 'reportDate'):
            infoMap.append((convert(metric),' '+str(stock.get_financials()[0][metric])))
        else:
            infoMap.append((convert(metric),' $'+str(stock.get_financials()[0][metric])))

    infoMap.append(('Beta', stock.get_beta()))
    return infoMap


def convert(name):
    '''
    Receives a name in came case, then returns the name in normal "Title" Case.
    '''
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower().title()
