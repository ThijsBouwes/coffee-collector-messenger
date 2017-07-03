import sys
from os.path import join
from dotenv import load_dotenv

dotenv_path = join(sys.path[0], '.env')
load_dotenv(dotenv_path)
