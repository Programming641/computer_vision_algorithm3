import re
import math
import os, sys
import shutil

from PIL import Image

from libraries.cv_globals import proj_dir, internal
from libraries import read_files_functions, pixel_functions

import pickle
import winsound

top_shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"


filename = "13"
im_directory = "videos/street3/resized/min"
shapes_directory = "videos/street3/resized/min/spixc_shapes/"
shapes_type = "intnl_spixcShp"

# directory is specified but does not contain /
if im_directory != "" and im_directory[-1] != '/':
   im_directory +='/'
if shapes_directory != "" and shapes_directory[-1] != '/':
   shapes_directory +='/'

s_pixc_shape_nbrs_dir = top_shapes_dir + shapes_directory + "nbrs/"



s_pixc_shape_nbrs_filedir = s_pixc_shape_nbrs_dir + filename + "/"



# delete and create folder
if os.path.exists(s_pixc_shape_nbrs_filedir) == True:
   shutil.rmtree(s_pixc_shape_nbrs_filedir)

os.makedirs(s_pixc_shape_nbrs_filedir)




s_pixc_shape_nbrs_dfile = s_pixc_shape_nbrs_dir + "data/" + filename + ".data"

if shapes_type == "normal":

   # we need to get every pixel of the shapes
   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   shapes_pixels = read_files_functions.rd_shapes_file(filename, im_directory)
   
elif shapes_type == "intnl_spixcShp":   
   s_pixcShp_intnl_dir = top_shapes_dir + im_directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + filename + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      shapes_pixels = pickle.load(fp)
   fp.close()   



with open (s_pixc_shape_nbrs_dfile, 'rb') as fp:
   # [{'213': ['638', '641', '1066'], 'nbr_nbrs': ['215', '641', '1066', '1070', '635',... ]}, ... ]
   s_pixc_shape_nbrs = pickle.load(fp)
fp.close()


original_image = Image.open(images_dir + im_directory + filename + ".png")
image_width, image_height = original_image.size

for s_nbrs in s_pixc_shape_nbrs:
   original_image = Image.open(images_dir + im_directory + filename + ".png")

   # put together all shapes in one list
   s_nbrs_list = []
   shapeid = None
   for s_nbr in s_nbrs:
      # get shapeid first
      if s_nbr != "nbr_nbrs":
         shapeid = s_nbr
         
         if shapeid == "2":
            print( s_nbrs )
            sys.exit()
         
         s_nbrs_list.append( s_nbr )
      
      s_nbrs_list.extend( s_nbrs[s_nbr] )
      
   s_nbrs_list = list(dict.fromkeys(s_nbrs_list))
   

   for cur_shapeid in s_nbrs_list:
      if shapes_type == "normal":
         # need to get all pixels of current shape
         for pixel_index in shapes_pixels[cur_shapeid]:
            x = shapes_pixels[cur_shapeid][pixel_index]['x']
            y = shapes_pixels[cur_shapeid][pixel_index]['y']          

            new_image.putpixel( (x, y) , (255, 0, 0) )
      
      elif shapes_type == "intnl_spixcShp":
         # need to get all pixels of current shape
         for pixel_index in shapes_pixels[cur_shapeid]:
            xy = pixel_functions.convert_pindex_to_xy( pixel_index, image_width )
                   
            original_image.putpixel( xy , (255, 0, 0) )      
      
      

   original_image.save(s_pixc_shape_nbrs_filedir + str(shapeid) + ".png")


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

















