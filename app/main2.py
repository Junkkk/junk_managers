import os
import sys

os.path = ['', '..'] + sys.path[1:]
os.system('alembic upgrade head')