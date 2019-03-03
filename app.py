'''Investment Research Web-App'''
import dash
import flask
import dash_core_components as dcc
import dash_html_components as html

import requests
import pandas as pd

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
    "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
    "https://cdn.rawgit.com/amadoukane96/8f29daabc5cacb0b7e77707fc1956373/raw/854b1dc5d8b25cd2c36002e1e4f598f5f4ebeee3/test.css",
    "https://use.fontawesome.com/releases/v5.2.0/css/all.css"
]

# Define Dash App
app = dash.Dash(__name__='Scarab', external_css=external_css)
server = app.server

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
                                        style={
                                            "font-size": 16
                                        }
                                    )
                                )
                            ]
                        )
                        for i in range(min(len(dataframe), max_rows))
                    ]
                ),
                style={"height": "150px", "overflowY": "scroll"},
            ),
        ],
        style={"height": "100%"},
    )

DATAFRAME = pd.read_csv('SP500_price.csv')
NAMES = pd.read_csv('constituents.csv')['Name']
LABELS = DATAFRAME.columns.values.tolist()[1:]
REGTEXT = open('regressionText.txt', 'r').readlines()
PREDICTIONS = pd.read_csv('predictiondat.csv')

def regressionText(line):
    return REGTEXT[line-1]

def label_maker(LABELS, NAMES, PREDICTIONS):
    options = []
    map1 = {}
    map2 = {}
    map3 = {}
    for i in range(0, len(LABELS)):
        options.append({'label': NAMES[i], 'value': NAMES[i]})
        map1[NAMES[i]] = LABELS[i]
        if i < 20:
            map2[LABELS[i]] = PREDICTIONS['LM'][i]
            map3[LABELS[i]] = PREDICTIONS['RFM'][i]
    return options, map1, map2, map3

LABELS, MAP, LM, RF = label_maker(LABELS, NAMES, PREDICTIONS)

app.layout = html.Div(style={'backgroundColor': "#1a2d46"}, children=[
    #left column
    html.Div([
        html.Div(
            [
                html.H1(children='Company Statistics', style={
                    'textAlign': 'center',
                    'color': 'white',
                    'fontSize': 24
                }),
                html.Article(id='a1', children='Company Name: ', style={
                    'color': 'white',
                    'fontSize': 16
                }),
                html.Article(id='a2', children='Sector: ', style={
                    'color': 'white',
                    'fontSize': 16
                }),
                html.Article(id='a3', children='Market Cap: ', style={
                    'color': 'white',
                    'fontSize': 16
                }),
                html.Article(id='a6', children='Report Date: ', style={
                    'color': 'white',
                    'fontSize': 16
                }),
                html.Article(id='a7', children='Total Revenue: ', style={
                    'color': 'white',
                    'fontSize': 16
                }),
                html.Article(id='a8', children='Gross Profit: ', style={
                    'color': 'white',
                    'fontSize': 16
                }),
                html.Article(id='a9', children='Current Assets: ', style={
                    'color': 'white',
                    'fontSize': 16
                }),
                dcc.Textarea(rows='4', cols='45', id='my-id', className='noteBox', placeholder='Enter Notes:',
                    style={
                        'height': '500px',
                        'marginTop': '5'
                    }),
            ],
            style={
                "backgroundColor": "#1a2d46",
                "padding": "10",
                "margin": "0",
                "height":"100%"
            },
        ),
        ],
        style={'width': '25%', 'display': 'inline-block', 'height': '900px', 'vertical-align': 'top'}
        ),

    #middle column
    html.Div([
        html.H1(children='Scarab: Investment Research', style={
            'textAlign': 'center',
            'color': 'white'
        }),
        dcc.Dropdown(
            id='dropdown',
            options=LABELS,
            value='Akamai Technologies Inc'
        ),
        dcc.Graph(id='prices'),

        html.Div([
                    html.P('Headlines', style={"fontSize":"16","color":"#45df7e"}),
                    html.Div(get_news('Akamai Technologies Inc'), id="news", style={
                        "height": "100%"
                    })
                    ],
                    style={
                        "backgroundColor": "#1a2d46",
                        "color": "#1a2d46",
                        "fontSize": "12",
                        "padding":"10px 10px 0px 10px",
                        "marginTop":"5",
                        "marginBottom":"0"
                    }),
        ],
        style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top', 'height': '950px'}
        ),

    #right column
    html.Div([
        html.Div(
            [
                html.H1(children="Scarab's Predictions", id='mover-header', style={
                'textAlign': 'center',
                'color': 'white',
                'fontSize': 24
                }),

                #This is the first div for the regression
                html.Div([
                    html.P('Scarab: Linear Regression', className='regression', style={
                        "color":"#45df7e"
                    }),
                    html.P(regressionText(1), className='regression', style={
                        "color": "white"
                    }),
                    html.Article(id='a10', children="Scarab's Linear Model Prediction: ", style={
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': 16
                }),
                ], className='regression', style={
                    'vertical-align': 'middle'
                }),

                #This is the second div for the regression
                html.Div([
                    html.P('Scarab: Random Tree Regression', className='regression', style={
                        "color":"#45df7e"
                    }),
                    html.P(regressionText(2), className='regression', style={
                        'color': 'white'
                    }),
                    html.Article(id='a11', children="Scarab's Random Forest Prediction: ", style={
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': 16
                })
                ], className='regression', style={
                    'vertical-align': 'middle'
                }),
            ],
            style={
                "backgroundColor": "#1a2d46",
                "padding": "10",
                "margin": "0",
                "height":"100%",
            },
        )
        ],
        style={'width': '25%', 'display': 'inline-block', 'float': 'right', 'height': '925px', 'vertical-align': 'top'},
        )
    ]
)

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
                'b': 70,
                't': 50
            },
            'title': 'Stock Prices for ' + selected_dropdown_value,
            'font': {
                "color": "#45df7e"
            },
            'xaxis': {
                'title':'Time',
                "color": "#45df7e"
                #'range': ['2019-02-25', '2019-03-01']
            },
            'yaxis': {
                'title':'Price (USD)',
                "color": "#45df7e"
            },
            'plot_bgcolor': '#1a2d46',
            'paper_bgcolor': '#1a2d46',
        }
    }

#callback for interacting with news
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

# callback for company name
@app.callback(Output('a1', component_property='children'),
              [Input('dropdown', 'value')])
def update_a1(selected_dropdown_value):
    info = informationMap(MAP[selected_dropdown_value])
    return info[0][0]+ ": " + info[0][1]

# callback for company sector
@app.callback(Output('a2', component_property='children'),
              [Input('dropdown', 'value')])
def update_a2(selected_dropdown_value):
    info = informationMap(MAP[selected_dropdown_value])
    return info[1][0]+ ": " + info[1][1]

# callback for market cap
@app.callback(Output('a3', component_property='children'),
              [Input('dropdown', 'value')])
def update_a3(selected_dropdown_value):
    info = informationMap(MAP[selected_dropdown_value])
    return info[2][0]+ ": " + info[2][1]

# callback for report date
@app.callback(Output('a6', component_property='children'),
              [Input('dropdown', 'value')])
def update_a6(selected_dropdown_value):
    info = informationMap(MAP[selected_dropdown_value])
    return info[5][0]+ ": " + info[5][1]

# callback for total revenue
@app.callback(Output('a7', component_property='children'),
              [Input('dropdown', 'value')])
def update_a7(selected_dropdown_value):
    info = informationMap(MAP[selected_dropdown_value])
    return info[6][0]+ ": " + info[6][1]

# callback for gross profit
@app.callback(Output('a8', component_property='children'),
              [Input('dropdown', 'value')])
def update_a8(selected_dropdown_value):
    info = informationMap(MAP[selected_dropdown_value])
    return info[7][0]+ ": " + info[7][1]

# callback for current assets
@app.callback(Output('a9', component_property='children'),
              [Input('dropdown', 'value')])
def update_a9(selected_dropdown_value):
    info = informationMap(MAP[selected_dropdown_value])
    return info[8][0]+ ": " + info[8][1]

# callback for LM
@app.callback(Output('a10', component_property='children'),
              [Input('dropdown', 'value')])
def update_a10(selected_dropdown_value):
    try:
        return "Scarab's Linear Model Prediction: $" + str(LM[MAP[selected_dropdown_value]].round(decimals=2))
    except:
        "Scarab's Linear Model Prediction: UNAVAILABLE"

# callback for LM
@app.callback(Output('a11', component_property='children'),
              [Input('dropdown', 'value')])
def update_a11(selected_dropdown_value):
    try:
        return "Scarab's Random Forest Prediction: $" + str(RF[MAP[selected_dropdown_value]].round(decimals=2))
    except:
        return "Scarab's Predictions: UNAVAILABLE"

if __name__ == '__main__':
    app.run_server(debug=True)
