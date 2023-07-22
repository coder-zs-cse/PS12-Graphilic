import dash 
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

import load_options

file_path = '../../Data/reviews1_data.csv'
reviews_data = pd.read_csv(file_path)
reviews_data = reviews_data.sort_values(by=['day'])

dayOptions, yearOptions, categoryOptions = load_options.load_options(reviews_data)












import heatmap 






app = Dash(__name__)

app.layout = html.Div([
    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),
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
    html.Div([

        html.Div([


            
            dcc.Graph(id='my_another_chart'),  # Replace 'my_another_chart' with your desired ID for the new chart


        ],className='bargraph',style={'width':'50%','height':'500px','margin':'30px','color':'white','background-color':'#1E1E1E'}),
        html.Div([],className='linegraph',style={'width':'50%','height':'500px','margin':'30px','color':'white','background-color':'#1B1B1B'}),

    ],style={'display':'flex'}),

    html.Div([],className='slider',style={'width':'90%','height':'50px','margin':'0px auto','color':'white','background-color':'#4E4E4E'}),

    html.Div([

        html.Div([],className='heatmap',style={'width':'50%','height':'500px','margin':'30px','color':'white','background-color':'#1E1E1E'}),
        html.Div([],className='piechart',style={'width':'50%','height':'500px','margin':'30px','color':'white','background-color':'#1B1B1B'}),

    ],style={'display':'flex'}),

])

if __name__ == '__main__':
    app.run_server(debug=True)