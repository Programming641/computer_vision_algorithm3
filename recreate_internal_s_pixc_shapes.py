import re
import math
import os, sys
import shutil

from PIL import Image

from libraries.cv_globals import proj_dir
from libraries import read_files_functions

import pickle
import winsound

top_shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"


filename = "24"
im_directory = "videos/giraffe/min"


# directory is specified but does not contain /
if im_directory != "" and im_directory[-1] != '/':
   im_directory +='/'

s_pixc_shapes_dir = top_shapes_dir + im_directory + "s_pixc_shapes/"
main_dir = s_pixc_shapes_dir + "internal/"
main_data_dir = main_dir + "data/"
main_dfile = main_data_dir + filename + ".data"



internal_s_pixc_shapes_imdir = main_dir + filename + "/"



# delete and create folder
if os.path.exists(internal_s_pixc_shapes_imdir) == True:
   shutil.rmtree(internal_s_pixc_shapes_imdir)

os.makedirs(internal_s_pixc_shapes_imdir)


original_image = Image.open(images_dir + im_directory + filename + ".png")
image_width, image_height = original_image.size
original_image_data = original_image.getdata()


# we need to get every pixel of the shapes
# return value form is
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes_pixels = read_files_functions.rd_shapes_file(filename, im_directory)



with open (main_dfile, 'rb') as fp:
   # [('213','638'), ('641', '1066')... ]
   internal_s_pixc_shapes = pickle.load(fp)
fp.close()

# first, put internal shapes together that belong to the same large shape.
s_pixc_shapes_in_Lshape = {}
for shapeids in internal_s_pixc_shapes:
   
   if shapeids[1] in s_pixc_shapes_in_Lshape.keys():
      s_pixc_shapes_in_Lshape[ shapeids[1] ].append( shapeids[0] )
   else:
      s_pixc_shapes_in_Lshape[ shapeids[1] ] = [ shapeids[0] ]


for Lshapeid in s_pixc_shapes_in_Lshape:
   new_image = Image.new('RGB', (image_width, image_height), ( 255, 255, 255) )

   for pixel_index in shapes_pixels[Lshapeid]:
      x = shapes_pixels[Lshapeid][pixel_index]['x']
      y = shapes_pixels[Lshapeid][pixel_index]['y']          
         
      if len(original_image_data[int(pixel_index)]) == 3:
         r, g, b = original_image_data[int(pixel_index)]
      else:
         r, g, b, a = original_image_data[int(pixel_index)]
               
      new_image.putpixel( (x, y) , (r, g, b) )  
   

   for cur_shapeid in s_pixc_shapes_in_Lshape[Lshapeid]:

      # need to get all pixels of current shape
      for pixel_index in shapes_pixels[cur_shapeid]:
         x = shapes_pixels[cur_shapeid][pixel_index]['x']
         y = shapes_pixels[cur_shapeid][pixel_index]['y']          
         
         if len(original_image_data[int(pixel_index)]) == 3:
            r, g, b = original_image_data[int(pixel_index)]
         else:
            r, g, b, a = original_image_data[int(pixel_index)]
               
         new_image.putpixel( (x, y) , (r, g, b) )

   new_image.save(internal_s_pixc_shapes_imdir + str(Lshapeid) + ".png")


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

















