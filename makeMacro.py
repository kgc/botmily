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

def drawAchieve(text):
    img = Image.open('achieve.png')
    draw = ImageDraw.Draw(img)
    shadowcolor = "black"
    x0 = 218 + 10
    y0= 128 
    y1 = 173 
    x1 = 884
    font = ImageFont.truetype("arial.ttf", 45)
    space = draw.textsize(" ", font)[0]
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
        #text
        draw.text((x,y), word, font=font, fill='white')        
        x += w
    return img
    
def overlayAchieve(text,url):
    target = getImageFromUrl(url)
    y = drawAchieve(text)
    basewidth = target.size[0]
    wpercent = basewidth/float(y.size[0])
    hsize = int((float(y.size[1])*float(wpercent)))
    y = y.resize((basewidth,hsize),Image.ANTIALIAS)
    target.paste(y ,(0,0) , y)
    target.save('achieved.png','PNG' )
    return 'achieved.png'