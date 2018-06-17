import os
import sys
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__),     'env/local/lib/python3.4/site-packages'))

# Path of execution
#sys.path.append('/var/www/winemapper')

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'env/bin/activate_this.py'))

with open(activate_env) as f:
	exec(f.read(), dict(__file__=activate_env))

sys.path.insert(0,"/var/www/winemapper")

#execfile(activate_env, dict(__file__=activate_env))
#code = compile(f.read(), "somefile.py", 'exec')
#exec(open(activate_env).read())

# import my_flask_app as application
from app import app as application
