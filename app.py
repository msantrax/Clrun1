"""
The Dash Server Testbench
"""
import os
from flask import Flask, render_template
from DashServer import DashServer
from CCDScan import CCDScan
from CCDProj import CCDProj

scanpath = '/Bascon/Bruker/Sandbox/Reverse1/'

# pylint: disable=C0103

# flserver = Flask(__name__)
flserver = None


def startapp(arg1, arg2):
    dserver = DashServer(flserver)
    dserver.getServer()


if __name__ == '__main__':
    dserver = DashServer(flserver)
    dserver.rundash()

    # ccdproj = CCDProj('/Bascon/Bruker/Q2-A/Sandbox_a/tst.svg')
    # ccdproj = CCDProj('./Cu000.ccdprj')


    pass


    # server_port = os.environ.get('PORT', '8080')
    # app.run(debug=False, port=server_port, host='0.0.0.0')



# import datetime
#
# import dash
# from dash.dependencies import Input, Output, State
# import dash_core_components as dcc
# import dash_html_components as html
#
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
# app.layout = html.Div([
#     dcc.Upload(
#         id='upload-image',
#         children=html.Div([
#             'Drag and Drop or ',
#             html.A('Select Files')
#         ]),
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'dashed',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px'
#         },
#         # Allow multiple files to be uploaded
#         multiple=True
#     ),
#     html.Div(id='output-image-upload'),
# ])
#
# def parse_contents(contents, filename, date):
#     return html.Div([
#         html.H5(filename),
#         html.H6(datetime.datetime.fromtimestamp(date)),
#
#         # HTML images accept base64 encoded strings in the same format
#         # that is supplied by the upload
#         html.Img(src=contents),
#         html.Hr(),
#         html.Div('Raw Content'),
#         html.Pre(contents[0:200] + '...', style={
#             'whiteSpace': 'pre-wrap',
#             'wordBreak': 'break-all'
#         })
#     ])
#
# @app.callback(Output('output-image-upload', 'children'),
#               Input('upload-image', 'contents'),
#               State('upload-image', 'filename'),
#               State('upload-image', 'last_modified'))
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children
#
# if __name__ == '__main__':
#     app.run_server(debug=True)


