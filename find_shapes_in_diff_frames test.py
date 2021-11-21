
from PIL import Image
from libraries import pixel_shapes_functions
from libraries import video_algorithms
from libraries import read_files_functions
import math

filename = "hanger002_color_group"

directory = ""

filename2 = "hanger003_color_group"

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

all_shape_match_results = []


for original_shape_id in original_shapeIDs_with_all_indexes:

   match_results = {}
   match_results[ int(original_shape_id )] = []

   print(" original_shape_id " + str(original_shape_id ) )

   # boundary_pixels has the following form
   # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, {'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
   # containing coordinates of boundary pixels
   original_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(original_shapeIDs_with_all_indexes[original_shape_id], int(original_shape_id) )

   for compare_shape_id in compare_shapeIDs_with_all_indexes:

      
      shape_ids = [ int(original_shape_id ), int (compare_shape_id ) ]

         
      print("compare shape " + str(shape_ids[1]) )
      compare_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(compare_shapeIDs_with_all_indexes[compare_shape_id], int(compare_shape_id) )
      boundary_result = None
      boundary_result = video_algorithms.find_shapes_in_diff_frames(original_boundary_pixels, compare_boundary_pixels, "boundary", shape_ids)

      result = video_algorithms.find_shapes_in_diff_frames(original_shapeIDs_with_all_indexes[original_shape_id], \
                                                             compare_shapeIDs_with_all_indexes[compare_shape_id],  "consecutive_count", shape_ids)

      print(" result " + str(result) )
      if result:
               
         temp = {}
            
         if boundary_result:
            match_result = round( result + boundary_result )
         else:
            match_result = round( result )
               
         temp[compare_shape_id] = match_result
         match_results[shape_ids[0]].append(temp)
            

   if match_results[shape_ids[0]]:
      all_shape_match_results.append(match_results)
      
   closest_match = {}
   prev_compare_shapeid = None
   for matches in match_results[shape_ids[0]]:
      for compare_shapeid in matches:
         
         # closest_match initialization
         if not closest_match:
            closest_match[compare_shapeid] = matches[compare_shapeid]
            prev_compare_shapeid = compare_shapeid

         elif closest_match[prev_compare_shapeid] < matches[compare_shapeid]:
            closest_match.pop(prev_compare_shapeid)
            prev_compare_shapeid = compare_shapeid
            closest_match[prev_compare_shapeid] = matches[compare_shapeid]
               
   print(" original shape " + str(shape_ids[0]) + " closest match shape is " + str( prev_compare_shapeid ) )




print("all_shape_match_results")
print(all_shape_match_results)












