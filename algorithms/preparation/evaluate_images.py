#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#
from libraries import pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir

from PIL import Image
import math
import os, sys
import winsound
import glob

from collections import OrderedDict
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir

image_filename = '1'

directory = "videos/street6/resized/"

if len(sys.argv) >= 2:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_shapes.py. filename " + image_filename + " directory " + directory )


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

image_width = image_height = original_im_pixel = None


def check_image_color_mode():
   for dir_content in glob.glob( top_images_dir + directory + "*" ):

      if dir_content[ len( dir_content ) - 4: len( dir_content ) ] == ".png":
         cur_image = Image.open(dir_content)
         cur_im_pixel = cur_image.getdata()         
         if len( cur_im_pixel[0] ) == 4:
            print("ERROR at check_image_color_mode")
            sys.exit()
   
   print("all image color modes are OK")
         
         

# loop all files and folders
for dir_content in glob.glob( top_images_dir + directory + "*" ):
   print( dir_content )
   
   cur_image = cur_im_pixel = cur_image_width = cur_image_height = None
   if dir_content[ len( dir_content ) - 4: len( dir_content ) ] == ".png":
   
      if image_width is None and image_height is None and original_im_pixel is None:

         original_image = Image.open(dir_content)
         original_im_pixel = original_image.getdata()
         image_width, image_height = original_image.size
         
         if len( original_im_pixel[0] ) == 4:
            original_image = original_image.convert("RGB")
            original_image.save( dir_content )
            

      else:
         cur_image = Image.open(dir_content)
         cur_im_pixel = cur_image.getdata()
         cur_image_width, cur_image_height = cur_image.size         

         if len( cur_im_pixel[0] ) == 4:
            cur_image = cur_image.convert("RGB") 
            cur_image.save( dir_content )            
      
         if image_width == cur_image_width and image_height == cur_image_height:
            print("image size is OK")
         else:
            print("ERROR at image size")
            sys.exit()


check_image_color_mode( )

image_areas = image_functions.get_image_areas( image_filename, directory )
if len( image_areas ) >= 1:
   print("image areas OK")





