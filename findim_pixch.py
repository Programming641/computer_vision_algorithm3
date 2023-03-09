

from PIL import Image
import re, pickle

import os, sys
from libraries.cv_globals import proj_dir

if proj_dir != "" and proj_dir[-1] != "/":
   proj_dir +='/'

top_shapes_dir = proj_dir + "shapes/"
top_images_dir = proj_dir + "images/"

directory = "videos/street3/resized/min"
im1file = "10"
im2file = "11"
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
pixch_data_dir = top_shapes_dir + directory + "pixch/data/"

im1 = Image.open(top_images_dir + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

im2 = Image.open(top_images_dir + directory + im2file + ".png" )
im2pxls = im2.getdata()
im2width, im2height = im2.size


pxlch_im = Image.new('RGB', (im1width,im1height))

image_data = []
pixch_data = []


debug = False


#image_size[0] is image width
for y in range(im1height):


  for x in range(im1width):

    #getting pixel index value.
    pixel_index =  ( y * im1width ) + x
    
    # if im1pxls[pixel_index] != im2pxls[pixel_index] and ( im1pxls[pixel_index] != (255, 255, 255) and im2pxls[pixel_index] != (255, 255, 255) ): 
    if im1pxls[pixel_index] != im2pxls[pixel_index] :
       image_data.append( (255, 0, 0) )    

       pixch_data.append( str(pixel_index) )

    else:
       # if pixel did not chage
       image_data.append( im2pxls[pixel_index] )
    
  if debug == True:
       break
    
  if debug == True:
       break


pxlch_im.putdata (image_data)


temp_num = [x for x in list(im1file) if x.isdigit()]
im1file_num = ""
for i in range( 0, len( temp_num ) ):
   im1file_num += temp_num[i]

im2file_num = ""
temp_num = [x for x in list(im2file) if x.isdigit()]
for i in range( 0, len( temp_num ) ):
   im2file_num += temp_num[i]
   
if os.path.exists(pixch_imdir ) == False:
   os.makedirs(pixch_imdir )
if os.path.exists(pixch_data_dir ) == False:
   os.makedirs(pixch_data_dir )

if rest_of_filename != "":
   rest_of_filename = "_" + rest_of_filename

pxlch_im.save (pixch_imdir  + im1file_num + "." + im2file_num + "result" + im2file_num + rest_of_filename + ".png" )

with open(pixch_data_dir  + im1file_num + "." + im2file_num + rest_of_filename + ".data", 'wb') as fp:
   pickle.dump(pixch_data, fp)
fp.close()






