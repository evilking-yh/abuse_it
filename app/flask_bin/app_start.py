#!flask/bin/python
import sys
from os.path import dirname, abspath
import os
sys.path.append(dirname(dirname(abspath(__file__))))

from flask_bin import app, routes

app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")

