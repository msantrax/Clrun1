import logging

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask

from DashUtils import DashUtils
from HeaderBand import HeaderBand
from NavBand import NavBand
from AcvtScanner import AcvtScanner
from AcvtEdit import AcvtEdit
from AcvtLand import AcvtLand

import numpy as np
import pandas as pd
from CCDScan import CCDScan


logger = logging.getLogger(__name__)

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'}
    # ,{
    #     'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
    #     'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
    #     'crossorigin': 'anonymous'
    # }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        # 'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        # 'crossorigin': 'anonymous'
    }
]



class DashServer():

    def __init__(self, qlog = None):
        # super().__init__()
        # self._transport = None
        # self.runsm :RunSM

        self.server_config = {
            'scanpath' : '/Bascon/Bruker/Sandbox/Reverse1/',
            'lastloaded' : ['RE12_1000_221:0:6666', 'RE12_1075_221:0:6666', 'RE12_1075_221:0:10000'],

        }


        self.server = Flask(__name__)
        self.app = dash.Dash(__name__, server = self.server
                             ,external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
                             # ,external_scripts = external_scripts
                             # ,routes_pathname_prefix = '/dash/'
                             )
        # self.app.config.suppress_callback_exceptions = True

        self.headerband = HeaderBand(self.app)
        self.navband = NavBand(self.app)
        self.acvtscanner = AcvtScanner(self.app)
        self.acvtedit = AcvtEdit(app=self.app, config=self.server_config)
        self.acvtland = AcvtLand(self.app)

        self.url_bar_and_content_div = html.Div([
            dcc.Location(id='url', refresh=False),
                self.headerband.getLayout(),
                html.Div(id='page-content'),
                self.navband.getLayout(),

            self.installTimer(),

            html.Div(id="dummy-nav", style={"display":"none"})

        ])

        # index layout
        self.app.layout = self.url_bar_and_content_div

        # "complete" layout
        self.app.validation_layout = html.Div([
            self.url_bar_and_content_div,
            self.acvtscanner.getLayout(),
            self.acvtedit.getLayout(),
            self.acvtland.getLayout(),
        ])

        DashServer.currentpage = ""
        DashServer.currentlayout = self.acvtland.getLayout()

        DashServer.refreshpage = False

        def updatepage():
            DashServer.currentpage=''

        # Index callbacks
        @self.app.callback( Output('timer', 'interval'),
                            [ Input('url', 'pathname'),
                              # Input('dummy-nav', 'children')
                            ]
                        )
        def update_page(pathname):
            if DashServer.currentpage != pathname :
                DashServer.currentpage = pathname
                if pathname == "/page-1":
                    DashServer.currentlayout = self.acvtscanner.getLayout()
                elif pathname == "/page-2":
                    DashServer.currentlayout = self.acvtedit.getLayout()
                else:
                    DashServer.currentlayout = self.acvtland.getLayout()
                self.headerband.model.currentpage = pathname
                self.headerband.update = True
                DashServer.refreshpage = True
            # elif nav != 'nonav':
            #     DashServer.currentlayout = self.acvtland.getLayout()
            #     self.headerband.model.currentpage = nav
            #     self.headerband.update = True
            #     DashServer.refreshpage = True
            else:
                DashServer.refreshpage = False
            return 1000

        @self.app.callback( Output('page-content', 'children'),
                            Output('headerband', 'children'),
                            # Output('navband', 'children'),
                            [
                                Input('timer', 'n_intervals'),
                                # Input('dummy-nav', 'children'),
                            ])
        def display_page(n_intervals):
            updates = [dash.no_update, dash.no_update]
            if DashServer.refreshpage :
                logger.info('Loading page on {}'.format(DashServer.currentpage))
                DashServer.refreshpage = False
                updates[0] = DashServer.currentlayout
            if self.headerband.update :
                updates[1] = self.headerband.getLayout()
            # if self.headerband.update :
            #     updates[2] = self.navband.getLayout()
            # logger.info('Timer = {} - dummynav = {}'.format(n_intervals))

            return updates


        @self.server.route('/user/<username>')
        def	show_user_profile(username):
            # self.app.update_output_div(username)
            # if username == 'opus':
            #     return self.acvtscanner.getLayout()
            # elif username == '2':
            #     return self.acvtedit.getLayout()
            # else :
                return	'Now adjusting dash to	%s'	%	username

        # self.configLogger(qlog)

    # end init ?


    def installTimer(self, id_='timer', interval_=1000 ):
        interv =  dcc.Interval(
            id=id_,
            interval=interval_, # in milliseconds
            n_intervals=0
        )
        return interv


    #========================================== SERVICE POINTS ========================================================
    def rundash(self):
        self.app.run_server(debug=True, threaded=True)

    def getServer(self):
        return self.app.server

    # def setRunSM(self, rsm):
    #     self.runsm = rsm

    def configLogger(self, qlog):

        logger.setLevel(logging.DEBUG)
        if qlog is None:
            ch = logging.StreamHandler()
        else:
            ch = logging.StreamHandler(qlog)

        formatter = logging.Formatter('%(msecs).2f - %(levelno)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


    #========================================== STATES ========================================================

    # DASH:DASHINIT
    def sm_init(self, payload):
        logger.debug("Dash Server is initializing")

    # DASH:DASHCONFIG
    def sm_config(self, payload):
        logger.debug("Configuring Dash Server")













    # Tie a callback to the interval
    # @self.app.callback(
    #     Output('tick_out', 'children'),
    #     [Input('interval-component', 'n_intervals')]
    # )
    # def update_metrics(n):
    #     # logger.info('Tick is :{}'.format(n))
    #     # component = html.Div(id='bt_out') # create new children for some-output-component
    #     return 'Tick is :{}'.format(n)







