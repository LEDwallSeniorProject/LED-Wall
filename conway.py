
import displayio
import board
import rgbmatrix
import framebufferio
import random

def apply_life_rule(old, new):
    width = old.width
    height = old.height
    for y in range(height):
        yyy = y * width
        ym1 = ((y + height - 1) % height) * width
        yp1 = ((y + 1) % height) * width
        xm1 = width - 1
        for x in range(width):
            xp1 = (x + 1) % width
            neighbors = (
                old[xm1 + ym1] + old[xm1 + yyy] + old[xm1 + yp1] +
                old[x   + ym1] +                  old[x   + yp1] +
                old[xp1 + ym1] + old[xp1 + yyy] + old[xp1 + yp1])
            new[x+yyy] = neighbors == 3 or (neighbors == 2 and old[x+yyy])
            xm1 = x


# Fill 'fraction' out of all the cells.
def randomize(output, fraction=0.33):
    for i in range(output.height * output.width):
        output[i] = random.random() < fraction

def conway(output):
    # based on xkcd's tribute to John Conway (1937-2020) https://xkcd.com/2293/
    conway_data = [
        b'  +++   ',
        b'  + +   ',
        b'  + +   ',
        b'   +    ',
        b'+ +++   ',
        b' + + +  ',
        b'   +  + ',
        b'  + +   ',
        b'  + +   ',
    ]

    for i in range(output.height * output.width):
        output[i] = 0
    for i, si in enumerate(conway_data):
        y = output.height - len(conway_data) - 2 + i
        for j, cj in enumerate(si):
            output[(output.width - 8)//2 + j, y] = cj & 1

def run( g1, g2, b1, b2, display ):
    
    # palette = displayio.Palette(2)
    #     run 2*n generations.
    # For the Conway tribute on 64x32, 80 frames is appropriate.  For random
    # values, 400 frames seems like a good number.  Working in this way, with
    # two bitmaps, reduces copying data and makes the animation a bit faster
    n = 200

    # After 2*n generations, fill the board with random values and
    # start over with a new color.
    randomize(b1)
    # Pick a random color out of 3 primary colors or white.
    # palette[1] = (
    #     (0x57c1fa if random.random() > .33 else 0) | #blue
    #     (0xbcfa57 if random.random() > .33 else 0) | #yellowgreen
    #     (0xf50cd2 if random.random() > .33 else 0))  #pink!
    # palette[1] = 0xffffff
    for _ in range(n):
        display.root_group = g1
        apply_life_rule(b1, b2)
        display.root_group = g2
        apply_life_rule(b2, b1)
    
    