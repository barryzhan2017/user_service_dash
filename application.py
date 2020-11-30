import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import application
from apps import login, user_service


application.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@application.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return login.layout
    elif pathname == '/users':
        return user_service.layout
    else:
        return '404'

if __name__ == '__main__':
    application.run_server(debug=True, port=8080)