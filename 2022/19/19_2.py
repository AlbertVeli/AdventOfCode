#!/usr/bin/env python3

import sys
import re

blueprints = {}

for line in open(sys.argv[1]).read().rstrip().split('\n'):
    ints = list(map(int, re.findall(r'(\d+)', line)))
    no, ore_cost, clay_cost, obs_ore, obs_clay, geo_ore, geo_obs = ints
    # I borrowed the structure for storing the numbers from my sons solution
    ore = {'ore_cost': ore_cost}
    clay = {'ore_cost': clay_cost}
    obsidian = {'ore_cost': obs_ore, 'clay_cost': obs_clay}
    geode = {'ore_cost': geo_ore, 'obs_cost': geo_obs}
    # Part 2, only use 3 first blueprints
    if no <= 3:
        blueprints[no] = {'orebot': ore, 'claybot': clay, 'obsbot': obsidian, 'geobot': geode}


# goodness of a state is used for pruning
def goodness(state, bp):
    g  = state['clay'] + bp['obsbot']['clay_cost'] * state['obs']
    g += bp['obsbot']['clay_cost'] * bp['geobot']['obs_cost'] * state['geo']
    g += 2 * (state['claybots'] + bp['obsbot']['clay_cost'] * state['obsbots'] + \
            bp['obsbot']['clay_cost'] * bp['geobot']['obs_cost'] * state['geobots'])
    return g

def new_states(state, bp):
    orebots, claybots, obsbots, geobots, ore, clay, obs, geo = state.values()

    new_states = []

    new_states.append({
        'orebots': orebots, 'claybots': claybots, 'obsbots': obsbots, 'geobots': geobots,
        'ore': ore + orebots, 'clay': clay + claybots,
        'obs': obs + obsbots, 'geo': geo + geobots})

    if ore >= bp['orebot']['ore_cost']:
        new_states.append({
            'orebots': orebots + 1, 'claybots': claybots, 'obsbots': obsbots, 'geobots': geobots,
            'ore': ore + orebots - bp['orebot']['ore_cost'], 'clay': clay + claybots,
            'obs': obs + obsbots, 'geo': geo + geobots})

    if ore >= bp['claybot']['ore_cost']:
        new_states.append({
            'orebots': orebots, 'claybots': claybots + 1, 'obsbots': obsbots, 'geobots': geobots,
            'ore': ore + orebots - bp['claybot']['ore_cost'], 'clay': clay + claybots,
            'obs': obs + obsbots, 'geo': geo + geobots})

    if ore >= bp['obsbot']['ore_cost'] and clay >= bp['obsbot']['clay_cost']:
        new_states.append({
            'orebots': orebots, 'claybots': claybots, 'obsbots': obsbots + 1, 'geobots': geobots,
            'ore': ore + orebots - bp['obsbot']['ore_cost'], 'clay': clay + claybots - bp['obsbot']['clay_cost'],
            'obs': obs + obsbots, 'geo': geo + geobots})

    if ore >= bp['geobot']['ore_cost'] and obs >= bp['geobot']['obs_cost']:
        new_states.append({
            'orebots': orebots, 'claybots': claybots, 'obsbots': obsbots, 'geobots': geobots + 1,
            'ore': ore + orebots - bp['geobot']['ore_cost'], 'clay': clay + claybots,
            'obs': obs + obsbots - bp['geobot']['obs_cost'], 'geo': geo + geobots})
    
    return new_states

start = {'orebots': 1, 'claybots': 0, 'obsbots': 0, 'geobots': 0, 'ore': 0, 'clay': 0, 'obs': 0, 'geo': 0}
best = {}
for i in range(len(blueprints)):
    bp = blueprints[i + 1]
    states = [start]
    for minute in range(32):
        newstates = []
        for state in states:
            for ns in new_states(state, bp):
                newstates.append(ns)
        states = newstates
        if len(states) > 20000:
            states.sort(key = lambda state: goodness(state, bp), reverse = True)
            states = states[:20000]
    max_geo = max(states, key = lambda state: state['geo'])
    best[i + 1] = max_geo['geo']
res = 1
print(best)
for val in best.values():
    res *= val
print('Part 2:', res)
