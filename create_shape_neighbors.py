from libraries import read_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions

import os

filename = "nbr_shape2"

directory = ""

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

shape_neighbors_path = 'shapes/' + directory + 'shape_nbrs/'

if not os.path.isdir(shape_neighbors_path):
   os.makedirs(shape_neighbors_path)


shape_neighbor_file = open(shape_neighbors_path + filename + "_shape_nbrs.txt" , "w" )

# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapeIDs_with_all_indexes = read_files_functions.rd_shapes_file(filename, directory)

all_shape_neighbors = []


for src_shape_id in shapeIDs_with_all_indexes:

   print("src_shape_id " + src_shape_id )
   
   cur_shape_neighbors = {}
   
   cur_shape_neighbors[src_shape_id] = []
   
   # boundary_pixels has the following form
   # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, 86{'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
   # containing coordinates of boundary pixels
   src_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(shapeIDs_with_all_indexes[src_shape_id] )

   # comparing every one of shape of the image with every other shapes of the image
   for candidate_shape_id in shapeIDs_with_all_indexes:
      
      if src_shape_id == candidate_shape_id :
         # itself or already processed as src_shape_id
         continue
            
      candidate_pixels = pixel_shapes_functions.get_boundary_pixels(shapeIDs_with_all_indexes[candidate_shape_id] )
         
      # returned value example. {'src': {'x': 33, 'y': 33}, 1: {'x': 33, 'y': 34}, 2: {'x': 34, 'y': 34}}
      matched_neighbor_coords = pixel_shapes_functions.find_direct_neighbors( src_boundary_pixels, candidate_pixels )

      if matched_neighbor_coords:

         cur_shape_neighbors[src_shape_id].append(candidate_shape_id)

   
   print("current neighbors")
   print(cur_shape_neighbors)   
   all_shape_neighbors.append(cur_shape_neighbors)
            
            
            
shape_neighbor_file.write(str( all_shape_neighbors ) )
shape_neighbor_file.close()














