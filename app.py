import dash
import dash_core_components as dcc
import dash_html_components as html

import json
import base64
import datetime
import requests

import flask
import pandas as pd


#Define Dash App
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
    "https://cdn.rawgit.com/amadoukane96/8f29daabc5cacb0b7e77707fc1956373/raw/854b1dc5d8b25cd2c36002e1e4f598f5f4ebeee3/test.css",
    "https://use.fontawesome.com/releases/v5.2.0/css/all.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

def get_news(company):
    url = ('https://newsapi.org/v2/everything?'
       'q=' + company + '&'
       'language=en&'
       'apiKey=***REMOVED***')
    r = requests.get(url)
    json_data = r.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title","url"]])
    return generate_news_table(df)

def generate_news_table(dataframe, max_rows=10):
    return html.Div(
        [
            html.Div(
                html.Table(
                    # Header
                    [html.Tr([html.Th()])]
                    +
                    # Body
                    [
                        html.Tr(
                            [
                                html.Td(
                                    html.A(
                                        dataframe.iloc[i]["title"],
                                        href=dataframe.iloc[i]["url"],
                                        target="_blank",
                                    )
                                )
                            ]
                        )
                        for i in range(min(len(dataframe), max_rows))
                    ]
                ),
                style={"height": "150px", "overflowY": "scroll"},
            ),
            html.P(
                "Last update : " + datetime.datetime.now().strftime("%H:%M:%S"),
                style={"fontSize": "11", "marginTop": "4", "color": "#45df7e"},
            ),
        ],
        style={"height": "100%"},
    )

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

app.layout = html.Div([
    #left column
    html.Div([
        html.Div(
            [
                html.Button(id='save-button', n_clicks=0, children='Saved'),
                html.Button(id='note-button', n_clicks=0, children='Notes'),
            ],
            style={
                "backgroundColor": "#1a2d46",
                "padding": "10",
                "margin": "0",
                "height":"100%"
            },
        ),
        ],
        style={'width': '25%', 'display': 'inline-block', 'height': '1000px', 'vertical-align': 'top'}
        ),

    #middle column
    html.Div([
        html.H1('Stock Tickers'),
        dcc.Dropdown(
            id='dropdown',
            options=LABELS,
            value='Advanced Micro Devices Inc'
        ),
        dcc.Graph(id='prices'),

        html.Div([
                    html.P('Headlines',style={"fontSize":"13","color":"#45df7e"}),
                    html.Div(get_news('Advanced Micro Devices Inc'), id="news")
                    ],
                    style={
                        "height":"33%",
                        "backgroundColor": "#18252E",
                        "color": "white",
                        "fontSize": "12",
                        "padding":"10px 10px 0px 10px",
                        "marginTop":"5",
                        "marginBottom":"0"
                    }),
        ],
        style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'height': '100%'}
        ),

    #right column
    html.Div([

        html.Div(
            [
                html.H1('Top Movers', id='mover-header'),
                html.Div(
                    [
                        html.Button(id='ee-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='eee-button', className = 'fullwidth', n_clicks=0, children='eee'),
                        html.Button(id='a-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='aa-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='b-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='bb-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='c-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='cc-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='d-button', className = 'fullwidth', n_clicks=0, children='ee'),
                        html.Button(id='dd-button', className = 'fullwidth', n_clicks=0, children='ee'),
                    ],)
            ],
            style={
                "backgroundColor": "#1a2d46",
                "padding": "10",
                "margin": "0",
                "height":"100%",
            },
        )
        ],
        style={'width': '25%', 'display': 'inline-block', 'float': 'right', 'height': '100%', 'vertical-align': 'top'},
        )
    ]
)

from dash.dependencies import Input, Output
@app.callback(Output('prices', 'figure'),
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

@app.callback(Output('news', component_property='children'),
              [Input('dropdown', 'value')])

def update_news(selected_dropdown_value):
    url = ('https://newsapi.org/v2/everything?'
       'q=' + selected_dropdown_value + '&'
       'language=en&'
       'apiKey=***REMOVED***')
    r = requests.get(url)
    json_data = r.json()["articles"]
    df = pd.DataFrame(json_data)
    df = pd.DataFrame(df[["title","url"]])
    return generate_news_table(df)

if __name__ == '__main__':
    app.run_server(debug=True)
