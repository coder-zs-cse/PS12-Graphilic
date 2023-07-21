import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


x = []
UserCount = []
OverallProfit = []



app = Dash(__name__)




# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
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
x = filtered_df['day']
#store count of reviews in UserCount
UserCount = filtered_df1['Count'].tolist()
#store average profit in OverallProfit
OverallProfit = filtered_df2['Profit'].tolist()


# Get unique days and years from the data
available_days = filtered_df1['day']
#sort available days
# sorted(available_days)

available_years = df['year']

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    html.Div([
        dcc.Dropdown(id="slct_day",
                     options=[{"label": str(day), "value": day} for day in available_days],
                     multi=False,
                     value=available_days[0],
                     style={'width': "100%"}
                     ),
        dcc.Dropdown(id="slct_month",
                     multi=False,
                     style={'width': "100%"}
                     ),
        dcc.Dropdown(id="slct_year",
                     options=[{"label": str(year), "value": year} for year in available_years],
                     multi=False,
                     value=available_years[0],
                     style={'width': "100%"}
                     ),
    ], style={'display': 'inline-block', 'width': '30%'}),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_profit_chart'),  # Bar chart for profit

    # Add another graph vertically beside the first graph
    dcc.Graph(id='my_another_chart'),  # Replace 'my_another_chart' with your desired ID for the new chart

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output('slct_month', 'options'),
    [Input('slct_day', 'value'),
     Input('slct_year', 'value')]
)
def update_month_dropdown(selected_day, selected_year):
    dff = df[(df['day'] == selected_day) & (df['year'] == selected_year)]
    available_months = dff['month'].unique() if 'month' in dff else []
    month_options = [{'label': str(month), 'value': month} for month in available_months]
    return month_options


@app.callback(
    Output(component_id='my_profit_chart', component_property='figure'),
    [Input(component_id='slct_day', component_property='value'),
     Input(component_id='slct_month', component_property='value'),
     Input(component_id='slct_year', component_property='value')]
)
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


# ------------------------------------------------------------------------------
# Add callback for the second graph (replace 'my_another_chart' with the actual ID of the new graph)
@app.callback(
    Output(component_id='my_another_chart', component_property='figure'),
    [Input(component_id='slct_day', component_property='value'),
     Input(component_id='slct_month', component_property='value'),
     Input(component_id='slct_year', component_property='value')]
)
def update_another_graph(selected_day, selected_month, selected_year):
    container = f"The day, month, and year chosen by the user are: {selected_day}, {selected_month}, {selected_year}"

    dff = df[(df["day"] == selected_day) & (df["month"] == selected_month) & (df["year"] == selected_year)]

    # Example: Create another Plotly Express chart for the second graph
    fig = px.scatter(
        data_frame=dff,
        x='day',  # Replace 'day' with the appropriate column from your data for the X-axis
        y='some_other_column',  # Replace 'some_other_column' with the appropriate column for the Y-axis
        labels={'day': 'Day', 'some_other_column': 'Some Other Data'},
        template='plotly_dark'
    )

    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
