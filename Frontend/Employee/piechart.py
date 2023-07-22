import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import datetime as dt

# Load the reviews data from a CSV file (change the file path accordingly)
reviews_data = pd.read_csv('../../Data/reviews1_data.csv')

# Create a Dash application
app = Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("User Interactions per Category", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': month, 'value': month} for month in reviews_data['month'].unique()],
        value=6,
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in reviews_data['year'].unique()],
        value=2000,
        style={'width': '50%', 'margin': 'auto'}
    ),
    dcc.Graph(id='pie-chart')
])


# Define the callback to update the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_pie_chart(selected_month, selected_year):
    filtered_data = reviews_data[
        (reviews_data['year'] == selected_year) &
        (reviews_data['month'] == selected_month)
    ]

    # Group the filtered data by 'group' and calculate the total interactions per category
    interactions_per_category = filtered_data.groupby('group')['rating'].sum()

    # Create the pie chart using plotly.graph_objects
    fig = go.Figure(data=[go.Pie(
        labels=interactions_per_category.index,
        values=interactions_per_category,
        textinfo='percent',
        hoverinfo='label+percent',
        marker=dict(colors=px.colors.sequential.Viridis)
    )])

    fig.update_layout(
        title=f'User Interactions per Category in {selected_month}-{selected_year}',
        template='plotly_dark',
        showlegend=True
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
