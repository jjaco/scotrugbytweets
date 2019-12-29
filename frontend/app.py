from flask import Flask, request, render_template, send_file
from sqlalchemy import create_engine
import pandas as pd
from itertools import chain

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as graph_obj


def create_app():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    return app


app = create_app()

app.layout = html.Div([
    html.H2(children='jocka'),
    html.Button("Query", id="query_data"),
    html.Div(id="graph")
])

engine = create_engine('postgresql://postgres:postgres@db:5432/scotrugbytweet')

df_query = pd.read_sql_query("""
		SELECT entities
		FROM tweets
		WHERE timestamp > NOW() - INTERVAL '24 hours'
		AND LENGTH(entities) > 3
		""", engine)
df_query['entities'] = df_query['entities'].apply(lambda row: row[1:-1].split(', '))
entities = pd.Series([row[1:-1] for row in list(chain(*df_query['entities'].values))])


@app.callback(Output('graph', 'children'), [Input('query_data', component_property='n_clicks')])
def graph(n):
    N = 10
    top_N_entities = entities.value_counts()[:N]

    print(top_N_entities)

    x = list(top_N_entities.index)
    y = list(top_N_entities.values)

    bar = graph_obj.Bar(x=x, y=y, name='Results')
    return html.Div([dcc.Graph(id="bar_plot", figure=graph_obj.Figure(data=bar))])


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
