import dash
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
user_service_url = "http://18.216.73.6"

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
page_url = "http://user-service-dash.eba-y82cxuwr.us-east-2.elasticbeanstalk.com/"
secret = os.environ['TOKEN_SECRET'].encode('utf-8')
