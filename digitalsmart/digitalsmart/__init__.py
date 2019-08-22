import sys
import os
# sys.path[0] = os.path.abspath(os.path.join(os.path.curdir, "venv/lib/python3.7/site-packages"))
# print(sys.path)

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import pymysql
from .celeryconfig import app as share_app

share_app.config_from_object(celeryconfig)
pymysql.install_as_MySQLdb()
