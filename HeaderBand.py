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



class HeaderBand():

    def __init__(self, app, header='Scanner : ', qlog = None):

        self.configLogger(qlog)
        self.model = Model()
        self.app = app
        self.update = False

        @self.app.callback(Output("out1", 'children'),
                           Input("bt1", 'n_clicks'),)
        def display_value(value):
            if self.update:
                return 'You have selectect "{}"'.format(value)
            else:
                return dash.no_update


    def getLayout(self):
        headerband = html.Div(
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.I(id="bt1", className="fas fa-arrow-circle-right hb-button"), width="auto"),
                    dbc.Col(html.I(id="notif", className="fas fa-bell hb-button"), width="auto"),
                    dbc.Col(html.Div(self.model.currentpage, id="out1"
                                     , style = {"margin-top": "5px"}
                                     )),
                    # dbc.Col(html.I(id="user", className="fas fa-user hb-button"), width="auto"),
                    dbc.Col(dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("Root", href='/'),
                            dbc.DropdownMenuItem("Page 1", href='/page-1'),
                            dbc.DropdownMenuItem("Page 2", href='/page-2'),
                        ],
                        nav=True,
                        in_navbar=True,
                        # className="hb-button",
                        style = {"color": "white"},
                        label= "♻"
                    ), width="auto"),
                ], )
            ], fluid=True),

            className="headerband g-0",
            id="headerband",
        )

        self.update = False
        return headerband




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
    version: str = 'V-1.0.3'
    headertag : int = 0
    currentpage : str = 'root'
