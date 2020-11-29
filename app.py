import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
user_service_url = "http://0.0.0.0:80"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJyb2xlIjoic3VwcG9ydCIsImV4cCI6MTYwNjYxMTEyMX0.dDhwK_ObkGwPSr43lvVG_HDgjI7tTT8Y0TdEAz4HN8E"

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server
