from PIL import Image , ImageDraw , ImageFilter
import faceapi, urllib2
from StringIO import StringIO

#had to make this method because PIL wont let me draw a rectangle properly
def drawRect(img,top_left,bottom_right, width , color):
	draw = ImageDraw.Draw(img)
	top_right = bottom_right[0],top_left[1]
	bottom_left = top_left[0], bottom_right[1]

	if width > 1:
		top_left_l1 = top_left[0]  , top_left[1] - width/2
		top_right_l1 = top_right[0] , top_right[1] - width/2
		l1 = [top_left_l1,top_right_l1]

		top_right_l2 = top_right[0] - width/2, top_right[1]
		bottom_right_l2 = bottom_right[0] - width/2 , bottom_right[1]
		l2 = [top_right_l2 , bottom_right_l2]

		bottom_right_l3 = bottom_right[0]  , bottom_right[1] + width/2
		bottom_left_l3 = bottom_left[0]  , bottom_left[1] + width/2
		l3 = [bottom_right_l3,bottom_left_l3]

		bottom_left_l4 = bottom_left[0] + width/2 , bottom_left[1]
		top_left_l4 = top_left[0] + width/2 , top_left[1]
		l4 = [bottom_left_l4, top_left_l4]
	else:
		l1 = [top_left,top_right]
		l2 = [top_right,bottom_right]
		l3 = [bottom_left,bottom_right]
 		l4 = [bottom_left,top_left]

	draw.line(l1, fill=color, width=width)
	draw.line(l2, fill=color, width=width)
	draw.line(l3 ,fill=color, width=width)
	draw.line(l4, fill=color, width=width)

def getImageFromUrl(url):
	print url
	opener1 = urllib2.build_opener()  
	page1 = opener1.open(url)  
	data = StringIO(page1.read())
	img = Image.open(data)
	return img

def drawTags(tags,imgurl):
	image = getImageFromUrl(imgurl).convert('RGB').filter(ImageFilter.FIND_EDGES)
	for tag in tags:
		if tag.has_key('attributes'):
			if tag['attributes'].has_key('gender'):
				gender = tag['attributes']['gender']['value']
				center = int(tag['center']['x']) , int(tag['center']['y'])
				height = int(tag['height'])
				width = int(tag['width'])
				drawTag(gender,center,width,height,image)
	return image

def drawTag(gender,center,width,height,im):
	c1 = (center[0] - (width/2)) * im.size[0]/100 , (center[1] - (height/2)) * im.size[1]/100
	c3 = (center[0] + (width/2)) * im.size[0]/100 , (center[1] + (height/2)) * im.size[1]/100
	c2 = (center[0] + (width/2)) * im.size[0]/100 , (center[1] - (height/2)) * im.size[1]/100
	c4 = (center[0] - (width/2)) * im.size[0]/100 , (center[1] + (height/2)) * im.size[1]/100
	if gender == 'female':
		drawRect(im,c1,c3,width=4,color='blue')
	elif gender == 'male':
		drawRect(im,c1,c3,width=4,color='pink')
	else:
		raise Exception('Gender_Binary_Error , please check your priveldge')
