import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
user_service_url = "http://18.216.73.6"

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)


