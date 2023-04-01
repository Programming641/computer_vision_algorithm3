import re
from PIL import Image, ImageOps
import os
from libraries import read_files_functions

import shutil
import winsound




filename = "24"

directory = "videos/giraffe/min"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

rpt_ptn_folder = "shapes/" + directory + "rpt_ptn/"

repeating_shapes_pattern_filename = rpt_ptn_folder + filename + "_rpt_ptn_shapes.txt"

rpt_ptn_shape_foldername = rpt_ptn_folder + filename + "/"

# delete and create folder
if os.path.exists(rpt_ptn_shape_foldername) == True:
   shutil.rmtree(rpt_ptn_shape_foldername)

os.makedirs(rpt_ptn_shape_foldername)


original_image = Image.open("images/" + directory + filename + ".png")

image_width, image_height = original_image.size

original_image_data = original_image.getdata()


# returned form 
# [{'1738': ['1738', '1968', '14240']}, {'1738': [ '5674', '14240']}, ... ]
repeating_shapes_patterns = read_files_functions.rd_ldict_k_v_l(filename, directory, repeating_shapes_pattern_filename)

# we need to get every pixel of the shapes
# return value form is
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes_pixels = read_files_functions.rd_shapes_file(filename, directory)

prev_shape_id = None
same_shape_id_counter = 1
for rpt_ptn_dict in repeating_shapes_patterns:

   new_image = Image.new('RGB', (image_width, image_height), ( 0, 0, 255) )

   for shape_id, rpt_ptn_shape_ids in rpt_ptn_dict.items():
      if prev_shape_id == None:
         prev_shape_id = shape_id
      elif prev_shape_id == shape_id:
         
         same_shape_id_counter += 1
      
      else:
         same_shape_id_counter = 1
      
      for image_shape_id in shapes_pixels:
      
         if shape_id == image_shape_id or image_shape_id in rpt_ptn_shape_ids:
            # getting all pixels of one of the shapes in the list
            for pixel_index in shapes_pixels[image_shape_id]:
         
               # getting pixel's rgb
               x = shapes_pixels[image_shape_id][pixel_index]['x']
               y = shapes_pixels[image_shape_id][pixel_index]['y']             
               
               if len(original_image_data[int(pixel_index)]) == 3:
                  r, g, b = original_image_data[int(pixel_index)]
               else:
                  r, g, b, a = original_image_data[int(pixel_index)]
               
               new_image.putpixel( (x, y) , (r, g, b) )

   prev_shape_id = shape_id

   if same_shape_id_counter != 1:
      new_image.save(rpt_ptn_shape_foldername + str(shape_id) + "_" + str(same_shape_id_counter) + ".png")
   else:
      new_image.save(rpt_ptn_shape_foldername + str(shape_id) + ".png")


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)
























