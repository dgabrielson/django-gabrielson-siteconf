#########################################################
####
#### Local override settings -- new style.
####
#########################################################
# The very last thing the settings file does should be
#   importing this file.
#########################################################
#######################
from __future__ import print_function, unicode_literals

import itertools
import json
import os
import sys

########################################################

# use caution: this file *should not* be accessible via your web server.
config_basename = os.path.basename(os.environ.get("VIRTUAL_ENV", "/django"))

# use caution: this file *should not* be accessible via your web server.
CONFIG_FILENAME = config_basename + "-settings.json"
# CONFIG_FILENAME = 'stats_site.conf.json'
basename_list = [CONFIG_FILENAME, "django_site.conf.json"]

#########################################################

BASE_PATHS = [
    "/etc",
    "/etc/apache2",
    "/etc/nginx",
    "/usr/local/etc",
    os.path.expanduser("~"),
]

# this will check each base path for each basename; in that order
#   so /etc/django_site.conf.json takes precedence over
#   /usr/local/etc/{VIRTUAL_ENV}-settings.json
def json_conf():
    for dirname, basename in itertools.product(BASE_PATHS, basename_list):
        fn = os.path.join(dirname, basename)
        if os.path.exists(fn):
            with open(fn, "r") as f:
                config = json.load(f)
            # for key, value in config.items():
            #     globals()[key] = value
            if config.get("DEBUG", False) and sys.stdout.isatty():
                print("Local config file '{}'".format(fn))
            return config
            # break
    return {}


#########################################################
