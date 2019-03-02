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

def update_news():
    r = requests.get('https://newsapi.org/v2/top-headlines?sources=financial-times&apiKey=***REMOVED***')
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
        style={'width': '25%', 'display': 'inline-block', 'height': '100%', 'vertical-align': 'top'}
        ),

    #middle column
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montreal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
                ],
            value=['MTL', 'SF'],
            multi=True
        ),

        dcc.Graph(
            id='example-graph3',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar'}
                ],
                'layout': {
                    'title': 'Dash Data Visualization',
                    'height':250
                    }
                }
            ),

        html.Div([
                    html.P('Headlines',style={"fontSize":"13","color":"#45df7e"}),
                    html.Div(update_news(),id="news")
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
                        html.Button(id='ee-button', n_clicks=0, children='ee'),
                        html.Button(id='eee-button', n_clicks=0, children='eee')
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


if __name__ == '__main__':
    app.run_server(debug=True)
