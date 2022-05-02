from libraries import read_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions

import os, sys
from libraries.cv_globals import proj_dir

shapes_dir = proj_dir + "/shapes/"

im_file = "1clrgrp"

directory = "videos/street"

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

shape_locations_path = shapes_dir + directory + "locations/" + im_file + "_loc.txt"
shape_neighbors_path = shapes_dir + directory + 'shape_nbrs/'

if not os.path.isdir(shape_neighbors_path):
   os.makedirs(shape_neighbors_path)


s_locations = read_files_functions.rd_ldict_k_v_l( im_file, directory, shape_locations_path )


shape_neighbor_file = open(shape_neighbors_path + im_file + "_shape_nbrs.txt" , "w" )

# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes = read_files_functions.rd_shapes_file(im_file, directory)

all_shape_neighbors = []

shapes_in_im_areas = {}
for shapeid in shapes:
   
   for s_locs in s_locations:
      if shapeid in s_locs.keys():
         shapes_in_im_areas[shapeid] = s_locs[ list(s_locs.keys())[0] ]
         break

all_shapes = len(shapes)
for src_shapeid in shapes:

   print("src_shapeid " + src_shapeid + " " +  str(all_shapes) + " remaining" )
   
   cur_shape_neighbors = {}
   
   cur_shape_neighbors[src_shapeid] = []
   
   
   # boundary_pixels has the following form
   # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, 86{'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
   # containing coordinates of boundary pixels
   src_boundary_pixels = pixel_shapes_functions.get_boundary_pixels(shapes[src_shapeid] )

   # comparing every one of shape of the image with every other shapes of the image
   for candidate_shapeid in shapes:
      
      if src_shapeid == candidate_shapeid :
         # itself or already processed as src_shapeid
         continue
      
      same_im_area = False
      for src_s_loc in shapes_in_im_areas[src_shapeid]:
         if src_s_loc in shapes_in_im_areas[candidate_shapeid]:
            same_im_area = True
      
      if not same_im_area:
         continue
      
      candidate_pixels = pixel_shapes_functions.get_boundary_pixels(shapes[candidate_shapeid] )
         
      # returned value example. {'src': {'x': 33, 'y': 33}, 1: {'x': 33, 'y': 34}, 2: {'x': 34, 'y': 34}}
      matched_neighbor_coords = pixel_shapes_functions.find_direct_neighbors( src_boundary_pixels, candidate_pixels )

      if matched_neighbor_coords:

         cur_shape_neighbors[src_shapeid].append(candidate_shapeid)

 
   all_shape_neighbors.append(cur_shape_neighbors)
   
   all_shapes -= 1
            
            
            
shape_neighbor_file.write(str( all_shape_neighbors ) )
shape_neighbor_file.close()














