import re
import math
import os, sys
import shutil
import pickle

from PIL import Image

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
from libraries import image_functions, read_files_functions

main_fname = "10"
filename = "10"
filename2 = "11"
directory = "videos/street3/resized/min"

pixch_shapes_color = ( 0, 0, 255 )

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_dir = directory + "pixch/"
pixch_filename = filename + "." + filename2

pixch_shapes_dir = top_shapes_dir + pixch_dir + "shapes/" + pixch_filename + "/"

if os.path.exists(pixch_shapes_dir ) == False:
   os.makedirs(pixch_shapes_dir )

original_image = Image.open(top_images_dir + directory + main_fname + ".png")
original_pixel = original_image.getdata()
im_width, im_height = original_image.size

# returned value has below form
# { '79999':{'79999': {'x': 399, 'y': 199}, '79599': {'x': 399, 'y': 198}, ... }, ... }
# { 'shapeid': { 'pixel index': { 'x': x, 'y': y }, ... }, ... }
pixch_shapes = read_files_functions.rd_shapes_file(pixch_filename, pixch_dir)


for shapeid, pixels in pixch_shapes.items():
   new_im = Image.new('RGB', (im_width,im_height))

   newdata = []

   for y in range(im_height):
      for x in range(im_width):
 
         # current pixel in the same form as pixels in target_shapeid_pixels
         cur_pixel =  { 'x': x, 'y': y }
         current_pixel_index = (y * im_width)+ x    
         cur_pixel_color = original_pixel[ current_pixel_index ]
      
         if cur_pixel in pixels.values():
            newdata.append( pixch_shapes_color )
         else:
            newdata.append( cur_pixel_color )
      



   new_im.putdata (newdata)
   new_im.save (pixch_shapes_dir + shapeid + ".png")   





