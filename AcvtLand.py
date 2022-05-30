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

class AcvtLand():

    def __init__(self, app, header='Scanner : ', qlog = None):

        self.configLogger(qlog)

        self.header = header
        self.headertag = 0

        self.model = Model()
        self.app = app

        # Land Callbacks
        # @app.callback(  Output('button-state', 'children'),
        #                 Input('submit-button', 'n_clicks')
        #               )
        # def update_output(n_clicks):
        #
        #     return ('The Button has been pressed {} times').format(n_clicks)


        # @app.callback(  Output('url', 'pathname'),
        #                 Input('submit-button', 'n_clicks')
        #                 )
        # def update_output(n_clicks):
        #     return "/page-2"

        # @app.callback(  Output('page-content', 'children'),
        #                 Input('submit-button', 'n_clicks')
        #                 )
        # def update_output(n_clicks):
        #     return self.getLayout()


    def getLayout(self):
        self.model.headertag +=1

        return html.Div([

            dash.html.Img (src= self.app.get_asset_url('logo-bsw.png'), className="logofixed"),
            dash.html.H1 ('BSW Service Tools - Troubleshoot applications for CCD Instruments', className="labelfixed"),
            # dash.html.H1 ('Troubleshoot applications for CCD Instruments', className="labelfixed"),

            dbc.Container([
                    dbc.Card([
                            dbc.CardImg(src= self.app.get_asset_url('cement2.jpg'), top=True),
                            dbc.CardBody([dbc.Button("Scan Research", color="primary", href="/scanview")]),
                        ],
                        className="card-icon",),

                    dbc.Card([
                        dbc.CardImg(src= self.app.get_asset_url('petrochemical_plant.jpg'), top=True),
                        dbc.CardBody([dbc.Button("CCD Project Editor", color="primary", href="/ccdeditor")]),
                    ],
                        className="card-icon",),

                    dbc.Card([
                        dbc.CardImg(src= self.app.get_asset_url('research-icon11.jpg'), top=True),
                        dbc.CardBody([dbc.Button("Global Cache Inspector", color="primary", href="/")]),
                    ],
                        className="card-icon",),
                ],
                fluid=True,
                className="landcanvas",
            ),]

        )


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
    header: str = 'Scanner : '
    headertag : int = 0


    #
    # # html.H1(self.header+str(self.headertag), className="display-3"),
    # html.H1(self.model.header+str(self.model.headertag), className="display-3"),
    # html.P(
    #     "Use Containers 1 to create a jumbotron to call attention to "
    #     "featured content or information.",
    #     className="lead",
    # ),
    # html.Hr(className="my-2"),
    # html.P(
    #     "Use utility classes for typography and spacing to suit the larger container.",
    #     id='button-state'
    # ),


# image_filename = 'my-image.png' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#
# app.layout = html.Div([
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image))
# ])
