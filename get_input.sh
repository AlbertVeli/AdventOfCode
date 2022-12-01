#!/bin/sh

# To get input for day 3:
# ./get_input.sh 3

if [ "$#" != "1" ]; then
    echo "Usage: $0 <day>"
    exit 1
fi

# Do some magic to follow symlinks, to read cookie.txt
# Does the same as readlink --canonicalize on Linux
cd $(dirname $0)
TARGET_FILE=$(basename $0)

# Iterate down a (possible) chain of symlinks
while [ -L "$TARGET_FILE" ]
do
	TARGET_FILE=$(readlink $TARGET_FILE)
	cd $(dirname $TARGET_FILE)
	TARGET_FILE=$(basename $TARGET_FILE)
done
DIR=$(pwd -P)

day=$1

# Put your own session cookie and year in cookie.txt
# year=2019
# cookie='cookie: session=1234abcd..'
. ${DIR}/cookie.txt || exit 1

agent='github.com/AlbertVeli/AdventOfCode'

curl "https://adventofcode.com/${year}/day/${day}/input" -A "$agent" -H "$cookie" --compressed
