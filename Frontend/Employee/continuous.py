import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from datetime import datetime as dt

# Load the profit data from a CSV file (change the file path accordingly)
profit_data = pd.read_csv('../../Data/reviews1_data.csv')

# Assuming the data has the following columns: year, month, day, profit

# Convert the 'time' column to a pandas datetime object
profit_data['datetime'] = pd.to_datetime(profit_data[['year', 'month', 'day']])

# Create a Dash application
app = Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Company Profit over datetime", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='group-dropdown',
        options=[{'label': group, 'value': group} for group in profit_data['group'].unique()],
        value='Book',
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.DatePickerRange(
        id='date-range',
        start_date=dt(2000, 6, 1),
        end_date=dt(2000, 6, 30),
        display_format='YYYY-MM-DD',
        style={'margin': 'auto'}
    ),
    dcc.Graph(id='profit-graph')
])


# Define the callback to update the graph
@app.callback(
    Output('profit-graph', 'figure'),
    [Input('group-dropdown', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graph(selected_group, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered_data = profit_data[
        (profit_data['group'] == selected_group) &
        (profit_data['datetime'] >= start_date) &
        (profit_data['datetime'] <= end_date)
    ]

    # Create the graph using plotly.graph_objects
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_data['datetime'],
        y=filtered_data['profit'],
        mode='markers+lines',
        marker=dict(size=8, color='purple', line=dict(width=2, color='DarkSlateGrey')),
        line=dict(width=2, color='purple'),
        name='Profit'
    ))

    fig.update_layout(
        xaxis=dict(title='Datetime'),
        yaxis=dict(title='Profit'),
        title=f'Company Profit over datetime in {selected_group}',
        template='plotly_dark',
        showlegend=True
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
