import dash 
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output

import load_options

file_path = '../../Data/reviews1_data.csv'
reviews_data = pd.read_csv(file_path)
reviews_data = reviews_data.sort_values(by=['day'])

dayOptions, monthOptions, yearOptions, categoryOptions = load_options.load_options(reviews_data)












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
            
            dcc.Graph(id='my_another_chart'),  # Replace 'my_another_chart' with your desired ID for the new chart


        ],className='bargraph',style={'width':'50%','height':'500px','margin':'30px','color':'white','background-color':'#1E1E1E'}),
        html.Div([],className='linegraph',style={'width':'50%','height':'500px','margin':'30px','color':'white','background-color':'#1B1B1B'}),

    ],style={'display':'flex'}),



    html.Div([],className='slider',style={'width':'90%','height':'50px','margin':'0px auto','color':'white','background-color':'#4E4E4E'}),



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
            ],style={'display':'flex'}),

            dcc.Graph(id='heatmap-graph'),
        ],className='heatmap',style={'width':'50%'}),


        html.Div([

            # html.H1("User Interactions per Category", style={'text-align': 'center'}),
            
            dcc.Graph(id='pie-chart')



        ],className='piechart',style={'width':'50%','height':'500px','margin':'30px'}),

    ],style={'display':'flex'}),

])


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