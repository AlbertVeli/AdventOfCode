#!/usr/bin/env python3

from PIL import Image

with open('input.txt') as f:
    line = f.readline().rstrip()

pixels = []
for c in line:
    pixels.append(int(c))

w = 25
h = 6
layersize = w * h
nlayers = len(pixels) // layersize
layers = []
for i in range(nlayers):
    layers.append(pixels[i * layersize : (i + 1) * layersize])

# part 1
minzero = 1000000
mini = 0
for i in range(nlayers):
    zeros = layers[i].count(0)
    if zeros < minzero:
        minzero = zeros
        mini = i
# layer number mini has the fewest zeros
ones = layers[mini].count(1)
twos = layers[mini].count(2)
print(ones * twos)

# part 2, flatten image
flat = []
for i in range(layersize):
    for j in range(nlayers):
        pixel = layers[j][i]
        if pixel == 2:
            # transparent, next j
            continue
        else:
            # 0 or 1, append and go to next i
            flat.append(pixel)
            break

colors = [(0, 0, 0), (255, 255, 255)]
im = Image.new('RGB', (w, h))
for y in range(h):
    offs = y * w
    for x in range(w):
        pixel = flat[offs + x]
        im.putpixel((x, y), colors[pixel])
im.save('out.png')
