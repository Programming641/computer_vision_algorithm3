import re
import math
import os, sys

from PIL import Image
from libraries.cv_globals import proj_dir
from libraries import pixel_shapes_functions, read_files_functions
import shutil, pickle
import winsound

shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"


im_fname = "1clrgrp"
directory = "videos/cat"



# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

combi_rpt_ptn_fname = shapes_dir + directory + "rpt_ptn/" + im_fname + "_combi_rpt_ptn_shapes.data"

combi_rpt_ptn_folder = shapes_dir + directory + "combi_rpt_ptn/" + im_fname

# delete and create folder
if os.path.exists(combi_rpt_ptn_folder) == True:
   shutil.rmtree(combi_rpt_ptn_folder)
   
if os.path.exists(combi_rpt_ptn_folder) == False:
   os.makedirs(combi_rpt_ptn_folder)

original_image = Image.open(images_dir + directory + im_fname + ".png")

image_width, image_height = original_image.size

original_image_data = original_image.getdata()

# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
im_shape_pixels = read_files_functions.rd_shapes_file(im_fname, directory)

with open (combi_rpt_ptn_fname, 'rb') as fp:
   combi_rpt_ptn_shapes = pickle.load(fp)


# match contains all shapes
for combi_rpt_ptn_shape in combi_rpt_ptn_shapes:

   shapeids = combi_rpt_ptn_shape[0]
   combi_shapeids = combi_rpt_ptn_shape[1]
   combi_shapeid = combi_shapeids["shapeid1"]

   new_image = Image.new('RGB', (image_width, image_height), ( 255, 255, 255 ) )


   
   cur_pixels = {}
   
   for im_shapeid, im_pindexes in im_shape_pixels.items():
      if im_shapeid in shapeids:
         cur_pixels = im_pindexes
   
   
      for cur_pindex, cur_pxy in cur_pixels.items():
         cur_pindex = int(cur_pindex)

         if len(original_image_data[ cur_pindex ]) == 3:
            original_image_red, original_image_green, original_image_blue = original_image_data[cur_pindex ]
         else:
            original_image_red, original_image_green, original_image_blue, alpha = original_image_data[cur_pindex ]      
             

         new_image.putpixel( (cur_pxy["x"], cur_pxy["y"] ) , (original_image_red, original_image_green, original_image_blue) )



   new_image.save(combi_rpt_ptn_folder  + '/' + combi_shapeid + '.png')




frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)     


    

















