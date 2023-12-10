#!/usr/bin/env python3

import json
from datetime import datetime
import sys

def date_str(ts_str):
    ts = int(ts_str)
    # Add %Y or %y for year
    return datetime.fromtimestamp(ts).strftime('%m/%d %H:%M:%S')

# Put your local leaderboard in leaderboard.json
# Download it from https://adventofcode.com/2021/leaderboard/private/view/<id>.json
# where id is your private leaderboard id.
data = json.loads(open(sys.argv[1]).read())

# Just for debug, see what fields there are
#for member in data['members']:
#    if data['members'][member]['name'] != 'Albert Veli':
#        continue
#    print(data['members'][member])

# Header
inverse ='\033[7m'
inverse_off = '\033[27m'
name = 'Name'
last_star = 'Last Star'
# The f-string notation is available from python3.6
print(f'{inverse}{name:23}  {last_star:15}{inverse_off}')

# Data
for member in data['members']:
    if data['members'][member]['name']:
        name = data['members'][member]['name']
    else:
        name = f'anonymous user #{member}'
    last_star = date_str(data['members'][member]['last_star_ts'])
    print(f'{name:23}  {last_star:15}')
