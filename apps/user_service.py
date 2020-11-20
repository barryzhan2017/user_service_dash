import app
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import dash_table

get_all_users = '/users'
user_fields = ["user_id", "username", "password", "email", "phone",
               "slack_id", "role", "created_date"]

layout = html.Div([
    html.H6("Dash Signal User Management"),
    html.Button(id='show', children="Show All", n_clicks=0),
    html.Br(),
    dash_table.DataTable(
        id='user_info',
        editable=True
    ),
    html.Br(),
    html.Div(id='error2', style={'color': 'red'})
])


@app.app.callback(
    [Output('user_info', 'data'),
     Output('user_info', 'columns'),
     Output('error2', 'children')],
    [Input('show', 'n_clicks')]
)
def show_all(click):
    if click != 0:
        header = {"Authorization": app.token}
        res = requests.get(app.user_service_url + get_all_users, headers=header)
        res_json = res.json()
        if res.status_code == 200:
            return res_json['data'], [{'id': p, 'name': p} for p in user_fields], ""
        return [], [], res_json["message"]
    return [], [], ""
