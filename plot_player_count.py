#!/usr/bin/env python2.7

import os
import sys
import sqlite3
from datetime import datetime

from matplotlib import pyplot as plt
import matplotlib.dates as mdates

import numpy as np

SCRIPT_DIR = os.path.dirname(sys.argv[0])
DB_FILE = os.path.join(SCRIPT_DIR, 'mc_players.db')
PLOT_FILE = "/path/to/players_by_time.png"

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Distinct hostnames
host_list = [ row[0] for row in c.execute("select distinct host from players_online").fetchall() ]

fig,axes = plt.subplots(len(host_list), sharex=True)

# Format dates nicer
fig.autofmt_xdate()

for host, ax in zip(host_list, axes):
    time_query = 'select online_at, count(player_name) from players_online where host = "%s" group by online_at' % host
    players_per_time = c.execute(time_query).fetchall()
    players_per_time = np.array(players_per_time)
    #print host, players_per_time

    player_counts = [ int(count) for count in players_per_time[:,1] ]
    count_dts = [ datetime.strptime(dstr, "%Y-%m-%d %H:%M:%S") for dstr in players_per_time[:,0] ]

    #ax.plot(count_dts, player_counts, ".")
    ax.bar(count_dts, player_counts, width=0.01)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
    ax.set_title(host)
    ax.set_ylabel("Number of Players")

#plt.legend(host_list, 0)
fig.suptitle("SDF Minecraft Players over Time")
plt.savefig(PLOT_FILE)

conn.close()
