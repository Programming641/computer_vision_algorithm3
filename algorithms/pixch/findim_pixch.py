# it finds all pixel changes

from PIL import Image
import re, pickle

import os, sys
from libraries.cv_globals import top_shapes_dir, top_images_dir
from help_lib import create_pixch_image, create_pixch_shape_locations, find_pixch_shapes


directory = "videos/horse1/resized/min"
im1file = "3"
im2file = "4"
rest_of_filename = ""


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   
   rest_of_filename = sys.argv[2][0: len( sys.argv[2] ) - 4 ]

   directory = sys.argv[3]

   print("execute script findim_pixch.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )




# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


pixch_imdir = top_shapes_dir + directory + "pixch/"
pixch_data_dir = pixch_imdir + "data/"

im1 = Image.open(top_images_dir + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

im2 = Image.open(top_images_dir + directory + im2file + ".png" )
im2pxls = im2.getdata()
im2width, im2height = im2.size


pxlch_im2 = Image.new('RGB', (im1width,im1height))
pxlch_im1 = Image.new('RGB', (im1width,im1height))

image2_data = []
image1_data = []
pixch_data = set()


#image_size[0] is image width
for y in range(im1height):


  for x in range(im1width):

    #getting pixel index value.
    pixel_index =  ( y * im1width ) + x
    
    # if im1pxls[pixel_index] != im2pxls[pixel_index] and ( im1pxls[pixel_index] != (255, 255, 255) and im2pxls[pixel_index] != (255, 255, 255) ): 
    if im1pxls[pixel_index] != im2pxls[pixel_index] :
       image2_data.append( (255, 0, 0) )    
       image1_data.append( (255, 0, 0) )

       pixch_data.add( str(pixel_index) )

    else:
       # if pixel did not chage
       image2_data.append( im2pxls[pixel_index] )
       image1_data.append( im1pxls[pixel_index] )
    


pxlch_im2.putdata (image2_data)
pxlch_im1.putdata( image1_data )

   
if os.path.exists(pixch_imdir ) == False:
   os.makedirs(pixch_imdir )
if os.path.exists(pixch_data_dir ) == False:
   os.makedirs(pixch_data_dir )


pxlch_im2.save (pixch_imdir  + im1file + "." + im2file + "." + im2file + ".png" )
pxlch_im1.save(pixch_imdir  + im1file + "." + im2file + "." + im1file + ".png" )

with open(pixch_data_dir  + im1file + "." + im2file + ".data", 'wb') as fp:
   pickle.dump(pixch_data, fp)
fp.close()


create_pixch_image.do_create( im1file, im2file, directory )
find_pixch_shapes.do_find( im1file, im2file, directory)
create_pixch_shape_locations.do_create( im1file, im2file, directory)


















