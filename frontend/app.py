import yaml
from sqlalchemy import create_engine
import pandas as pd
from itertools import chain

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as graph_obj

with open('./credentials.yaml', 'r') as f:
    creds = yaml.load(f)


def create_app():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    return app


app = create_app()

app.layout = html.Div([
    html.Div([
        html.Div(html.H2(children='jocka'), style={'display': 'inline-block', 'width': '20%', 'textAlign': 'right'}),
        html.Div(html.Img(src=app.get_asset_url('jocka.jpg'),
                          style={'height': '40%', 'width': '40%'}),
                 style={'display': 'inline-block', 'width': '10%'})]),
    html.Div(id="recent_tweets", style={'padding-left': '15%', 'padding-right': '15%'}),
    html.Div(id="graph"),
    dcc.Interval(id='interval-component', interval=15 * 1000, n_intervals=0)
])

engine = create_engine(
    'postgresql://{0}:{1}@db:5432/scotrugbytweet'.format(creds['postgres']['user'], creds['postgres']['pass']))


@app.callback(Output('graph', 'children'), [Input('interval-component', 'n_intervals')])
def graph(n):
    df_query = pd.read_sql_query("""
    		SELECT entities
    		FROM tweets
    		WHERE timestamp > NOW() - INTERVAL '24 hours'
    		AND LENGTH(entities) > 3
    		""", engine)
    df_query['entities'] = df_query['entities'].apply(lambda row: row[1:-1].split(', '))
    entities = pd.Series([row[1:-1] for row in list(chain(*df_query['entities'].values))])

    N = 10
    top_N_entities = entities.value_counts()[:N]

    x = list(top_N_entities.index)
    y = list(top_N_entities.values)

    bar = graph_obj.Bar(x=x, y=y, name='Results')
    return html.Div([dcc.Graph(id="bar_plot", figure=graph_obj.Figure(data=bar))])


@app.callback(Output('recent_tweets', 'children'), [Input('interval-component', 'n_intervals')])
def most_recent_tweets(n):
    tweets = pd.read_sql_query("""
        		SELECT timestamp, tweet
        		FROM tweets
        		ORDER BY timestamp DESC LIMIT 10
        		""", engine)

    tweets['timestamp'] = pd.to_datetime(tweets['timestamp']).dt.strftime('%B %d, %Y, %X')

    table = dash_table.DataTable(id='table',
                                 columns=[{"name": i, "id": i} for i in tweets.columns],
                                 data=tweets.to_dict('rows'),
                                 style_table={"overflowX": "scroll"},
                                 style_cell={"textAlign": "left"})
    return table


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
