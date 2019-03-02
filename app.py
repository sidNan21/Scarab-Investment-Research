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

#Define Dash App
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
                html.Button(id='save-button', className='fullwidth', n_clicks=0, children='Saved'),
                html.Button(id='note-button', className='fullwidth', n_clicks=0, children='Notes'),
            ],
            style={
                "backgroundColor": "#1a2d46",
                "padding": "10",
                "margin": "0",
                "height":"100%"
            },
        ),
        ],
        style={'width': '25%', 'display': 'inline-block', 'height': '100%', 'vertical-align': 'top'}
        ),

    #middle column
    html.Div([
        html.H1('Scarab: Smart Investments'),
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
                        "backgroundColor": "#1a2d46",
                        "color": "#1a2d46",
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
                        html.Button(id='button-1', className='fullwidth', n_clicks=0, children='BPTH'),
                        html.Button(id='button-2', className='fullwidth', n_clicks=0, children='CIFS'),
                        html.Button(id='button-3', className='fullwidth', n_clicks=0, children='PBYI'),
                        html.Button(id='button-4', className='fullwidth', n_clicks=0, children='GSB'),
                        html.Button(id='button-5', className='fullwidth', n_clicks=0, children='LXRX'),
                        html.Button(id='button-6', className='fullwidth', n_clicks=0, children='IMGN'),
                        html.Button(id='button-7', className='fullwidth', n_clicks=0, children='XON'),
                        html.Button(id='button-8', className='fullwidth', n_clicks=0, children='NTNX'),
                        html.Button(id='button-9', className='fullwidth', n_clicks=0, children='MAXR'),
                        html.Button(id='button-10', className='fullwidth', n_clicks=0, children='IMV'),
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
