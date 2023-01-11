# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

#app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = Dash(__name__)

by_type = pd.read_parquet('../aggregator/by_type_hour.parquet', engine='pyarrow')
by_from = pd.read_parquet('../aggregator/by_from.parquet', engine='pyarrow').sort_values('from count', ascending=False).head(50)

print(by_type.info())
print(by_from.info())

#print(all_transactions.shape)
# sum of values
transac_total_value = by_type['value sum'].sum()

# number of transactions
num_of_transac = by_type['from count'].sum()



fig1 = px.pie(by_type, values="value sum", names="type", title="value by type")

fig2 = px.bar(by_type, x="type", y="from count", title="number of transactions by type")

fig3 = px.histogram(by_from, x="from", y="from count", title="transactions per payee")

app.layout = html.Div(children=[
    html.H1(children='Ethereum transactions POC'),

    html.Div(children=f'Number of transactions : {num_of_transac}'),

    html.Div(children=f'Total value : {transac_total_value}'),

    dcc.Graph(
        id='value by type',
        figure=fig1
    ),
    dcc.Graph(
        id='number of transactions by type',
        figure=fig2
    ),

    dcc.Graph(
        id='transactions by payee',
        figure=fig3
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

