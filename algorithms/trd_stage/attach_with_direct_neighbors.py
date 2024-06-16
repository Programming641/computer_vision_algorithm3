
from libraries import  pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir

directory = "videos/street3/resized/min1"
if len( sys.argv ) >= 2:
   directory = sys.argv[1]

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory  + "shapes/"
all_matches_ddir = top_shapes_dir + directory + "all_matches" + "/data/"

move_shapes_dfile = all_matches_ddir + "move_shapes2.data"
with open (move_shapes_dfile, 'rb') as fp:
   # { filename: [ [ { im1shapeids }, { im2shapeids }, movement ], ... ], ... }
   move_shapes2_data = pickle.load(fp)
fp.close()


move_together_shapes = {}
for each_files in move_shapes2_data:
   print(each_files)
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]
   
   move_together_shapes[each_files] = []

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()     
      

   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   
 

   im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
   im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"

   with open (im1shape_neighbors_file, 'rb') as fp:
      im1shapes_neighbors = pickle.load(fp)
   fp.close()   

   with open (im2shape_neighbors_file, 'rb') as fp:
      im2shapes_neighbors = pickle.load(fp)
   fp.close()   

   # get neighbor shapes that move together
   already_found_shapes = []
   for move_shapes2_datum in move_shapes2_data[each_files]:
      # [ { im1shapeids }, { im2shapeids }, movement ]
   
      cur_im1shapes_neighbors = set()
      for im1shapeid in move_shapes2_datum[0]:
            
         cur_im1shapes_neighbors |= set( im1shapes_neighbors[im1shapeid] )
      
      cur_im2shapes_neighbors = set()
      for im2shapeid in move_shapes2_datum[1]:
            
         cur_im2shapes_neighbors |= set( im2shapes_neighbors[im2shapeid] )
         
      best_movement = ( 100, 100 )
      cur_move_together_shapes = [ move_shapes2_datum ]
      for ano_move_shapes2_datum in move_shapes2_data[each_files]:
         if ano_move_shapes2_datum in already_found_shapes:
            continue
            
         found_im1shp_nbrs = set( ano_move_shapes2_datum[0] ).intersection( cur_im1shapes_neighbors )
         found_im2shp_nbrs = set( ano_move_shapes2_datum[1] ).intersection( cur_im2shapes_neighbors )
            
         if len( found_im1shp_nbrs ) >= 1 and len( found_im2shp_nbrs ) >= 1:
            # move_shapes2_datum and ano_move_shapes2_datum are neighbors
            # check if both move together
               
            distance_x = abs( move_shapes2_datum[2][0] - ano_move_shapes2_datum[2][0] )
            distance_y = abs( move_shapes2_datum[2][1] - ano_move_shapes2_datum[2][1] )
            cur_movement_score = distance_x + distance_y               
               
            if cur_movement_score < 5:
               if cur_movement_score == ( best_movement[0] + best_movement[1] ):
                  already_found_shapes.append( ano_move_shapes2_datum )
                  cur_move_together_shapes.append( ano_move_shapes2_datum )
                  
               elif cur_movement_score < ( best_movement[0] + best_movement[1] ):
                  already_found_shapes.append( ano_move_shapes2_datum )
                  cur_move_together_shapes = [ move_shapes2_datum, ano_move_shapes2_datum ]
                  
                  best_movement = ( distance_x, distance_y )

      if len(cur_move_together_shapes) >= 2:
         move_together_shapes[each_files].append( cur_move_together_shapes )



obj_shapes_dir = top_shapes_dir + directory + "trd_stage/obj_shapes/"
obj_shapes_ddir = obj_shapes_dir + "data/"
if os.path.exists(obj_shapes_ddir ) == False:
   os.makedirs(obj_shapes_ddir )
   
move_shapes3 = obj_shapes_ddir + "objects1.data"
with open(move_shapes3, 'wb') as fp:
   pickle.dump(move_together_shapes, fp)
fp.close()
















