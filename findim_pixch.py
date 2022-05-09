

from PIL import Image
import re

import os, sys


directory = "videos/street"
im1file = "1clrgrp"
im2file = "2clrgrp"

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'




im1 = Image.open("images/" + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

im2 = Image.open("images/" + directory + im2file + ".png" )
im2pxls = im2.getdata()
im2width, im2height = im2.size




print("im1width " + str(im1width) + " im1height " + str(im1height) )

pxlch_im = Image.new('RGB', (im1width,im1height))

newdata = []


debug = False


#image_size[0] is image width
for y in range(im1height):
  print("y is " + str(y))


  for x in range(im1width):

    #getting pixel index value.
    pixel_index =  ( y * im1width ) + x
    
    if im1pxls[pixel_index] != im2pxls[pixel_index] and ( im1pxls[pixel_index] != (255, 255, 255) and im2pxls[pixel_index] != (255, 255, 255) ) :
       
       newdata.append( im1pxls[pixel_index] )

    else:
       # if pixel did not chage
       newdata.append( (255, 255, 255) )    
    
  if debug == True:
       break
    
  if debug == True:
       break


pxlch_im.putdata (newdata)
pxlch_im.save ("images/" + directory + "diff12result1.png")








