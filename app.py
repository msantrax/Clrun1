"""
The Dash Server Testbench
"""
import os
from flask import Flask, render_template
from DashServer import DashServer
from CCDScan import CCDScan

scanpath = '/Bascon/Bruker/Sandbox/Reverse1/'

if __name__ == '__main__':
    dserver = DashServer()
    dserver.rundash()






# server_port = os.environ.get('PORT', '8080')
# app.run(debug=False, port=server_port, host='0.0.0.0')

# pylint: disable=C0103
# app = Flask(__name__)

# @app.route('/')
# def hello():
#     """Return a friendly HTTP greeting."""
#     message = "Adding from python 3.8"
#
#     """Get Cloud Run environment variables."""
#     service = os.environ.get('K_SERVICE', 'Unknown service')
#     revision = os.environ.get('K_REVISION', 'Unknown revision')
#
#     return render_template('index.html',
#                            message=message,
#                            Service=service,
#                            Revision=revision)
