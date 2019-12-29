import re
from PIL import Image
import os
import read_files_functions






filename = "birdcopy face color group"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'

repeating_shapes_pattern_filename = "shapes/" + filename + " with repeating pattern shapes.txt"

repeating_shapes_pattern_foldername = filename + " with repeating pattern shapes"

# if the folder does not exists, create it
if os.path.exists("shapes/objectshape/" + repeating_shapes_pattern_foldername) == False:
   os.mkdir("shapes/objectshape/" + repeating_shapes_pattern_foldername)

repeating_shapes_pattern_path = "shapes/objectshape/" + repeating_shapes_pattern_foldername + "/" + filename


original_image = Image.open("images/" + directory + filename + ".png")

image_width, image_height = original_image.size

original_image_data = original_image.getdata()



repeating_shapes_patterns = read_files_functions.read_dict_key_value_list(filename, directory, repeating_shapes_pattern_filename)

# we need to get every pixel of the shapes
# return value form is
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes_pixels = read_files_functions.read_shapes_file(filename, directory)

file_counter = 1

for key in repeating_shapes_patterns:
   print(" new image " + str(file_counter) + " created ")

   new_image = Image.new('RGB', (image_width, image_height) )

   for repeating_pattern_shape in repeating_shapes_patterns[key]:


      for image_shape_id in shapes_pixels:
      
         if repeating_pattern_shape == image_shape_id:
            # getting all pixels of one of the shapes in the list
            for pixel_index in shapes_pixels[image_shape_id]:
         
               # getting pixel's rgb
               x = shapes_pixels[image_shape_id][pixel_index]['x']
               y = shapes_pixels[image_shape_id][pixel_index]['y']             
               
               r, g, b, a = original_image_data[int(pixel_index)]
               
               new_image.putpixel( (x, y) , (r, g, b) )


   new_image.save(repeating_shapes_pattern_path + str(file_counter) + ".png")

   file_counter += 1



































