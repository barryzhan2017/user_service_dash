import dash
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
user_service_url = "http://user-service.eba-txbhbpef.us-east-2.elasticbeanstalk.com/"
catalog_url = "http://signaldevv20-env.eba-2ibxmk54.us-east-2.elasticbeanstalk.com/"
user_service_dash_url = "http://user-service-dash.eba-y82cxuwr.us-east-2.elasticbeanstalk.com/"
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
secret = os.environ['TOKEN_SECRET'].encode('utf-8')
