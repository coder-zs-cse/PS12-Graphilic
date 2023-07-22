import dash
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output



x = []
UserCount = []
OverallProfit = []



app = Dash(__name__)




# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
reviews_data = pd.read_csv('../../Data/reviews1_data.csv')
file_path = '../../Data/reviews1_data.csv'
df = pd.read_csv(file_path)

print(">",df[:5])
#filter rows with month 5 and year 2002 and group Books
filtered_df = df[(df['month'] == 6) & (df['year']== 2000) & (df['group'] == 'Book')]
filtered_df = filtered_df.sort_values(by=['day'])
#group by day and get average profit and total count of reviews

filtered_df1 = filtered_df.groupby('day')['profit'].count().rename('Count')
filtered_df2 = filtered_df.groupby('day')['profit'].mean().rename('Profit')

filtered_df = filtered_df.reset_index()
filtered_df1 = filtered_df1.reset_index()
filtered_df2 = filtered_df2.reset_index()
# filtered_df = df[(df['month'] == 12 & (df['year']== 2000))]

# print(filtered_df[:40])


# print("<")
# print(filtered_df[:5])
# print()
# print(filtered_df1[:5])
# print()
# print(filtered_df2[:5])

#store day in x
x = filtered_df1['day'].tolist()
#store count of reviews in UserCount
UserCount = filtered_df1['Count'].tolist()
#store average profit in OverallProfit
OverallProfit = filtered_df2['Profit'].tolist()
print(x)
print(UserCount)
print(OverallProfit)


# Get unique days and years from the data
available_days = filtered_df1['day']
#sort available days
# sorted(available_days)

available_years = df['year'].unique()
available_cat = df['group'].unique()
print(">",available_cat)
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    html.Div([
        dcc.Dropdown(id="slct_day",
                     options=[{"label": str(day), "value": day} for day in available_days],
                     multi=False,
                     value=available_days[0],
                     style={'width': "100%",'margin':'0px 30px 0px 30px'}
                     ),
        dcc.Dropdown(id="slct_month",
                     options=[{"label": str(cat), "value": cat} for cat in available_cat],
                     multi=False,
                     value=12,
                     style={'width': "100%",'margin':'0px 30px 0px 30px'}
                     ),
        dcc.Dropdown(id="slct_year",
                     options=[{"label": str(year), "value": year} for year in available_years],
                     multi=False,
                     value=1999,
                     style={'width': "100%",'margin':'0px 30px 0px 30px'}
                     ),
    ], style={'display': 'flex','width': '30%'}),

    html.Div(id='output_container', children=[]),
    html.Br(),
    html.Div(id='heatmap-graph'),
    dcc.Graph(id='my_another_chart'),  # Replace 'my_another_chart' with your desired ID for the new chart

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output('my_another_chart', 'options'),
    [Input('slct_day', 'value'),
     Input('slct_month', 'value'),
     Input('slct_year', 'value')]
)
def update_month_dropdown(selected_day, selected_year):
    dff = df[(df['day'] == selected_day) & (df['year'] == selected_year)]
    available_months = dff['month'].unique() if 'month' in dff else []
    month_options = [{'label': str(month), 'value': month} for month in available_months]
    return month_options


def update_graph(selected_day, selected_month, selected_year):
    container = f"The day, month, and year chosen by the user are: {selected_day}, {selected_month}, {selected_year}"

    dff = df[(df["day"] == selected_day) & (df["month"] == selected_month) & (df["year"] == selected_year)]

    # Plotly Express bar chart
    fig = px.bar(
        data_frame=dff,
        x=x,  # Replace 'day' with the appropriate column from your data for the X-axis
        y=UserCount,  # Replace 'profit' with the appropriate column for the Y-axis
        labels={'day': 'Day', 'profit': 'Profit'},
        template='plotly_dark'
    )

    return fig

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


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

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
