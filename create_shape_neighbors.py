from libraries import read_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions

import os, sys
from libraries.cv_globals import proj_dir
import winsound

top_shapes_dir = proj_dir + "/shapes/"

im_file = "1clrgrp"

directory = "videos/street"

if sys.argv:
   im_file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   
   location_fname = im_file + "_loc.txt"

   directory = sys.argv[1]

   print("execute script create_shape_neighbors.py. filename " + im_file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

shape_locations_path = top_shapes_dir + directory + "locations/" + im_file + "_loc.txt"
shape_neighbors_path = top_shapes_dir + directory + 'shape_nbrs/'

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

shapes_boundaries = {}
# get boundary pixels of all shapes
for shapeid in shapes:
   shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels(shapes[shapeid] )



all_shapes = len(shapes)
for src_shapeid in shapes:

   if all_shapes % 100 == 0:
      print("src_shapeid " + src_shapeid + " " +  str(all_shapes) + " remaining" )
   
   
   cur_shape_neighbors = {}
   
   cur_shape_neighbors[src_shapeid] = []
   

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
      

      # returned value example. {'src': {'x': 33, 'y': 33}, 1: {'x': 33, 'y': 34}, 2: {'x': 34, 'y': 34}}
      matched_neighbor_coords = pixel_shapes_functions.find_direct_neighbors( shapes_boundaries[src_shapeid] , shapes_boundaries[candidate_shapeid] )



      if matched_neighbor_coords:

         cur_shape_neighbors[src_shapeid].append(candidate_shapeid)


   if not cur_shape_neighbors[src_shapeid]:
      print("ERROR. current shape " + src_shapeid + " could not find neighbors")
      sys.exit()
      
   all_shape_neighbors.append(cur_shape_neighbors)
   
   all_shapes -= 1
            
            
            
shape_neighbor_file.write(str( all_shape_neighbors ) )
shape_neighbor_file.close()


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)













