#!/usr/bin/env python2.7

import os
import sys
import sqlite3
from datetime import datetime

from matplotlib import pyplot as plt
import matplotlib.dates as mdates

import numpy as np

# Import config
from query_config import PlayersPerTimePlotConfig as config 

conn = sqlite3.connect(config.db_file)
c = conn.cursor()

# Distinct hostnames
host_list = [ row[0] for row in c.execute("select distinct host from players_online").fetchall() ]

# Get player counts per host
host_players_per_time = {}
for host in host_list:
    time_query = 'select online_at, count(player_name) from players_online where host = "%s" and strftime("%%s", online_at) > strftime("%%s", "now", "-%d days") group by online_at' % (host, config.days_before)

    players_per_time = c.execute(time_query).fetchall()
    players_per_time = np.array(players_per_time)

    if len(players_per_time) > 0:
        host_players_per_time[host] = players_per_time

num_hosts = len(host_players_per_time)
fig,axes = plt.subplots(num_hosts, sharex=True, figsize=(config.x_size/100.0, config.y_size/100.0*num_hosts+2), dpi=100)
if not hasattr(axes, "__iter__"):
    axes = [ axes ]

# Format dates nicer
fig.autofmt_xdate()

for host, ax in zip(host_players_per_time.keys(), axes):
    players_per_time = host_players_per_time[host]

    player_counts = [ int(count) for count in players_per_time[:,1] ]
    count_dts = [ datetime.strptime(dstr, "%Y-%m-%d %H:%M:%S") for dstr in players_per_time[:,0] ]

    #ax.plot(count_dts, player_counts, ".")
    ax.bar(count_dts, player_counts, width=0.001)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d %H:%M"))
    ax.set_title(host)
    ax.set_ylabel("Number of Players")

#plt.legend(host_list, 0)
fig.suptitle(config.title)
plt.savefig(config.filename)

conn.close()
