import dash
import dash
from flask import Flask
import dash_bootstrap_components as dbc

server = Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'assets/style.css'],server=server)
app.scripts.config.serve_locally = True
app.config['suppress_callback_exceptions']=True

