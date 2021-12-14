import re
from PIL import Image
import os
from libraries import read_files_functions
import winsound
import shutil




filename = "bird01_clr_grp"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'

repeating_shapes_pattern_filename = "shapes/" + filename + "_rpt_ptn_shapes.txt"

repeating_shapes_pattern_foldername = filename + "_rpt_ptn_shapes"

# delete and create folder
if os.path.exists("shapes/objectshape/" + repeating_shapes_pattern_foldername) == True:
   shutil.rmtree("shapes/objectshape/" + repeating_shapes_pattern_foldername)
   
if os.path.exists("shapes/objectshape/" + repeating_shapes_pattern_foldername) == False:
   os.mkdir("shapes/objectshape/" + repeating_shapes_pattern_foldername)


repeating_shapes_pattern_path = "shapes/objectshape/" + repeating_shapes_pattern_foldername + "/"


original_image = Image.open("images/" + directory + filename + ".png")

image_width, image_height = original_image.size

original_image_data = original_image.getdata()



repeating_shapes_patterns = read_files_functions.rd_dict_key_value_list(filename, directory, repeating_shapes_pattern_filename)

# we need to get every pixel of the shapes
# return value form is
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes_pixels = read_files_functions.read_shapes_file(filename, directory)

for key in repeating_shapes_patterns:

   new_image = Image.new('RGB', (image_width, image_height) )

   for repeating_pattern_shape in repeating_shapes_patterns[key]:


      for image_shape_id in shapes_pixels:
      
         if repeating_pattern_shape == image_shape_id:
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


   new_image.save(repeating_shapes_pattern_path + str(repeating_pattern_shape) + ".png")



winsound.Beep(200, 500)































