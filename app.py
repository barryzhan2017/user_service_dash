import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
user_service_url = "http://0.0.0.0:80"

application = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = application.server

