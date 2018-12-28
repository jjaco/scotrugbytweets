from flask import Flask, request, render_template, send_file
from sqlalchemy import create_engine
import pandas as pd
from itertools import chain

import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

engine = create_engine('postgresql://postgres:postgres@localhost:5432/scotrugbytweet')

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

def fig():
    entities.value_counts()[:10].plot(kind='bar')
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return img

@app.route('/graphs')
def graphs():   
    graph = fig()
    return send_file(graph, 
        attachment_filename='plot.png', 
        mimetype='image/png')

if __name__ == '__main__':
    app.run()