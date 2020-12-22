import dash
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
user_service_url = os.environ['USER_SERVICE_URL']
user_service_g_login_url = os.environ['USER_SERVICE_G_LOGIN_URL']
catalog_url = os.environ['CATALOG_URL']
user_service_dash_url = os.environ['USER_SERVICE_DASH_URL']
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
secret = os.environ['TOKEN_SECRET'].encode('utf-8')
auth_id = os.environ['SMARTY_AUTH_ID']
auth_token = os.environ['SMARTY_AUTH_TOKEN']
invalid_token_status_code = 401
