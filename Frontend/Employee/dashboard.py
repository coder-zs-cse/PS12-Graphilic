import dash 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime as dt

from dash import Dash, dcc, html, Input, Output

import load_options

file_path = '../../Data/reviews1_data.csv'
reviews_data = pd.read_csv(file_path)
reviews_data = reviews_data.sort_values(by=['day'])

dayOptions, monthOptions, yearOptions, categoryOptions = load_options.load_options(reviews_data)

profit_data = reviews_data
profit_data['datetime'] = pd.to_datetime(profit_data[['year', 'month', 'day']])










import heatmap 






app = Dash(__name__)

app.layout = html.Div([


    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),




    html.Div([

        html.Div([


            html.Div([
                dcc.Dropdown(id="slct_day",
                            options=[{"label": str(day), "value": day} for day in dayOptions],
                            multi=False,
                            value= dayOptions[0],
                            style={'width': "100%",'margin':'0px 30px 0px 30px'}
                            ),
                dcc.Dropdown(id="slct_year",
                            options=[{"label": str(year), "value": year} for year in yearOptions],
                            multi=False,
                            value=yearOptions[0],
                            style={'width': "100%",'margin':'0px 30px 0px 30px'}
                            ),
                dcc.Dropdown(id="slct_group",
                            options=[{"label": str(cat), "value": cat} for cat in categoryOptions],
                            multi=False,
                            value=categoryOptions[0],
                            style={'width': "100%",'margin':'0px 30px 0px 30px'}
                            ),
            ], style={'display': 'flex','width': '30%','margin':'20px'}),
            
            dcc.Graph(id='bar-chart'),  # Replace 'my_another_chart' with your desired ID for the new chart


        ],className='bargraph',style={'width':'50%','height':'500px','margin':'30px'}),
        html.Div([

            html.H1("Company Profit over datetime", style={'text-align': 'center'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=dt(2000, 6, 1),
                end_date=dt(2000, 6, 30),
                display_format='YYYY-MM-DD',
                style={'margin': 'auto'}
            ),
            dcc.Graph(id='profit-graph')


        ],className='linegraph',style={'width':'50%','height':'500px','margin':'30px'}),

    ],style={'display':'flex'}),



    html.Div([
        dcc.Slider(
            id='slider-component',
            min=0,
            max=100,
            step=5,
            value=50,
            
        ),
        html.Div(id='output-container')
    ],className='slider',style={'width':'50%','height':'50px','margin':'20px auto'}),



    html.Div([

        html.Div([
            html.Div([

                dcc.Dropdown(
                    id='group-dropdown',
                    options=[{'label': group, 'value': group} for group in reviews_data['group'].unique()],
                    value='Book',
                    style={'width': '50%', 'margin': 'auto'}
                ),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in sorted(reviews_data['month'].unique().tolist())],
                    value=6,
                    style={'width': '50%', 'margin': 'auto'}
                ),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': year, 'value': year} for year in reviews_data['year'].unique()],
                    value=2000,
                    style={'width': '50%', 'margin': 'auto'}
                ),
            ],style={'display':'flex','margin':'40px'}),

            dcc.Graph(id='heatmap-graph'),
        ],className='heatmap',style={'width':'50%'}),


        html.Div([

            # html.H1("User Interactions per Category", style={'text-align': 'center'}),
            
            dcc.Graph(id='pie-chart')



        ],className='piechart',style={'width':'50%','height':'500px','margin':'110px'}),

    ],style={'display':'flex'}),

])

@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    [Input(component_id='slct_day', component_property='value'),
     Input(component_id='slct_group', component_property='value'),
     Input(component_id='slct_year', component_property='value')]
)
def update_another_graph(selected_day, selected_month, selected_year):
    container = f"The day, month, and year chosen by the user are: {selected_day}, {selected_month}, {selected_year}"
    df = reviews_data
    dff = df[(df["day"] == selected_day) & (df["group"] == selected_month) & (df["year"] == selected_year)]

    filtered_df = dff
    filtered_df = filtered_df.sort_values(by=['day'])
    #group by day and get average profit and total count of reviews

    filtered_df1 = filtered_df.groupby('day')['profit'].count().rename('Count')
    filtered_df2 = filtered_df.groupby('day')['profit'].mean().rename('Profit')

    filtered_df = filtered_df.reset_index()
    filtered_df1 = filtered_df1.reset_index()
    filtered_df2 = filtered_df2.reset_index()

    days = filtered_df1['day'].tolist()
    #store count of reviews in UserCount
    UserCount = filtered_df1['Count'].tolist()
    #store average profit in OverallProfit
    # OverallProfit = filtered_df2['Profit'].tolist()
    # Example: Create another Plotly Express chart for the second graph
    fig = px.scatter(
        data_frame=dff,
        x='day',  # Replace 'day' with the appropriate column from your data for the X-axis
        y=UserCount,  # Replace 'some_other_column' with the appropriate column for the Y-axis
        labels={'day': 'Day', 'some_other_column': 'Some Other Data'},
        template='plotly_dark'
    )

    return fig


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





@app.callback(
    Output('output-container', 'children'),
    Input('slider-component', 'value')
)
def update_output(value):
    # In this example, we'll simply return the value as the output.
    # You can perform any backend processing using the received value here.
    # Additionally, send the value to the backend using a POST request.
    url = 'http://localhost:5000/slider'  # Replace with your backend endpoint URL
    data = {'slider_value': value}
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return f'Slider Value: {value} (Successfully sent to backend)'
    else:
        return f'Slider Value: {value} (Failed to send to backend)'









@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('group-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_heatmap(selected_group, selected_month, selected_year):

    heatmap_data = reviews_data[(reviews_data['group'] == selected_group) & (reviews_data['year'] == selected_year)].groupby('month')['rating', 'helpful'].mean().reset_index()
    heatmap_data = heatmap_data.pivot(index='month', columns='rating', values='helpful')

    fig = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.index,
        y=heatmap_data.columns,
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