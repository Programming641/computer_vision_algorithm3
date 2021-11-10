
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

   # boundary_pixels has the following form
   # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, {'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
   # containing coordinates of boundary pixels
   original_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(original_shapeIDs_with_all_indexes[original_shape_id])

   for compare_shape_id in compare_shapeIDs_with_all_indexes:

      print("original_shape_id " + str(original_shape_id) + " compare_shape_id " + str( compare_shape_id ) )


      '''
      # compare shapes only if they contain enough pixels
      minimum_pixels_required = 15


      # one shape is too large or too small
      total_pixels_threshold = len(original_boundary_pixels) + minimum_pixels_required + round( len(original_boundary_pixels) * 0.1 )
      minus_total_pixels_threshold = len(original_boundary_pixels) - minimum_pixels_required - round( len(original_boundary_pixels) * 0.1 )

      
      if len(original_boundary_pixels) <= 5:
         print("original_failed")
         break
      
      if len(compare_boundary_pixels) <= 5:
         print("compare_failed")
         continue

      


      # one shape is too large or too small   
      if len(compare_boundary_pixels) >= total_pixels_threshold or len(compare_boundary_pixels) <= minus_total_pixels_threshold:
         print("compare is too large or too small")
         continue

      '''





      shape_ids = [ int(original_shape_id ), int (compare_shape_id ) ]

      compare_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(compare_shapeIDs_with_all_indexes[compare_shape_id])


      boundary_result = pixel_shapes_functions.find_shapes_in_diff_frames(original_boundary_pixels, compare_boundary_pixels, "boundary", shape_ids)
      
      if boundary_result:
         print("original_shape_id " + str(original_shape_id) + " compare_shape_id " + str( compare_shape_id ) + " boundary_result " + str(boundary_result) )

         boundary_result = pixel_shapes_functions.find_shapes_in_diff_frames(original_boundary_pixels, compare_boundary_pixels, "boundary", shape_ids)

         consecutive_result = pixel_shapes_functions.find_shapes_in_diff_frames(original_shapeIDs_with_all_indexes[original_shape_id], compare_shapeIDs_with_all_indexes[compare_shape_id], \
                                 "consecutive_count", shape_ids)

         if consecutive_result:
            print("original_shape_id " + str(original_shape_id) + " compare_shape_id " + str( compare_shape_id ) + " consecutive_result " + \
                  str(consecutive_result ) )





























      '''

      if consecutive_count_result == "original_failed":
         break
         
      if consecutive_count_result == "compare_failed":
         continue
      '''   
      




























