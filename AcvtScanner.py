import logging
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask

from DashUtils import DashUtils

logger = logging.getLogger(__name__)

class AcvtScanner():

    def __init__(self, app, qlog = None):

        self.configLogger(qlog)

        self.layout_page = html.Div([
            html.H2('Page 1'),
            dcc.Input(id='input-1-state', type='text', value='Montreal'),
            dcc.Input(id='input-2-state', type='text', value='Canada'),
            html.Button(id='submit-button', n_clicks=0, children='Submit'),
            html.Div(id='output-state'),
        ])


        # Page 1 callbacks
        @app.callback(Output('output-state', 'children'),
                           Input('submit-button', 'n_clicks'),
                           State('input-1-state', 'value'),
                           State('input-2-state', 'value'))
        def update_output(n_clicks, input1, input2):
            return ('The Button has been pressed {} times,'
                    'Input 1 is "{}",'
                    'and Input 2 is "{}"').format(n_clicks, input1, input2)


    def getLayout(self):
        return self.layout_page


    def configLogger(self, qlog):

        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

