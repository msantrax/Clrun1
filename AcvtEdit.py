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

    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    # fig.update_layout(
    #     plot_bgcolor=self.colors['background'],
    #     paper_bgcolor=self.colors['background'],
    #     font_color=self.colors['text']
    # )

    def __init__(self, app, config, qlog = None):

        self.configLogger(qlog)
        self.app = app

        self.loadedfiles = dict()
        self.fileslist = list()
        self.loadedfile_ptr = 0

        self.loadedscans = OrderedDict()

        self.CurrentScanDescriptor = namedtuple('CurrentScanDescriptor', 'file chip intnum chipvals intvals')
        self.currentscan = None

        self.graphlayout = {'autosize':True,
                            'margin': Margin (t=30, b=10),
                            'legend': Legend(itemclick = 'toggleothers'),
                            'clickmode': 'event+select'}

        self.update_scan_selection  = False

        loadlist = config['lastloaded']
        for toload in loadlist:
            tokens = toload.split(':')
            file = tokens[0]
            if not file in self.loadedfiles.keys():
                ccdscantemp = CCDScan( file+".ccdos", config)
                self.loadedfiles[file] = ccdscantemp
                entry = {'label': file, 'value': file}
                self.fileslist.append(entry)
            else:
                ccdscantemp = self.loadedfiles[file]

            chip = int(tokens[1])
            intnum = int(tokens[2])
            rows = ccdscantemp.getScanRows(chip, intnum)
            trace = go.Scatter(x=rows [:, 0], y=rows [:, 1], showlegend=True, name=toload, line_shape='spline')
            self.loadedscans[toload] = trace

        self.loadedfile_ptr = len(self.fileslist)-1
        self.newCurrentScan(file, chip, intnum, ccdscantemp)

        self.traces =  [*self.loadedscans.values()]
        fig = go.Figure(data=self.traces,  layout = self.graphlayout )


        self.layout_page = html.Div(children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.H3(children='BSW Scan Research - Beta 1.0.3',style = {"color": "white"}), width="auto" ),
                ], style = {"background-color": "green", "height" : "60px", "align-items" : "center", "margin-bottom": "15px"} ),
                dbc.Row([
                    dbc.Col(html.Div(children = self.getFileForm(),
                            style = {"margin-left": "25px", "display": "flex", "column-gap" : "25px", "justify-content" : "left", "align-items" : "center"},
                            id = 'scanrow')
                    ,width="auto"),
                ], ),
                dbc.Row([
                    dcc.Graph(
                        id='scangraph',
                        figure=fig,
                    )
                ], ),
                dbc.Row([
                    html.Div([
                        html.Div(id='dummy1', style = {"display": "none"}),
                        html.P('Test1', id='testlabel', style = {"display": "inline-block"}),
                    ] ,
                    id='bottom_row',
                    style = {"margin-left": "25px", "display": "flex", "column-gap" : "25px", "justify-content" : "left", "align-items" : "center"})

                ], ),
            ], fluid=True),
            self.installTimer(),
        ])


        @self.app.callback( Output('scanrow', 'children'),
                            Input('scantimer', 'n_intervals'),
                        )
        def update_page(n_intervals):
            updates = [dash.no_update, dash.no_update]
            # print ('Scanedit timer tick ...')

            if self.update_scan_selection :
                self.update_scan_selection = False
                return self.getFileForm()

            return dash.no_update



        @self.app.callback(  Output('dummy1', 'visible'),
                             Input('scangraph', 'restyleData'))
        def display_restyle_data(data):

            if data is not None:
                print (data)
                visibles = data[0]['visible']
                if 'legendonly' in visibles:
                    for idx in range(0, len(visibles)):
                        val = visibles[idx]
                        if isinstance(val, bool):
                            self.loadedfile_ptr = idx
                            scans = list(self.loadedscans.values())
                            scan = scans[idx]
                            tokens = scan.name.split(':')
                            self.currentscan[0] = tokens[0]
                            tempscan = self.loadedfiles[tokens[0]]
                            self.currentscan[1] = int(tokens[1])
                            self.currentscan[2] = int(tokens[2])
                            chipnums = ccdscantemp.getChipNums()
                            self.currentscan[3] = chipnums
                            scanint, default = ccdscantemp.getIntegrations(self.currentscan[1])
                            self.currentscan[4] = scanint
                            self.update_scan_selection = True
                            self.currentscan[8] = False # Btactions
                            return dash.no_update

            return dash.no_update


        @self.app.callback( Output('scangraph', 'figure'),
                            Input('bt_remove', 'n_clicks'),
                            Input('bt_add', 'n_clicks'),
                            Input('bt_reset', 'n_clicks'),
                            )
        def update_traces(rem, add, rst):

            ctx = dash.callback_context
            if not ctx.triggered or not self.currentscan[8]:
                input_id = 'bt_none'
                self.currentscan[8] = True
            else:
                input_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if input_id == 'bt_remove':
                self.loadedscans.pop('{}:{}:{}'.format(self.currentscan[0], self.currentscan[1], self.currentscan[2]))
                self.traces =  [*self.loadedscans.values()]
                fig = go.Figure(data=self.traces, layout = self.graphlayout)
                self.currentscan[5] = True # Remove bt
                self.currentscan[6] = False  # Add Bt
                self.currentscan[7] = True # Reset Bt
                self.update_scan_selection = True
                self.currentscan[8] = False # Btactions
                return fig
            elif input_id == 'bt_reset':
                pass
            elif input_id == 'bt_add':
                newid = '{}:{}:{}'.format(self.currentscan[0], self.currentscan[1], self.currentscan[2])
                ccdscantemp = self.loadedfiles[self.currentscan[0]]
                rows = ccdscantemp.getScanRows(self.currentscan[1], self.currentscan[2])
                trace = go.Scatter(x=rows [:, 0], y=rows [:, 1], showlegend=True,
                                   name= newid)
                self.loadedscans[newid] = trace
                self.traces =  [*self.loadedscans.values()]
                fig = go.Figure(data=self.traces, layout = self.graphlayout)
                self.currentscan[5] = False # Remove bt
                self.currentscan[6] = True  # Add Bt
                self.currentscan[7] = False # Reset Bt
                self.update_scan_selection = True
                self.currentscan[8] = False # Btactions
                return fig

            else:
                return dash.no_update


        @self.app.callback( Output('dummy1', 'children'),
                            Input('scanfiles', 'value'),
                            Input('chip_num', 'value'),
                            Input('scan_num', 'value'),
                           )
        def update_actions(file, chip, scan):

            ctx = dash.callback_context
            if not ctx.triggered:
                input_id = 'None'
                return dash.no_update
            else:
                input_id = ctx.triggered[0]['prop_id'].split('.')[0]

            # print ('Updating buttons (context = {}) based on values {} - {} - {}'.format(input_id, file, chip , scan))

            if input_id == 'scanfiles':
                if file == self.currentscan[0] : return dash.no_update
                ccdscantemp = self.loadedfiles[file]
                scanint, default = ccdscantemp.getIntegrations(0)
                chipnums = ccdscantemp.getChipNums()

                self.currentscan[0] = file
                self.currentscan[1] = 0
                self.currentscan[2] = default
                self.currentscan[3] = chipnums
                self.currentscan[4] = scanint

            elif input_id == 'scan_num':
                if scan == self.currentscan[2] : return dash.no_update
                self.currentscan[2] = scan

            elif input_id ==  'chip_num':
                if chip == self.currentscan[1] : return dash.no_update
                self.currentscan[1] = chip
                ccdscantemp = self.loadedfiles[self.currentscan[0]]
                scanint, default = ccdscantemp.getIntegrations(chip)
                self.currentscan[4] = scanint
                self.currentscan[2] = default

            link = '{}:{}:{}'.format(self.currentscan[0], self.currentscan[1], self.currentscan[2])
            print ('Update Buttons based on : '+ link)
            if link in self.loadedscans:
                # self.update_scan_selection = True
                self.currentscan[5] = False # Remove bt
                self.currentscan[6] = True  # Add Bt
                self.currentscan[7] = False # Reset Bt
            else:
                # self.update_scan_selection = True
                self.currentscan[5] = True
                self.currentscan[6] = False
                self.currentscan[7] = True

            self.update_scan_selection = True
            self.currentscan[8] = False # Btactions
            return dash.no_update


        @self.app.callback( Output('scanfiles', 'options'),
                            Output('scanfiles', 'value'),
                            Input('upload', 'filename')
                            )
        def update_scanfile(value:str):
            print ('Updating Scan file based on upload {}'.format(value))
            if value is None: return dash.no_update, dash.no_update
            file = value.replace(".ccdos", "")
            if not file in self.loadedfiles.keys():
                ccdscantemp = CCDScan( file+".ccdos", config)
                self.loadedfiles[file] = ccdscantemp
                entry = {'label': file, 'value': file}
                self.fileslist.append(entry)
                self.currentscan[0] = file  # File name
                ccdscantemp = self.loadedfiles[self.currentscan[0]]
                scanint, default = ccdscantemp.getIntegrations(chip)
                chipnums = ccdscantemp.getChipNums()

                self.currentscan[1] = 0  # Chip value
                self.currentscan[2] = default  # Integration Value
                self.currentscan[3] = chipnums  # Chip list
                self.currentscan[4] = scanint  # Integrations list

                print ('File {} was loaded'.format(value))
                self.update_scan_selection = True
                self.currentscan[8] = False # Btactions
            else:
                print ('File {} is already loaded'.format(value))

            return self.fileslist, file



        # @self.app.callback( Output('chip_num', 'options'),
        #                     Output('chip_num', 'value'),
        #                     # Output('scan_num', 'options'),
        #                     # Output('scan_num', 'value'),
        #                     Input('scanfiles', 'value')
        #                     )
        # def update_scandetails(value:str):
        #     print ('Updating chip num based on file {}'.format(value))
        #     ccdscantemp = self.loadedfiles[value]
        #     # scanint = ccdscantemp.getIntegrations(0)
        #     chipnums = ccdscantemp.getChipNums()
        #     self.currentscan[3] = chipnums
        #     self.currentscan[1] = 0 #int(value)
        #     return chipnums, 0
        #
        #
        # @self.app.callback( Output('scan_num', 'options'),
        #                     Output('scan_num', 'value'),
        #                     Input('chip_num', 'value'),
        #                     Input('scanfiles', 'value')
        #                     )
        # def update_integrations(value, svalue ):
        #     print ('Updating Integrations based on chip {}'.format(value))
        #     ccdscantemp = self.loadedfiles[svalue]
        #     self.currentscan[0] = svalue
        #     scanint, default = ccdscantemp.getIntegrations(int(value))
        #     if self.currentscan[1] == None : self.currentscan[1] = int(value)
        #     if self.currentscan[2] == None : self.currentscan[2] = default
        #     if self.currentscan[4] == None : self.currentscan[4] = scanint
        #     return scanint, default
        #
        #

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


    def getFileForm(self):
        # out = html.Div([

        out = [
            html.Label('Scan File :', style = {"display": "inline-block"}),
            # dcc.Input(id='input-scanfile', type='text', value="insert value !", style = {"width": "600px", "display": "inline-block"}),
            dcc.Dropdown(id='scanfiles',options=self.fileslist, value=self.currentscan[0],
                         style = {"width": "400px", "display": "inline-block"}),

            dcc.Upload(dbc.Button("...", color="primary", id='load_scan', className="lead"), id='upload'),

            html.Label('Chip Nr. :', style = {"display": "inline-block"}),
            dcc.Dropdown(id='chip_num', options=self.currentscan[3],
                                        value=self.currentscan[1],
                                        style = {"width": "80px", "display": "inline-block"}),

            html.Label('Integration. Time :', style = {"display": "inline-block"}),
            dcc.Dropdown(id='scan_num', options= self.currentscan[4],
                                        value=self.currentscan[2],
                                        style = {"width": "140px", "display": "inline-block"}),

            html.Div([
                    dbc.Button("Remove", color="primary", id='bt_remove', className="lead", disabled=self.currentscan[5]),
                    dbc.Button("Add", color="primary", id='bt_add', className="lead", disabled=self.currentscan[6]),
                    dbc.Button("Reset", color="primary", id='bt_reset', className="lead", disabled=self.currentscan[7]),
                ],id='trace_buttons',
                style = {"margin-left": "25px", "display": "flex", "column-gap" : "25px", "justify-content" : "left", "align-items" : "center"}
            )
        ]
        # ], style = {"margin-left": "25px", "display": "flex", "column-gap" : "25px", "justify-content" : "left", "align-items" : "center"})

        return out


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




#
# Updating details based on file RE12_1075_221
# Listing scan[0/0] of file [RE12_1075_221.ccdos] EntryPoint @3838
# Infodir key [ChipNo] is [0]
# Infodir key [IntegrationTime] is [6666]
# Infodir key [CreatedOn] is [202112091632378699]
# Infodir key [ChipOrientationReversed] is [False]
# Infodir key [Hostname] is [BE2334]
# Infodir key [QLS1FirmwareVer] is [V2.18]
# Infodir key [QLS1BoardNo] is [2027500686]
# Infodir key [SampleName] is [RE 12/110]
# Infodir key [Scanfile] is [C:\Program Files\QUANTRON\QMatrix\Results\Scans\RE 12_110_QIFe01Q2    01075_20211209163221.ccdos]
# Infodir key [InstrRefXDiffPolyCoeffs] is [0.0]
# Infodir key [XShiftPolyCoeffs] is [0.105069095190944@-9.03905144400729E-05@2.66378035647102E-08]
# Infodir key [LightPath] is [2]
# Infodir key [SequenceName] is [QIFe01Q2    01075]
# Infodir key [ScanNumber] is [0]
# Infodir key [ScanType] is [15]
# Infodir key [ScanID] is [[51]]
# Infodir key [ScanSize] is [3694]
# Infodir key [ScanBegin] is [3825]
# Infodir key [PayloadInit] is [3838]
# Infodir key [PayloadSize] is [59108]
# Infodir key [TailDataInit] is [62947]
# Infodir key [TailDataSize] is [[732]]
# Infodir key [ScanEnd] is [63684]
# Infodir key [FilePath] is [RE12_1075_221.ccdos]
# Infodir key [FileSize] is [602476]
# Infodir key [RecNumber] is [10]
# Infodir key [RecSize] is [41]
# Infodir key [EntryPoint] is [3416]
# Int Callback is 0
