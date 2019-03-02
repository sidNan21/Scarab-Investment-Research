'''Visualization of stock prices by ticker'''

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd

SERVER = flask.Flask('app')
APP = dash.Dash('app', server=SERVER)

DATAFRAME = pd.read_csv('SP500_price.csv')
NAMES = pd.read_csv('constituents.csv')['Name']
LABELS = DATAFRAME.columns.values.tolist()[1:]

def label_maker(LABELS, NAMES):
    options = []
    map1 = {}
    for i in range(0, len(LABELS)):
        options.append({'label': NAMES[i], 'value': NAMES[i]})
        map1[NAMES[i]] = LABELS[i]
    return options, map1

LABELS, MAP = label_maker(LABELS, NAMES)

APP.layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='dropdown',
        options=LABELS,
        value='Advanced Micro Devices Inc'
    ),
    dcc.Graph(id='prices')
], className="container")

@APP.callback(Output('prices', 'figure'),
              [Input('dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dff = DATAFRAME[MAP[selected_dropdown_value]]
    return {
        'data': [{
            'x': DATAFRAME['date'],
            'y': dff,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 50,
                'r': 50,
                'b': 50,
                't': 50
            },
            'title': 'Stock Prices for ' + selected_dropdown_value,
            'xaxis': {
                'title':'Time',
                #'range': ['2019-02-25', '2019-03-01']
            },
            'yaxis': {
                'title':'Price (USD)'
            }
        }
    }

if __name__ == '__main__':
    APP.run_server(debug=True)
