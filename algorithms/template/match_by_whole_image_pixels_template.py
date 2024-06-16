
from PIL import Image
import re, pickle
import math
import shutil

import os, sys
from libraries.cv_globals import top_shapes_dir, top_images_dir, internal
from libraries import cv_globals, image_functions, pixel_shapes_functions, pixel_functions, same_shapes_functions



directory = "videos/street3/resized/min1"
im1file = "26"
im2file = "27"
shapes_type = "intnl_spixcShp"


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]

   directory = sys.argv[3]

   print("execute script template/match_by_whole_image_pixels_template.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )




# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

shapes_dir = top_shapes_dir + directory  + "shapes/" 

shapes_dfile = shapes_dir + im1file + "shapes.data"
with open (shapes_dfile, 'rb') as fp:
   # { '79999': ['79999', ... ], ... }
   # { 'shapeid': [ pixel indexes ], ... }
   im1shapes = pickle.load(fp)
fp.close()
im2shapes_dfile = shapes_dir + im2file + "shapes.data"
with open (im2shapes_dfile, 'rb') as fp:
   # { '79999': ['79999', ... ], ... }
   # { 'shapeid': [ pixel indexes ], ... }
   im2shapes = pickle.load(fp)
fp.close()   

im1shapes_neighbors_path = shapes_dir + "shape_nbrs/" + im1file + "_shape_nbrs.data"
im2shapes_neighbors_path = shapes_dir + "shape_nbrs/" + im2file + "_shape_nbrs.data"

# it takes so much time to see what shape contains the specific pixel, we prepare pixel and shapeid pair.
# { pixel: shapeid, pixel: shapeid, ... }
shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'
shp_by_index_dfile2 = shp_by_index_dir + im2file + ".data"
with open (shp_by_index_dfile2, 'rb') as fp:
   # { pindex: { shapeids }, ... }
   im2shapeids_by_pindex = pickle.load(fp)
fp.close()

original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

third_smallest_pixc = cv_globals.get_third_smallest_pixc( original_image.size )

def check_shape_size( param_im1shapeid, param_im2shapeid, param_shapes, param_ano_shapes, size_threshold=1 ):
   # check if size is too different
   im1shapes_total = len( param_shapes[param_im1shapeid] )
   im2shapes_total = len( param_ano_shapes[param_im2shapeid] )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_threshold:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > size_threshold:
            return True

   return False      



# target_notfnd_shapes 
# [ connected not found shapes, im_shapes_colors, im_shapes ]
# 
# directly_UD is directly up or down. if it is true, it goes directly up or down with left or right value 0.
def move_pixels( target_image_data, move_direction, directly_UD, step, move_total, non_t_image_data, target_im_shapes, 
                 target_im_shapes_nbrs, non_t_im_shape_by_pindex, best_match_t_im_conn_shapes=None, best_m_btwn_im_conn_shapes=None ):

   def get_connected_shapes( _shape, get_from_shapes, param_shapes_neighbors, connected_shapes=None ):
      
      initial_shape = None
      if connected_shapes is None:
         connected_shapes = set()
         connected_shapes.add( _shape )
         
         initial_shape =  _shape
      
      cur_shape_neighbors = set( param_shapes_neighbors[ _shape ] ).intersection( get_from_shapes )
      if len( cur_shape_neighbors ) >= 1:
         
         for cur_shape_neighbor in cur_shape_neighbors:
            if cur_shape_neighbor in connected_shapes:
               continue
            connected_shapes.add( cur_shape_neighbor )
            get_connected_shapes( cur_shape_neighbor, get_from_shapes, param_shapes_neighbors, connected_shapes )
      
      if initial_shape is not None:
         return connected_shapes
      
   
   
   
   if best_match_t_im_conn_shapes is not None:
      best_t_im_conn_shapes = best_match_t_im_conn_shapes
      best_btwn_im_conn_shapes = best_m_btwn_im_conn_shapes
   else:
      best_t_im_conn_shapes = []
      best_btwn_im_conn_shapes = []

   for move_LR in range( 0, move_total, step ):

      if directly_UD is False and move_LR == 0:
         continue

      move_x = None
      if "left" in move_direction.lower():
         # subtract from x
         if move_LR != 0:
            move_x = move_LR * -1
         else:
            move_x = 0
      
      elif "right" in move_direction.lower():
         # add to x
         if move_LR != 0:
            move_x = move_LR
         else:
            move_x = 0
         
      
      for move_UD in range( 0, move_total, step ):
         move_y = None
         
         if "up" in move_direction.lower():
            # subtract from y
            if move_UD != 0:
               move_y = move_UD * -1
            else:
               move_y = 0
         
         elif "down" in move_direction.lower():
            # add to y
            if move_UD != 0:
               move_y = move_UD
            else:
               move_y = 0


         matched_pixels = set()
         for y in range( 0, im1height ):
            for x in range( 0, im1width ):
               
               pindex = pixel_functions.convert_xy_to_pindex( (x,y), im1width )
               original_pixel_color = target_image_data[ pindex ]
               
               moved_xy = ( x + move_x, y + move_y )
               # check if pixel is out of the image
               if moved_xy[0] < 0 or moved_xy[0] >= im1width or moved_xy[1] < 0 or moved_xy[1] >= im1height:
                  continue

               moved_pindex = pixel_functions.convert_xy_to_pindex( moved_xy, im1width )
               
               if min_colors is True:
                  if original_pixel_color == non_t_image_data[ moved_pindex ]:
                     matched_pixels.add(pindex)
               
               else:
                  appear_diff = pixel_functions.compute_appearance_difference(original_pixel_color, non_t_image_data[ moved_pindex ] )
                  if appear_diff is False:
                     # same appearance
                     matched_pixels.add(pindex)                  

         
         cur_t_matched_shapes = set()
         matched_im_shapes = set()
         for target_im_shapeid in target_im_shapes:
            if len( target_im_shapes[ target_im_shapeid ] ) < third_smallest_pixc:
               continue
            
            matched_t_shape_pixels = set( target_im_shapes[ target_im_shapeid ] ).intersection( matched_pixels )
            if len( matched_t_shape_pixels ) / len( target_im_shapes[ target_im_shapeid ] ) >= 0.55:
               cur_t_matched_shapes.add( target_im_shapeid )
               
               non_t_shapes = {}
               for matched_pixel in matched_t_shape_pixels:
                  
                  for cur_non_t_shapeid in non_t_im_shape_by_pindex[ matched_pixel ]:

                     if cur_non_t_shapeid not in non_t_shapes.keys():
                        non_t_shapes[ cur_non_t_shapeid ] = 1
                     else:
                        non_t_shapes[ cur_non_t_shapeid ] += 1
               
               highest_matched_count = max( non_t_shapes.values() )
               highest_m_non_t_im_shapes = [ temp_shapeid for temp_shapeid, matched_count in non_t_shapes.items() if matched_count == highest_matched_count ]
               if len( highest_m_non_t_im_shapes ) >= 1:
                  for non_t_im_shape in highest_m_non_t_im_shapes:
                     matched_im_shapes.add( ( target_im_shapeid, non_t_im_shape ) )
         
         
         # get all matched connected target shapes
         done_shapes = set()
         all_connected_shapes = []
         btwn_im_all_conn_shapes = []
         for cur_t_matched_shape in cur_t_matched_shapes:
            if cur_t_matched_shape in done_shapes:
               continue
               
            connected_shapes = get_connected_shapes( cur_t_matched_shape, cur_t_matched_shapes, target_im_shapes_nbrs )
            
            all_connected_shapes.append( connected_shapes )
            done_shapes |= connected_shapes
            
            matched_shapes = set()
            for conn_shapeid in connected_shapes:
               matched_nont_shapeids = [ temp_shapes[1] for temp_shapes in matched_im_shapes if temp_shapes[0] == conn_shapeid ]
               if len( matched_nont_shapeids ) == 1:
                  for matched_nont_shapeid in matched_nont_shapeids:
                     matched_shapes.add( ( conn_shapeid, matched_nont_shapeid ) )

            
            btwn_im_all_conn_shapes.append( [ connected_shapes, matched_shapes ] )

         if len( best_t_im_conn_shapes ) == 0:
            best_t_im_conn_shapes = all_connected_shapes
            best_btwn_im_conn_shapes = btwn_im_all_conn_shapes
         
         else:

            for each_connected_shapes in all_connected_shapes:
               for each_best_t_im_conn_shapes in best_t_im_conn_shapes:
                  
                  common_shapes = each_connected_shapes.intersection( each_best_t_im_conn_shapes )
                  if len( common_shapes ) >= 1:
                     
                     if len( each_connected_shapes ) > len( each_best_t_im_conn_shapes ):
                        best_t_im_conn_shapes.remove( each_best_t_im_conn_shapes )
                        best_t_im_conn_shapes.append( each_connected_shapes )
                        
                        delete_index = None
                        for index, each_best_btwn_conn_shapes in enumerate( best_btwn_im_conn_shapes ):
                           if each_best_t_im_conn_shapes == each_best_btwn_conn_shapes[0]:
                              delete_index = index
                              break
                        
                        best_btwn_im_conn_shapes.pop( delete_index )
                        
                        add_index = None
                        for index, each_btwn_im_all_conn_shapes in enumerate(btwn_im_all_conn_shapes):
                           if each_connected_shapes == each_btwn_im_all_conn_shapes[0]:
                              add_index = index
                              break
                        
                        best_btwn_im_conn_shapes.append( btwn_im_all_conn_shapes[add_index] )  


   return best_t_im_conn_shapes, best_btwn_im_conn_shapes


if "min" in directory:
   min_colors = True
else:
   min_colors = False

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors( im1file, directory, min_colors=min_colors )
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors( im2file, directory, min_colors=min_colors )

with open (im1shapes_neighbors_path, 'rb') as fp:
   im1shapes_nbrs = pickle.load(fp)
fp.close()   

with open (im2shapes_neighbors_path, 'rb') as fp:
   im2shapes_nbrs = pickle.load(fp)
fp.close()   


im1 = Image.open(top_images_dir + directory + im1file + ".png" )
im1pxls = im1.getdata()
im1width, im1height = im1.size

im2 = Image.open(top_images_dir + directory + im2file + ".png" )
im2pxls = im2.getdata()
im2width, im2height = im2.size


LeftUp_matched_shapes, btwn_im_matched_shapes  = move_pixels( im1pxls, "leftUp", True, 2, 15, im2pxls, im1shapes, im1shapes_nbrs, im2shapeids_by_pindex )
print("leftUp finished")
RightUp_matched_shapes, btwn_im_matched_shapes = move_pixels( im1pxls, "leftdown",  False, 2, 15, im2pxls, im1shapes, im1shapes_nbrs, 
                         im2shapeids_by_pindex,  best_match_t_im_conn_shapes=LeftUp_matched_shapes, best_m_btwn_im_conn_shapes=btwn_im_matched_shapes )
print("rightup finished")                         
LeftDown_matched_shapes, btwn_im_matched_shapes = move_pixels( im1pxls, "rightup", True, 2, 15, im2pxls, im1shapes, im1shapes_nbrs,
                         im2shapeids_by_pindex, best_match_t_im_conn_shapes=RightUp_matched_shapes, best_m_btwn_im_conn_shapes=btwn_im_matched_shapes  )
print("leftdown finished")
RightDown_matched_shapes, btwn_im_matched_shapes = move_pixels( im1pxls, "rightdown", False, 2, 15, im2pxls, im1shapes, im1shapes_nbrs,
                         im2shapeids_by_pindex, best_match_t_im_conn_shapes=LeftDown_matched_shapes, best_m_btwn_im_conn_shapes=btwn_im_matched_shapes )

final_matched_shapes = set()
for each_im_matched_shapes in btwn_im_matched_shapes:
   # [ [ {'20275', '39325', ... }, {('29076', '79999'), ('64380', '79999'), ... }], ... ]
   for each_shapes in each_im_matched_shapes[1]:
      # ('64380', '79999')

      bigger_nbr_count = smaller_nbr_count = None
      if len( im1shapes_nbrs[ each_shapes[0] ] ) > len( im2shapes_nbrs[ each_shapes[1] ] ):
         bigger_nbr_count = len( im1shapes_nbrs[ each_shapes[0] ] )
         smaller_nbr_count = len( im2shapes_nbrs[ each_shapes[1] ] )
            
      else:
         bigger_nbr_count = len( im2shapes_nbrs[ each_shapes[1] ] )
         smaller_nbr_count = len( im1shapes_nbrs[ each_shapes[0] ] )
            
      if smaller_nbr_count / bigger_nbr_count < 0.55:
         # neighbor count is not matched
         continue


      nbr_matched_count = 0
      # neighbor matches
      for target_im_nbr in im1shapes_nbrs[ each_shapes[0] ]:
         for search_im_nbr in im2shapes_nbrs[ each_shapes[1] ]:     
            size_diff = check_shape_size( target_im_nbr, search_im_nbr, im1shapes, im2shapes, size_threshold=1 )
            if size_diff is True:
               continue            
            
            if min_colors is True:
               if im1shapes_colors[ target_im_nbr ] != im2shapes_colors[ search_im_nbr ]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(im1shapes_colors[ target_im_nbr ], im2shapes_colors[ search_im_nbr ] )
               if appear_diff is True:
                  # different appearance
                  continue            
            
            im1nbr_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[target_im_nbr], im1width, param_shp_type=0 )  
            im2nbr_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[search_im_nbr], im1width, param_shp_type=0 )  
                     
            # matching from smaller shape.
            if len( im1shapes[ target_im_nbr ] ) > len( im2shapes[ search_im_nbr ] ):
               im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2nbr_shp_coord_xy, im1nbr_shp_coord_xy, match_threshold=0.45 )
            else:
               im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1nbr_shp_coord_xy, im2nbr_shp_coord_xy, match_threshold=0.45 )

            if im1im2nbr_match is True:                  
               nbr_matched_count += 1
               break               

      if nbr_matched_count > 0 and nbr_matched_count / smaller_nbr_count >= 0.35:
         final_matched_shapes.add( each_shapes )
      
      


template_dir = top_shapes_dir + directory + "template/"
image_template_dir = template_dir + "image_pixels/"

image_template_ddir = image_template_dir + "data/"

if os.path.exists(template_dir ) == False:
   os.makedirs(template_dir )
if os.path.exists(image_template_dir ) == False:
   os.makedirs(image_template_dir )
if os.path.exists(image_template_ddir ) == False:
   os.makedirs(image_template_ddir )


image_template_dfile = image_template_ddir + im1file + "." + im2file + ".data"
with open(image_template_dfile, 'wb') as fp:
   pickle.dump(final_matched_shapes, fp)
fp.close()



























