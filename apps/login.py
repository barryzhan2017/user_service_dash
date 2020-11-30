import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
import json
import dash


login_endpoint = "/api/login"
catalog_page = "http://signaldevv20-env.eba-2ibxmk54.us-east-2.elasticbeanstalk.com/"
domain = ".us-east-2.elasticbeanstalk.com"

layout = html.Div([
    html.H1("Dash Signal Login Page"),
    html.Div(["Username: ",
              dcc.Input(id='username', placeholder='username', type='text')]),
    html.Br(),
    html.Div(["Password: ",
              dcc.Input(id='password', placeholder='password', type='password')]),
    html.Br(),
    html.Button(id='submit', children="Sign in", n_clicks=0),
    html.Br(),
    html.Div(id='error_login', style={'color': 'red'}),
    dcc.Store(id='session', storage_type='session')
])


@app.application.callback(
    [Output("error_login", "children"),
     Output("session", "data")],
    [Input("submit", "n_clicks")],
    [State("username", "value"),
     State("password", "value")]
)
def login(click, username, password):
    if click != 0:
        data = dict()
        if username is None or password is None:
            return "Username and password are required"
        header = {"Content-Type": "application/json"}
        payload = {"username": username, "password": password}
        res = requests.post(app.user_service_url + login_endpoint, headers=header, data=json.dumps(payload))
        res_json = res.json()
        if res.status_code == 200:
            data["token"] = res_json["token"]
            # domain – if you want to set a cross-domain cookie.
            # For example, domain=".example.com" will set a cookie
            # that is readable by the domain www.example.com, foo.example.com etc.
            # Otherwise, a cookie will only be readable by the domain that set it.
            # httponly to prevent xss attack and secure to encode the token while transmission
            dash.callback_context.response.set_cookie("token", data["token"], httponly=True,
                                                      secure=True, domain=domain)
            print(data["token"])
            #return dcc.Location(href=catalog_page, id="any"), " "
        return res_json["message"], data
    return "", {}
