from PIL import Image
from libraries import pixel_shapes_functions
from libraries import read_files_functions
import math

filename = "hanger001_color_group"

directory = ""

filename2 = "hanger002_color_group"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


original_image = Image.open("images/" + directory + filename + ".png")

image_width, image_height = original_image.size


compare_image = Image.open("images/" + directory + filename2 + ".png")

compare_image_width, compare_image_height = compare_image.size


# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
original_shapeIDs_with_all_indexes = read_files_functions.read_shapes_file(filename, directory)

compare_shapeIDs_with_all_indexes = read_files_functions.read_shapes_file(filename2, directory)



for original_shape_id in original_shapeIDs_with_all_indexes:


   for compare_shape_id in compare_shapeIDs_with_all_indexes:


      # boundary_pixels has the following form
      # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, {'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
      # containing coordinates of boundary pixels
      #original_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(original_shapeIDs_with_all_indexes[original_shape_id])
   
      #compare_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(compare_shapeIDs_with_all_indexes[compare_shape_id])   
   
      print("original_shape_id " + str(original_shape_id) + " compare_shape_id " + str( compare_shape_id ) )
   
      result = pixel_shapes_functions.find_shapes_in_diff_frames(original_shapeIDs_with_all_indexes[original_shape_id], compare_shapeIDs_with_all_indexes[compare_shape_id])

      if result == "original_failed":
         break
         
      if result == "compare_failed":
         continue
         
         
      if result == "identical":
         print("original_shape_id " + str(original_shape_id) + " compare_shape_id " + str( compare_shape_id ) + " are identical" )         































