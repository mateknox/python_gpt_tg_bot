import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

# insert your bot token
TOKEN = "<TOKEN>"

# logger settings
logging.basicConfig(filename="logs.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
