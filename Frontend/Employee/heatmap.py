import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_table

# Load the reviews data from a CSV file (change the file path accordingly)
reviews_data = pd.read_csv('../../Data/reviews1_data.csv')

# Assuming the data has the following columns: group, year, month, rating, helpful

# Create a Dash application
app = Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Heatmap of Ratings In Current Trends", style={'text-align': 'center'}),
    dcc.Dropdown(
        id='group-dropdown',
        options=[{'label': group, 'value': group} for group in reviews_data['group'].unique()],
        value='Book',
        style={'width': '50%', 'margin': 'auto'}
    ),
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
    dcc.Graph(id='heatmap-graph')
])


# Define the callback to update the heatmap
@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('group-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_heatmap(selected_group, selected_month, selected_year):

    heatmap_data = reviews_data[
        (reviews_data['group'] == selected_group) &
        (reviews_data['year'] == selected_year) &
        (reviews_data['month'] == selected_month)
    ].groupby('rating')['helpful'].mean().reset_index()

    # Create the heatmap using plotly.graph_objects
    fig = go.Figure(go.Heatmap(
        x=heatmap_data['rating'],
        y=[0],  # Y-axis is set to [0] to have a 1D heatmap
        z=[heatmap_data['helpful']],
        colorscale='Viridis',
        hoverongaps=False,
    ))

    fig.update_layout(
        xaxis=dict(title='Rating'),
        yaxis=dict(title=''),  # Empty y-axis label
        title='Heatmap of Ratings In Current Trends',
        template='plotly_dark',
        showlegend=False
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
