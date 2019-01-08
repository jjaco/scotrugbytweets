from flask import Flask, request, render_template, send_file
from sqlalchemy import create_engine
import pandas as pd
from itertools import chain

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

import io
import base64

app = Flask(__name__)

engine = create_engine('postgresql://postgres:postgres@db:5432/scotrugbytweet')

df_query = (
	pd.read_sql("""
		SELECT entities 
		FROM tweets 
		WHERE timestamp > NOW() - INTERVAL '24 hours'
		AND LENGTH(entities) > 3
		""", engine)
	)
df_query['entities'] = df_query['entities'].apply(lambda row: row[1:-1].split(', '))
entities = pd.Series([row[1:-1] for row in list(chain(*df_query['entities'].values))])

@app.route('/dash')
def bokeh():

    N = 10
    top_N_entities = entities.value_counts()[:N]

    x = list(top_N_entities.index)
    y = list(top_N_entities.values)

    fig = figure(plot_width=600, plot_height=600, x_range=x)
    fig.vbar(
        x=x,
        top=y,
        color='navy',
        width=0.9
    )

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)


if __name__ == '__main__':
    app.run(host='0.0.0.0')