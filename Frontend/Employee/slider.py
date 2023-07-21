import dash
from dash import dcc, html, Input, Output
import requests

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Slider(
        id='slider-component',
        min=0,
        max=100,
        step=1,
        value=50
    ),
    html.Div(id='output-container')
])

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

if __name__ == '__main__':
    app.run_server(debug=True)
