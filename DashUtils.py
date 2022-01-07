import logging

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask

logger = logging.getLogger(__name__)

class DashUtils():

    def __init__(self, qlog = None):

        self.configLogger(qlog)

    def configLogger(self, qlog):

        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


    #=========================================== STATIC METHODS =======================================================

    @staticmethod
    def buildSimpleNavBar():
        navbar = dbc.NavbarSimple(
            children=[
                # dbc.NavItem(dbc.NavLink("Page 1", href="#")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Root", href='/'),
                        dbc.DropdownMenuItem("Page 1", href='/page-1'),
                        dbc.DropdownMenuItem("Page 2", href='/page-2'),
                    ],
                    nav=True,
                    in_navbar=True,
                    className="fxf-session-header",
                    label="☎️" #+"Activities"
                ),
                dbc.Button(
                    "Click me", id="example-button", className="me-2", n_clicks=0
                ),
                html.Span(id="example-output", style={"verticalAlign": "middle"}),
            ],
            brand="Scanner 3",
            brand_href="#",
            color="blue",
            dark=True,
        )
        return navbar


    @staticmethod
    def buildHeaderBar(app):
        headerbar = html.Div(
            dbc.Container([
                    dbc.Row([
                        dbc.Col(html.Div("❱", id="bt1", className="hb-button"),width="auto"),
                        dbc.Col(html.Div("2", id="out1")),
                        dbc.Col(html.Div("3"), width="auto"),
                    ])
                ],
                fluid=True,
                # className="py-3",
            ),
            className="headerbar g-0",
        )

        @app.callback(Output("out1", 'children'),
                      Input("bt1", 'n_clicks'),)
        def display_value(value):
            # print('display_value')
            return 'You have selectect "{}"'.format(value)

        return headerbar
