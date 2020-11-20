import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
import json


login_endpoint = "/login"

layout = html.Div([
    html.H6("Dash Signal"),
    html.Div(["Username: ",
              dcc.Input(id='username', placeholder='username', type='text')]),
    html.Br(),
    html.Div(["Password: ",
              dcc.Input(id='password', placeholder='password', type='password')]),
    html.Br(),
    html.Button(id='submit', children="Sign in", n_clicks=0),
    html.Br(),
    html.Div(id='error1', style={'color': 'red'})
])


@app.app.callback(
    Output('error1', 'children'),
    [Input('submit', 'n_clicks')],
    [State('username', 'value'),
     State('password', 'value')]
)
def login(click, username, password):
    if click != 0:
        if username is None or password is None:
            return "Username and password are required"
        header = {"Content-Type": "application/json"}
        payload = {"username": username, "password": password}
        res = requests.post(app.user_service_url + login_endpoint, headers=header, data=json.dumps(payload))
        res_json = res.json()
        if res.status_code == 200:
            app.token = res_json["token"]
        return res_json["message"]
