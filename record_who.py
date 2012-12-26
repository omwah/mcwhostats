#!/usr/bin/env python

import os
import sys
import sqlite3
import socket

SCRIPT_DIR = os.path.dirname(sys.argv[0])

sys.path.append(os.path.join(SCRIPT_DIR, 'mcstatus'))

from minecraft_query import MinecraftQuery

DB_FILE = os.path.join(SCRIPT_DIR, 'mc_players.db')

DFLT_PORT = 25565
QUERY_SERVERS = ( ('server1.com', DFLT_PORT),
                  ('server1.com', DFLT_PORT),
                )
TIMEOUT = 5 

do_db_init = False
if not os.path.exists(DB_FILE):
   do_db_init = True

conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

if do_db_init:
    c.execute('CREATE TABLE players_online (host text,  player_name text, online_at text)')

for host, port in QUERY_SERVERS:
    try:
        mc_query = MinecraftQuery(host, port, timeout=TIMEOUT)

        server_data = mc_query.get_rules()

        for player in server_data['players']:
            c.execute('INSERT INTO players_online VALUES ("%s:%d", "%s", datetime("now"))' % (host, port, player))
        #print "%s:%d %s" % (host, port, server_data['players'])

    except socket.error as e:
        print >>sys.stderr, '%s: Minecraft server "%s:%d" is unavailable' % (os.path.realpath(sys.argv[0]), host, port)

conn.commit()
conn.close()
