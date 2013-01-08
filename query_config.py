# Contains configuration values for query and plot routines

import os, sys
from collections import namedtuple

BASE_DIR = os.path.dirname(sys.argv[0])

# Database configuration
class GeneralConfig(object):
    db_file = os.path.join(BASE_DIR, 'mc_players.db')

# Config for querying servers
DFLT_PORT = 25565

class QueryConfig(GeneralConfig):
    # Spaceribs server for example
    # http://www.reddit.com/r/spaceribs
    servers = ( ('server.spaceribs.com', DFLT_PORT),
               )
    timeout = 5 

# Config for plotting players per time 
class PlayersPerTimePlotConfig(GeneralConfig):
    title = "Minecraft Players over Time"
    filename = os.path.join(BASE_DIR, "players_by_time.png")
    days_before = 7

    # Width in pixels of output image
    x_size = 1200
    # Size per host, image size is num hosts * y_size
    y_size = 300 

