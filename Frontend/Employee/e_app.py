import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Step 1: Initialize the Dash app
app = dash.Dash(__name__)

# Step 2: Load data (optional)
# Assuming you have a CSV file named 'data.csv' with the required data
data = pd.read_csv('data.csv')

# Step 3: Design the layout with custom CSS
app.layout = html.Div(
    style={'backgroundColor': '#f0f0f0', 'textAlign': 'center'},  # Align title to the center
    children=[
        html.H1("My Dash Web App"),  # Title centered
        html.Div([
            html.Label('Select date:', style={'fontSize': '18px'}),  # Reduce the label font size
            dcc.Dropdown(
                id='dropdown',
                options=[
                    {'label': 'Date', 'value': 'option1'},
                    {'label': 'Month', 'value': 'option2'},
                    {'label': 'Year', 'value': 'option3'}
                ],
                value='option1',
                style={'fontSize': '14px', 'width': '200px'}  # Reduce the dropdown option font size and width
            ),
            dcc.Dropdown(
                id='dropdown2',
                options=[
                    {'label': 'Option 1', 'value': 'option1'},
                    {'label': 'Option 2', 'value': 'option2'},
                    {'label': 'Option 3', 'value': 'option3'}
                ],
                value='option1',
                style={'fontSize': '14px', 'width': '200px'}  # Reduce the dropdown option font size and width
            ),
            dcc.Dropdown(
                id='dropdown3',
                options=[
                    {'label': 'Option 1', 'value': 'option1'},
                    {'label': 'Option 2', 'value': 'option2'},
                    {'label': 'Option 3', 'value': 'option3'}
                ],
                value='option1',
                style={'fontSize': '14px', 'width': '200px'}  # Reduce the dropdown option font size and width
            ),
            dcc.Dropdown(
                id='dropdown4',
                options=[
                    {'label': 'Option 1', 'value': 'option1'},
                    {'label': 'Option 2', 'value': 'option2'},
                    {'label': 'Option 3', 'value': 'option3'}
                ],
                value='option1',
                style={'fontSize': '14px', 'width': '200px'}  # Reduce the dropdown option font size and width
            ),
        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'marginBottom': 20}),  # Align dropdowns side by side
        
        html.Div([
            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    ],
                    'layout': {
                        'title': 'Bar chart example'
                    }
                },
                style={'display': 'inline-block', 'width': '45%', 'marginRight': '5%'}  # Reduce the width and add margin
            ),
            dcc.Graph(
                id='example-graph2',
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [2, 5, 1], 'type': 'line', 'name': 'Line'},
                    ],
                    'layout': {
                        'title': 'Line chart example'
                    }
                },
                style={'display': 'inline-block', 'width': '45%'}  # Reduce the width
            )
        ], style={'marginTop': '30px'})  # Add some vertical spacing between the graphs
    ]
)

# Step 4: Define callbacks
@app.callback(
    Output('example-graph', 'figure'),  # Use the 'figure' property of the graph
    Input('dropdown', 'value')
)
def update_graph(value):
    if value == 'option1':
        return {
            'data': [{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'}],
            'layout': {'title': 'Bar chart example'}
        }
    elif value == 'option2':
        return {
            'data': [{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'NYC'}],
            'layout': {'title': 'Bar chart example'}
        }
    elif value == 'option3':
        return {
            'data': [{'x': [1, 2, 3], 'y': [3, 2, 1], 'type': 'bar', 'name': 'LA'}],
            'layout': {'title': 'Bar chart example'}
        }
    else:
        return {
            'data': [],
            'layout': {'title': 'No Data'}
        }

# Step 5: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
