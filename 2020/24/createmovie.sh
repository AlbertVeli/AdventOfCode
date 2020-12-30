#!/bin/sh

rm -rf out
mkdir out
for p in *.png; do
	echo "$p"
	convert $p -resize 900x900 out/$p || exit 1
done
rm -rf out.mp4
ffmpeg -r 5 -i out/img%03d.png -c:v libx264 -vf "fps=25,format=yuv420p" out.mp4
