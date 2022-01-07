import logging
from dataclasses import dataclass, field, fields
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask

from DashUtils import DashUtils
import DashServer as ds

logger = logging.getLogger(__name__)



class NavBand():

    def __init__(self, app, header='Scanner : ', qlog = None):

        self.configLogger(qlog)
        self.model = Model()
        self.app = app
        self.update = False

        @self.app.callback(Output('url', 'pathname'),
                           Input("nb_home", 'n_clicks'),)
        def call_home(value):
            self.model.currentnav = "/"
            self.update = True
            return self.model.currentnav


    def getLayout(self):
        navband = html.Div(
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.I(id="nb_previous", className="fas fa-chevron-left hb-button"), width="auto"),
                    dbc.Col(html.I(id="nb_home", className="fas fa-circle-notch hb-button"), width="auto"),
                    dbc.Col(html.I(id="nb_hist", className="fas fa-share-square hb-button"), width="auto"),
                ], justify = "center")
            ], fluid=True),

            className="navband g-0",
            id="navband",
        )

        self.model.currentnav = 'nonav'
        self.update = False
        return navband


    def configLogger(self, qlog):
        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


@dataclass
class Model:

    currentnav : str = 'nonav'
