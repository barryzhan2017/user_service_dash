import app
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import requests
import dash_table
import json
import flask

users_path = "/api/users"
user_fields = ["user_id", "username", "password", "email", "phone",
               "slack_id", "role", "created_date"]
editable_dic = {"user_id": False, "username": False, "password": True, "email": True, "phone": True,
                "slack_id": True, "role": True, "created_date": False}

layout = html.Div([
    html.H1("Dash Signal User Management"),
    html.H5("Add a user"),
    dcc.Input(id="username", type="text", placeholder="username"),
    dcc.Input(id="password", type="password", placeholder="password"),
    dcc.Input(id="email", type="text", placeholder="email"),
    dcc.Input(id="phone", type="text", placeholder="phone"),
    dcc.Input(id="slack_id", type="text", placeholder="slack_id"),
    dcc.Dropdown(id="role",
                 placeholder="role",
                 options=[
                     {"label": "support", "value": "support"},
                     {"label": "ip", "value": "ip"},
                 ],
                 style={"width": "30%"}
                 ),
    html.Button(id="add", children="Add", n_clicks=0),
    html.Div(id="error_add", style={"color": "red"}),
    html.H5("Search users"),
    html.Div([dcc.Dropdown(
        id="criteria",
        options=[
            {"label": "none", "value": "none"},
            {"label": "user_id", "value": "user_id"},
            {"label": "username", "value": "username"},
        ],
        value="user_id",
        style={"width": "30%"}
    )]),
    html.Div([dcc.Input(id="search_input", type="text", placeholder="value")]),
    html.Button(id="search", children="Search", n_clicks=0),
    html.Br(),
    html.Div(id="error_search", style={"color": "red"}),
    dash_table.DataTable(
        id="user_info",
    ),
    html.Br(),
    html.Div([html.Button(id="delete", children="Delete", n_clicks=0),
              html.Button(id="update", children="Update", n_clicks=0)], id="operation", style={"display": "none"}),
    html.Div(id="error_update", style={"color": "red"}),
    html.Div(id="error_delete", style={"color": "red"}),
])


# Show users information based on criteria, if searching for a specific user, we can update and delete it.
@app.app.callback(
    [Output("user_info", "data"),
     Output("user_info", "columns"),
     Output("error_search", "children"),
     Output("operation", "style")],
    [Input("search", "n_clicks")],
    [State("criteria", "value"),
     State("search_input", "value")]
)
def show_users(click, criteria, search_input):
    if click != 0:
        token = flask.request.cookies["token"]
        header = {"Authorization": token}
        # Send to /api/users/<id> to get user by user id
        if criteria == "user_id":
            if not search_input:
                return [], [], "Value is empty", {"display": "none"}
            res = requests.get(app.user_service_url + users_path + "/" + search_input, headers=header)
        # Send to /api/users?username=xxx to get users by username
        elif criteria == "username":
            if not search_input:
                return [], [], "Value is empty", {"display": "none"}
            res = requests.get(app.user_service_url + users_path + "?username=" + search_input, headers=header)
        # Send to /api/users to get all users
        else:
            res = requests.get(app.user_service_url + users_path, headers=header)
        res_json = res.json()
        # Remove all password value
        for data in res_json["data"]:
            data["password"] = ""
        # If we query based on username or user id, we should be able to update and delete that user
        if res.status_code == 200 and (criteria == "user_id" or criteria == "username" and len(res_json["data"]) == 1):
            return res_json["data"], [{"id": p, "name": p, "editable": editable_dic[p]} for p in user_fields], "", {
                "display": "block"}
        elif res.status_code == 200:
            return res_json["data"], [{"id": p, "name": p, "editable": editable_dic[p]} for p in user_fields], "", {
                "display": "none"}
        return [], [], res_json["message"], {"display": "none"}
    return [], [], "", {"display": "none"}


# Add users based on input value, all the fields are required.
@app.app.callback(
    Output("error_add", "children"),
    [Input("add", "n_clicks")],
    [State("username", "value"),
     State("password", "value"),
     State("email", "value"),
     State("phone", "value"),
     State("slack_id", "value"),
     State("role", "value")]
)
def add_users(click, username, password, email, phone, slack_id, role):
    if click != 0:
        if not username or not password or not email or not phone or not slack_id or not role:
            return "All fields are required"
        token = flask.request.cookies["token"]
        header = {"Authorization": token, "Content-Type": "application/json"}
        payload = {"username": username, "password": password, "email": email, "phone": phone, "slack_id": slack_id,
                   "role": role}
        print(payload)
        res = requests.post(app.user_service_url + users_path, headers=header, data=json.dumps(payload))
        res_json = res.json()
        return res_json["message"]
    return ""


# Update users based on its editable field value, update not none or empty value
@app.app.callback(
    Output("error_update", "children"),
    [Input("update", "n_clicks")],
    [State("user_info", "data")]
)
def update_users(click, data):
    if click != 0:
        user = data[0]
        payload = dict()
        user_id = 0
        for field in user_fields:
            if field in user and user[field]:
                # Get id and not update it
                if field == "user_id":
                    user_id = user[field]
                elif field != "created_date":
                    payload[field] = user[field]
        token = flask.request.cookies["token"]
        header = {"Authorization": token, "Content-Type": "application/json"}
        res = requests.put(app.user_service_url + users_path + "/" + str(user_id), headers=header,
                           data=json.dumps(payload))
        res_json = res.json()
        return res_json["message"]
    return ""


# Delete users based on the id
@app.app.callback(
    Output("error_delete", "children"),
    [Input("delete", "n_clicks")],
    [State("user_info", "data")]
)
def delete_users(click, data):
    if click != 0:
        user = data[0]
        user_id = user["user_id"]
        token = flask.request.cookies["token"]
        header = {"Authorization": token}
        res = requests.delete(app.user_service_url + users_path + "/" + str(user_id), headers=header)
        res_json = res.json()
        return res_json["message"]
    return ""
