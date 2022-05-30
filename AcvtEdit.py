import json
import logging
from collections import namedtuple, OrderedDict

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

from flask import Flask

import numpy as np
import pandas as pd
from plotly.graph_objs.layout import Margin
from plotly.graph_objs.layout import Legend

from CCDScan import CCDScan



from DashUtils import DashUtils

logger = logging.getLogger(__name__)

class AcvtEdit():

    def __init__(self, app, config, qlog = None):

        self.configLogger(qlog)
        self.app = app

        self.layout_page = html.Div(children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.H3(children='BSW CCD Project Editor - Beta 1.0.2',style = {"color": "white"}), width="auto" ),
                ], style = {"background-color": "blue", "height" : "60px", "align-items" : "center", "margin-bottom": "15px"} ),
                # dbc.Row([
                #     dbc.Col(html.Div(children = self.getFileForm(),
                #             style = {"margin-left": "25px", "display": "flex", "column-gap" : "25px", "justify-content" : "left", "align-items" : "center"},
                #             id = 'scanrow')
                #     ,width="auto"),
                # ], ),
                # dbc.Row([
                #     dcc.Graph(
                #         id='scangraph',
                #         figure=fig,
                #     )
                # ], ),
                dbc.Row([
                    html.Div([
                        html.Div(id='dummy2', style = {"display": "none"}),
                        html.P('.', id='testlabel', style = {"display": "inline-block"}),
                    ] ,
                    id='bottom_row',
                    style = {"margin-left": "25px", "display": "flex", "column-gap" : "25px", "justify-content" : "left", "align-items" : "center"})

                ], ),
            ], fluid=True),
            self.installTimer(),
        ])


        # @self.app.callback( Output('dummy2', 'hidden'),
        #                     Input('scantimer', 'n_intervals'),
        #                 )
        # def update_page(n_intervals):
        #     return dash.no_update



    # End of init section



    def newCurrentScan (self, file, chip, intnum, scan):
        intvals, default = scan.getIntegrations(0)
        chipvals = [{'label': "0", 'value': "0"}]
        self.currentscan = [file, chip, intnum, chipvals, intvals, True, True, True, False]


    def updateCurrentScan(self, file=None, chip=None, intnum=None, scan=None):
            if file is not None: self.currentscan[0] = file
            if chip is not None: self.currentscan[1] = chip
            if intnum is not None: self.currentscan[2] = intnum
            if scan is not None:
                intvals, default = scan.getIntegrations(0)
                chipvals = [{'label': "0", 'value': "0"}]




    def installTimer(self, id_='scantimer', interval_=1000 ):
        interv =  dcc.Interval(
            id=id_,
            interval=interval_, # in milliseconds
            n_intervals=0
        )
        return interv


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

