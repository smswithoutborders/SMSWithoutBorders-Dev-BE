import sys, os, logging
sys.stdout = sys.stderr
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/SMSWithoutBorders-Dev-BE')

from server import app as application
