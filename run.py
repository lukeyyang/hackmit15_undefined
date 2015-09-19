from app import app
from config import GOOGLEAPI_SECRET_DIR
import os

basedir = os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(os.path.join(basedir, GOOGLEAPI_SECRET_DIR)):
  print "FATAL: missing Google API secret"
else:
  app.run(debug = True)
