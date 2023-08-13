
from libraries import pixel_shapes_functions, read_files_functions, pixel_functions, image_functions, same_shapes_functions
from libraries.cv_globals import third_smallest_pixc, frth_smallest_pixc

from PIL import Image
import math
import os, sys
import copy


# param_shapes
# list of tuple image1 shape and image2 shape
# [ ( image1 shapeid, image2 shapeid ), ... ]
# tuple can be list also.
# outer list can also be set.
# list of tuple or set of tuple or list of list.
#
# returns verified_shapes
# { ( image1 shapeid, image2 shapeid ), ... }
def verify_matches( param_shapes, im_shapes, im_colors, im_neighbors, im_width, match_nbr_count=0.43 ):

   verified_shapes = set()

   for each_shapes in param_shapes:

         
      # neighbor match counting needs to be done from smaller shape.
      total_neighbors = 0
      
      cur_nbr_match_counter = 0
      matched = False
      matched_im2neighbors = []
      for im1nbr in im_neighbors[0][each_shapes[0]]:
         if len( im_shapes[0][im1nbr] ) < frth_smallest_pixc:
            continue
         
         cur_count_done = False
         for im2nbr in im_neighbors[1][each_shapes[1]]:
         
            if len( im_shapes[1][im2nbr] ) < frth_smallest_pixc or im2nbr in matched_im2neighbors:
               continue
            
            # check if size is too different
            im1shapes_total = len( im_shapes[0][im1nbr] )
            im2shapes_total = len( im_shapes[1][im2nbr] )
      
            im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
            if im1_2pixels_diff != 0:
               if im1shapes_total > im2shapes_total:
                  if im1_2pixels_diff / im2shapes_total > 1:
                     continue
               else:
                  if im1_2pixels_diff / im1shapes_total > 1:
                     continue                
            
            if cur_count_done is False:
               total_neighbors += 1
               cur_count_done = True

            if im_colors[0][im1nbr] != im_colors[1][im2nbr]:
               continue

            # get first element to check if it is (x,y) or pixel index
            if type( list( im_shapes[0][im1nbr] )[0] ) is tuple :
               param_shp_type = 1
            else:
               param_shp_type = 0
            
            # [(12, 15), (11, 15), ... ]
            im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[0][im1nbr], im_width, param_shp_type=param_shp_type )  
            im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[1][im2nbr], im_width, param_shp_type=param_shp_type )
            
            #image_functions.cr_im_from_shapeslist2( "10", "videos/street3/resized/min/", [ im1nbr ] )
            #image_functions.cr_im_from_shapeslist2( "11", "videos/street3/resized/min/", [ im2nbr ] )
            
            
            # match from smaller shape
            if im1shapes_total > im2shapes_total:
               im1_im2_nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy, match_threshold=0.6 )
            else:
               im1_im2_nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy, match_threshold=0.6 )
            if im1_im2_nbr_match is True:     
               
               cur_nbr_match_counter += 1
               matched_im2neighbors.append( im2nbr )


      if total_neighbors < 3:
         continue
      if cur_nbr_match_counter >= 1 and cur_nbr_match_counter / total_neighbors >= match_nbr_count:
         verified_shapes.add( (each_shapes[0], each_shapes[1]) )

   

   return verified_shapes



# remove very small isolated shapes
# param_shapes -> [ [ shapes ], [ shapes ] ]
def rm_vsmall_isolated_shapes( param_shapes, im_shapes, im_boundaries, im_shape_by_pindex, im_size ):
   
   result_shapes = []
   
   def _rm_vsmall_isolated_shapes( _param_shapes, _im_shapes, _im_boundaries, _im_shape_by_pindex ):
      
      _result_shapes = []
      
      biggest_shape_len = max( [ len( _im_shapes[ temp_shape ] ) for temp_shape in _param_shapes ] )
      
      biggest_shapes = [ temp_shape for temp_shape in _param_shapes if len( _im_shapes[ temp_shape ] ) == biggest_shape_len ]
      _result_shapes.extend( biggest_shapes )
      
      for each_shape in _param_shapes:
         # {(231, 63), (244, 82), ... }
         vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( _im_boundaries[ each_shape ], 3, im_size, param_shp_type=1 )         
      
         vicinity_shapes = set()
         # convert xy to pixel indexes
         for pixel in vicinity_pixels:
            pixel_index = pixel_functions.convert_xy_to_pindex( pixel, im_size[0] )
               
            vicinity_shapes.add( _im_shape_by_pindex[ str(pixel_index) ] )      
      
         
         for temp_shape in _param_shapes:
            if temp_shape != each_shape and temp_shape in vicinity_shapes:
               
               if biggest_shape_len / 25 < len( _im_shapes[ temp_shape ] ):
                  _result_shapes.append( each_shape )

                  break
      
      
      return _result_shapes




   if len( param_shapes[0] ) > 1:
      _results = _rm_vsmall_isolated_shapes( param_shapes[0], im_shapes[0], im_boundaries[0], im_shape_by_pindex[0] )

      result_shapes.append( _results )
         
      
   else:
      result_shapes.append( param_shapes[0] )
   
   if len( param_shapes[1] ) > 1:
      _results = _rm_vsmall_isolated_shapes( param_shapes[1], im_shapes[1], im_boundaries[1], im_shape_by_pindex[1] )

      result_shapes.append( _results )
   
   else:
      result_shapes.append( param_shapes[1] )


   return result_shapes
































