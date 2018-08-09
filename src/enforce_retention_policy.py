#!/usr/bin/python2
# -*- encoding: utf-8 -*-

import argparse
import sqlite3
import time
from yaml import safe_load

with open('retention.yaml') as retention:
    try:
        days_retain = int(safe_load(retention)["days"])
    except yaml.YAMLError as e:
        print(e)

seconds_retain = 60 * 60 * 24 * days_retain
seconds_since_epoch = int(time.time())
diff = seconds_since_epoch - seconds_retain

tables = [
    'mac',
    'probemon',
    'ssid',
    'vendor'
]

statements = ["delete from " + table + " where date < " + str(diff) for table in tables]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--db', default='probemon.db', help="database file name to use")
    args = parser.parse_args()
    
    conn = sqlite3.connect(args.db)
    c = conn.cursor()
    
    for statement in statements:
        c.execute(statement)

    try:
        conn.commit()
    except:
        time.sleep(5)
        # db is locked, retry
        try:
            conn.commit()
        except sqlite3.OperationalError as e:
            print(e)
            conn.close()
            sys.exit(1)
    conn.close()
    
main()
