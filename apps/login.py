import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
import json
import dash
from cryptography.fernet import Fernet
import re
from smartystreets_python_sdk import StaticCredentials, ClientBuilder
from smartystreets_python_sdk.us_autocomplete import Lookup as AutocompleteLookup

regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
registration_endpoint = "/api/registration"
g_login_endpoint = "/api/g_login"
login_endpoint = "/api/login"
catalog_page = app.catalog_url
suggestions = []

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
    html.Button(id='OAuth2', children="Sign in by Google", n_clicks=0),
    html.Br(),
    html.Div(id="OAuth2_result"),
    html.Div(id='error_login', style={'color': 'red'}),
    html.Br(),
    html.H5("Registration"),
    dcc.Input(id="username_reg", type="text", placeholder="username"),
    dcc.Input(id="password_reg", type="password", placeholder="password"),
    dcc.Input(id="email_reg", type="text", placeholder="email"),
    dcc.Input(id="phone_reg", type="text", placeholder="phone"),
    dcc.Input(id="slack_id_reg", type="text", placeholder="slack_id"),
    dcc.Input(id="address_reg", type="text", placeholder="[street, city state]", list='suggest_address'),
    dcc.Dropdown(id="role_reg",
                 placeholder="role",
                 options=[
                     {"label": "support", "value": "support"},
                     {"label": "ip", "value": "ip"},
                 ],
                 style={"width": "30%"}
                 ),
    html.Button(id="register", children="Register", n_clicks=0),
    html.Div(id="error_register", style={"color": "red"}),
    html.Datalist(
        id='suggest_address',
        children=[html.Option(value=word) for word in suggestions])
])


@app.app.callback(
    Output("error_login", "children"),
    [Input("submit", "n_clicks")],
    [State("username", "value"),
     State("password", "value")]
)
def login(click, username, password):
    if click != 0:
        f = Fernet(app.secret)
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
            dash.callback_context.response.set_cookie("token", data["token"], httponly=True)
            # False configuration, cannot save token: httponly=True,secure=True, domain=domain
            # Redirect to catalog page
            return dcc.Location(
                href=catalog_page + "?token=" + f.encrypt(data["token"].encode("utf-8")).decode("utf-8"), id="any"), " "
        return res_json["message"]
    return ""


# Add users based on input value, all the fields are required.
@app.app.callback(
    Output("error_register", "children"),
    [Input("register", "n_clicks")],
    [State("username_reg", "value"),
     State("password_reg", "value"),
     State("email_reg", "value"),
     State("phone_reg", "value"),
     State("slack_id_reg", "value"),
     State("role_reg", "value"),
     State("address_reg", "value")]
)
def add_users(click, username, password, email, phone, slack_id, role, address):
    if click != 0:
        if not username or not password or not email or not phone or not slack_id or not role:
            return "All fields are required"
        if not re.search(regex, email):
            return "Email format is incorrect"
        header = {"Content-Type": "application/json"}
        # Inactive status for a new user
        payload = {"username": username, "password": password, "email": email, "phone": phone, "slack_id": slack_id,
                   "role": role, "address": address, "status": "inactive"}
        res = requests.post(app.user_service_url + registration_endpoint, headers=header, data=json.dumps(payload))
        res_json = res.json()
        return res_json["message"]
    return ""


# Autocomplete the address fields by sending request to smartstreet
@app.app.callback(
    Output("suggest_address", "children"),
    [Input("address_reg", "value")]
)
def update_address(address):
    credentials = StaticCredentials(app.auth_id, app.auth_token)
    client = ClientBuilder(credentials).build_us_autocomplete_api_client()
    if address:
        lookup = AutocompleteLookup(address)
        client.send(lookup)
        for suggestion in lookup.result:
            print(suggestion.text)
        return [html.Option(value=suggestion.text) for suggestion in lookup.result]
    return []


# Go to server side api to get enable goolge verification
@app.app.callback(
    Output("OAuth2_result", "children"),
    [Input("OAuth2", "n_clicks")]
)
def oauth2_login(click):
    if click != 0:
        return dcc.Location(
            href=app.user_service_url + g_login_endpoint, id="any")
    return ""
