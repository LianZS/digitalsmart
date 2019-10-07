from __future__ import absolute_import, unicode_literals


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
import pymysql
# from __future__ import absolute_import, unicode_literals
from .celeryconfig import app as share_app

pymysql.install_as_MySQLdb()

share_app.config_from_object(celeryconfig)
