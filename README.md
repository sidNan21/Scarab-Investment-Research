# Scarab: Smarter Investment Research

## Description

A Dash based web-application designed to provide novice investors a "one-stop-shop" for researching popular equities

+ Provides timeseries data of price over the lifetime of the equity using Plotly.py
+ Supplies relevant statistics to the equity being researched via the IEX and Quandl APIs
+ Showcases up-to-date headlines on researched companies using News API
+ Highlights popular and commonly traded equities based on statistically analyzed market movements
+ Allows users to take notes and save articles during research

## References

The higher level technologies used are:

+ [Plotly](https://plot.ly) for interactive data data visualization
+ [Dash](https://plot.ly/products/dash/) as a framwork for creating the web application
+ [News API](https://newsapi.org) provides access to relevant news for each equity
+ [IEX API](https://iextrading.com/developer/docs/) provides access to financial data
+ [Quandl API](https://www.quandl.com/tools/api) provides access to financial data

## Running the web applet

The following libraries (and their dependencies) will need to be installed if not already present:

+ plotly `pip install plotly`
+ dash `pip install dash==0.38.0`
+ dash-html-components `pip install dash-html-components==0.13.5`
+ dash-core-components `pip install dash-core-components==0.43.1`
+ dash-table `pip install dash-table==3.5.0`
+ dash-daq `pip install dash-daq==0.1.0`
+ flask `pip install flask`
+ requests `pip install requests`
+ pandas `pip install pandas`

In addition, you will need to obtain and add a News API key in `app.py` in the `get_news()` and `update_news()` methods. NewsAPI is linked above in the "References" section of this document.

You can run the Dash app locally by executing `python3 app.py`. Make sure to have 'SP500_price.csv' and 'constituents.csv' in the same directory as the applet.

A live deployment of the app can be found at URL

## Environment

This project was developed with Python 3.6

## Contributers

+ [Cory Kim](https://www.linkedin.com/in/coryjkim/)
+ [Siddharth Nanda](https://www.linkedin.com/in/sidNan21)
+ [Dale Wilson](https://www.linkedin.com/in/dale-wilson-4a3893150/)
+ [Richard Wang](https://www.linkedin.com/in/yicheng-richard-wang-5b198a149/)
