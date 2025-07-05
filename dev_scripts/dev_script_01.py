# --------------
# Author : Serge Zaugg
# Description : For devel only 
# --------------

import os 
import getpass

os.environ["MY_SECRET"] = getpass.getpass()  
os.getenv("MY_SECRET")
  
# set MY_SECRET=aflagabouf

# echo %MY_SECRET%


