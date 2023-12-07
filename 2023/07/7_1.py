#!/usr/bin/env python3

import sys
sys.path.append('../..')
import aoc

lines = aoc.lines(sys.argv[1])

hands = []
for line in lines:
    hand, bet = line.split()
    bet = int(bet)
    hands.append((hand, bet))

def score_hand(hand):
    """
    high card = 0
    one pair = 1
    two pairs = 2
    three of a kind = 3
    full house = 4
    four of a kind = 5
    five of a kind = 6
    """
    values = [card for card in hand[0]]
    counts = {value: values.count(value) for value in values}
    vals = sorted(counts.values())
    if 5 in vals:
        return 6
    elif 4 in vals:
        return 5
    elif vals == [2, 3]:
        return 4
    elif 3 in vals:
        return 3
    elif vals == [1, 2, 2]:
        return 2
    elif 2 in vals:
        return 1
    else:
        # vals should be [1, 1, 1, 1, 1] here
        return 0

card_strengths = ('A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2')

# Note, all hands are unique
def compare_hands(a, b):
    sa = score_hand(a)
    sb = score_hand(b)
    if sa > sb:
        return a
    elif sb > sa:
        return b
    else:
        for i in range(len(a[0])):
            sa = card_strengths.index(a[0][i])
            sb = card_strengths.index(b[0][i])
            if sa < sb:
                return a
            elif sb < sa:
                return b
        # should not get here because all
        # cards are unique, but if we do
        # don't change order, return a
        return a

# hands should be almost sorted when we get
# here, so just do a simple bubble sort
def fine_sort(hands):
    while True:
        changed = False
        for i in range(len(hands) - 1):
            if compare_hands(hands[i], hands[i + 1]) == hands[i]:
                hand = hands[i]
                hands[i] = hands[i + 1]
                hands[i + 1] = hand
                changed = True
        if not changed:
            break
    return hands

# First do a rough sort based on score_hand
hands = sorted(hands, key = score_hand)
# Now also compare hands with same score
hands = fine_sort(hands)
winnings = []
for i in range(len(hands)):
    hand, bid = hands[i]
    winnings.append((i + 1) * bid)

print('Part 1:', sum(winnings))