from __future__ import print_function
import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw
import random

filename = "../sample_images/screenshots/screenshot-20171002T000100Z-cccvw09.png"
blueScreenFilename = "../sample_images/test/testbluescreen.png"
gridFileName = "../sample_images/test/gridscreen.png"
cropFileName = "../sample_images/crop/crop"
img = Image.open(filename)
width, height = img.size
rows = 7
cols = 7
gridfill= (255,255,255,255)
cellwidth = width/cols
cellheight = height/rows

def drawgrid():
    draw = ImageDraw.Draw(img)
    for x in range(1, rows):
        draw.line((0,x*cellheight,width,x*cellheight), fill=gridfill)
    for x in range(1, cols):
        draw.line((x*cellwidth,0,x*cellwidth,height), fill=gridfill)
    img.save(gridFileName)

def drawBlueScreen():
    draw = ImageDraw.Draw(img)
    row = random.randint(0, rows-1)
    col = random.randint(0, cols-1)
    print(row)
    print(col)
    draw.rectangle(((col*cellwidth, row*cellheight), ((col+1)*cellwidth, (row+1)*cellheight)), fill="blue")
    img.save(blueScreenFilename)

def detectBlue():
    blueScreenImage = Image.open(blueScreenFilename)
    for c in range(0, cols):
        for r in range(0, rows):
            box = (c*cellwidth, r*cellheight, (c+1)*cellwidth, (r+1)*cellheight)
            crop = blueScreenImage.crop(box)
            crop.save(f"{cropFileName}-{r}-{c}.png")
            cvcrop = np.array(crop)
            cvcrop = cv.cvtColor(cvcrop, cv.COLOR_RGB2BGR)
            hsv = cv.cvtColor(cvcrop, cv.COLOR_BGR2HSV)

            ## mask of blue
            lower_blue = np.array([100,150,0])
            upper_blue = np.array([140,255,255])
            if not 0 in cv.inRange(hsv, lower_blue, upper_blue):
                print (f"DETECTED BLUE - row: {r} column {c}")

def main():
    ## drawgrid()
    drawBlueScreen()
    detectBlue()

if __name__== "__main__":
  main()
