#!/usr/bin/env python3

import sys
from collections import deque
from itertools import islice

player1 = deque()
player2 = deque()

for line in open(sys.argv[1]).read().splitlines():
    if len(line) == 0:
        continue
    if line.startswith('Player '):
        if line.replace('Player ', '').replace(':', '') == '1':
            player = 1
        else:
            player = 2
        continue
    card = int(line)
    if player == 1:
        player1.append(card)
    else:
        player2.append(card)

# convert deques to tuple of tuples to
# get a hashable type
def deck_hash(d1, d2):
    return hash((tuple(d1), tuple(d2)))

def game(deck1, deck2):

    # Save hash of deck1, deck2 in prev_rounds.
    prev_rounds = set()

    while(len(deck1) > 0 and len(deck2) > 0):

        # Break recursion if this round has been played before
        h = deck_hash(deck1, deck2)
        if h in prev_rounds:
            return (1, deck1)

        # Save hash in prev_rounds
        prev_rounds.add(h)

        # Play round
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if len(deck1) < card1 or len(deck2) < card2:
            # Normal, non-recursive game
            if card1 < card2:
                winner = 2
            else:
                # Can't end in draw since cards are unique
                winner = 1
        else:
            # Recursive subgame with slices of deck1, deck2
            winner, deck = game(deque(islice(deck1, card1)), deque(islice(deck2, card2)))

        if winner == 1:
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

    # Game finished, one of the decks are empty
    if len(deck1) == 0:
        return (2, deck2)
    else:
        return (1, deck1)

winner, deck = game(player1, player2)
print('Player', winner, 'wins')
print(deck)

multiplier = 1
res = 0
while len(deck) > 0:
    res += deck.pop() * multiplier
    multiplier += 1
print(res)
