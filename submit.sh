#!/bin/sh

# To submit answer 42 for level 1, day 3:
# ./submit.sh 3 1 42

if [ "$#" != "3" ]; then
    echo "Usage: $0 <day> <level> <answer>"
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
source ${DIR}/cookie.txt

curl "https://adventofcode.com/${year}/day/${day}/answer" -H "$cookie" --data-raw "level=${2}&answer=${3}" --compressed
