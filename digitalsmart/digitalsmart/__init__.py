import sys
import os
sys.path[0] = os.path.abspath(os.path.join(os.path.curdir, "venv/lib/python3.7/site-packages"))
print(sys.path)
import pymysql
pymysql.install_as_MySQLdb()

