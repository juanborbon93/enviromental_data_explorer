import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from ..app import app

def modal(message:str,message_type:str="Error"):
    modal = dbc.Modal(
            [
                dbc.ModalHeader(message_type),
                dbc.ModalBody(message),
                dbc.ModalFooter(
                    dbc.Button("Close", id="modal-close", className="ml-auto")
                ),
            ],
            id="message-modal",
        )

@app.callback(
    Output("message-modal", "is_open"),
    [Input("modal-close", "n_clicks")],
    [State("message-modal", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open