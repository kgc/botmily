from PIL import  Image
from PIL import  ImageDraw
from PIL import  ImageFont
import textwrap
import os.path, random, string
import urllib2  
from cStringIO import StringIO

def drawtext(draw, text, font, color, bbox):
    shadowcolor = "black"
    x0, y0, x1, y1 = bbox # note: y1 is ignored
    space = draw.textsize(" ", font)[0]
    #font2 = ImageFont.truetype("Impact.ttf", 13)
    words = text.split()
    x = x0; y = y0; h = 0
    for word in words:
        # check size of this word
        w, h = draw.textsize(word, font)
        # figure out where to draw it
        if x > x0:
            x += space
            if x + w > x1:
                # new line
                x = x0
                y += h
        #draw.text((x, y), word, font=font, fill=color)
        
        # thin border
        draw.text((x-.5, y-.5), word, font=font, fill=shadowcolor)
        draw.text((x-1.5, y-1.5), word, font=font, fill=shadowcolor)
        draw.text((x-1.5, y+1.5), word, font=font, fill=shadowcolor)
        draw.text((x+1.5, y-1.5), word, font=font, fill=shadowcolor)
        
        #text
        draw.text((x,y), word, font=font, fill=color)
        
        x += w
    return y + h

def getImageFromUrl(url):
    opener1 = urllib2.build_opener()  
    page1 = opener1.open(url)  
    data = StringIO(page1.read())
    img = Image.open(data)
    return img

def makeMacro(imgUrl , text ,fileName):
    image = getImageFromUrl(imgUrl)
    imgWidth = image.size[0]
    imgHeight = image.size[0]
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("impact.ttf", 42)
    bbox = (50, 0, imgWidth, imgHeight)
    drawtext(draw, text, font, "white", bbox)
    image.save(fileName , 'JPEG')

