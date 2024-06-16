
from libraries import pixel_shapes_functions, pixel_functions, image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir
from libraries import cv_globals

from PIL import Image
import math
import os, sys
import copy
from collections import Counter
import time



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


# return True if size is too different, False if size is similar within threshold
def check_size_by_pixels( param_im1pixels, param_im2pixels, size_threshold=1, im_size=None  ):
   # check if size is too different
   im1shapes_total = len( param_im1pixels )
   im2shapes_total = len( param_im2pixels )
   
   im_pixels_size_factor = 1
   im_pixels_size_multiplier = 80
   # if im_size is provided, then this is a request to include the shape size in the calculation
   if im_size is not None:
      all_im_pixels_len = im_size[0] * im_size[1]
      im_pixels_average = ( im1shapes_total + im2shapes_total ) / 2
      # how many of im_pixels_average are there to fill the whole image?
      param_pix_need_to_fill = all_im_pixels_len / im_pixels_average
      # smaller the im_pixels_average is, the more is needed to fill the whole image.
      # bigger the im_pixels_average is, the size difference calculation should be more strict
      # the largest would result in 1. closer to 1, size calculation should be more strict
      im_pixels_size_factor = ( 1 / param_pix_need_to_fill ) * im_pixels_size_multiplier
      
      # the small enough pixels should be calculated only with this equation ( im1_2pixels_diff / im2shapes_total ).
      if im_pixels_size_factor < 1:
         im_pixels_size_factor = 1
      
   diff_value = None
   
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         diff_value = ( im1_2pixels_diff / im2shapes_total ) * im_pixels_size_factor
      else:
         diff_value = ( im1_2pixels_diff / im1shapes_total ) * im_pixels_size_factor
      
      if diff_value > size_threshold:
         return True

   return False      


# size is different more than threshold -> returns True. False otherwise.
def size_diff_by_percent( pixels1, pixels2, threshold=0.5 ):

   if len(pixels1) > len(pixels2):
      bigger_pixels = pixels1
      smaller_pixels = pixels2
   else:
      bigger_pixels = pixels2
      smaller_pixels = pixels1
      
   if len(smaller_pixels) / len(bigger_pixels) < threshold:
      return True
   else:
      return False




# target_im_shapes -> {'5588': [(128, 128, 128), (10, 13), (10, 12), ... }
#                     { shapeid: [ shape color , (x,y), (x,y), ... ], ... }
# ano_im_shapes same as target_im_shapes
# 
# above data form is the one that returned by pixel_shapes_functions.get_shapes_pos_in_shp_coord
def find_shapes_match( target_im_shapes, ano_im_shapes, shapeid ):
      match = [ [], [] ]
      
      # first check if image1 total pixel amount is too different from image2 total pixels
      im1shapes_total = 0
      for im1shapeid in target_im_shapes:
         im1shapes_total += len( target_im_shapes[im1shapeid] ) - 1
      im2shapes_total = 0
      for im2shapeid in ano_im_shapes:
         im2shapes_total += len( ano_im_shapes[im2shapeid] ) - 1      
      
      im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > 1:
            return None
      else:
         if im1_2pixels_diff / im1shapes_total > 1:
            return None
      
      
      im_total_match_count = 0
      for t_im_shape in target_im_shapes:
         cur_highest_match_count = 0
         
         cur_im_s_color = target_im_shapes[t_im_shape].pop(0)
         cur_im_s_pixels = set( target_im_shapes[t_im_shape] )
         

         for ano_im_shape in ano_im_shapes:
            ano_im_s_color = ano_im_shapes[ano_im_shape].pop(0)
            got_ano_im_clr = True
            
            ano_im_s_pixels = set( ano_im_shapes[ano_im_shape] )

            if cur_im_s_color == ano_im_s_color:            

              matched_pixels = cur_im_s_pixels.intersection( ano_im_s_pixels )
              cur_t_s_match_count = len( matched_pixels )
             
              # check if current image1shape and current image2 matched. if so, take their pixels and their matched pixels count
              if cur_t_s_match_count > 0 and cur_t_s_match_count / len( target_im_shapes[t_im_shape] ) >= 0.4:
                 if cur_t_s_match_count > cur_highest_match_count:
                    cur_highest_match_count = cur_t_s_match_count
                    
                    print("image1 " + t_im_shape + " image2 " + ano_im_shape + " matched" )
         
            ano_im_shapes[ano_im_shape].insert(0, ano_im_s_color )
            
         # at the end of current image1 shape
         im_total_match_count += cur_highest_match_count
         
         target_im_shapes[t_im_shape].insert( 0, cur_im_s_color )
               


      if im_total_match_count / im1shapes_total > 0.6:
         # match found
         match[0].extend( list(target_im_shapes.keys()) )
         match[1].extend( list(ano_im_shapes.keys()) )


      return match




# find shapes match by each shape's location
#
# 
# target_im_shapes -> {'2876': [(76, 7), (75, 7), ... }
#                     { shapeid: [ (x,y), (x,y), ... ], ... }
# ano_im_shapes same as target_im_shapes
# 
# above data form is the one that returned by pixel_shapes_functions.get_shapes_pos_in_shp_coord
def find_match_by_eachShp_loc( target_im_shapes, ano_im_shapes, im1_2colors, image_width, check_both_sides=False ):
      match = [ [], [] ]
      
      # first check if image1 total pixel amount is too different from image2 total pixels
      im1shapes_total = 0
      for im1shapeid in target_im_shapes:
         im1shapes_total += len( target_im_shapes[im1shapeid] ) - 1
      im2shapes_total = 0
      for im2shapeid in ano_im_shapes:
         im2shapes_total += len( ano_im_shapes[im2shapeid] ) - 1      
      
      im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > 1:
            return None, None
      else:
         if im1_2pixels_diff / im1shapes_total > 1:
            return None, None
      
      # im1shp_in_each_shp_coord -> {'2876': [(191, 191, 191), (11, 7), ... }
      im1shp_in_each_shp_coord = {}
      for im1shapeid in target_im_shapes:        
         im1shape_in_shp_coord, im1smallest_xy = pixel_shapes_functions.get_shapes_pos_in_shp_coord( { im1shapeid: target_im_shapes[im1shapeid] }, 
                                                 image_width, im1_2colors[0], param_shp_type=1 )
         im1shp_in_each_shp_coord[im1shapeid] = im1shape_in_shp_coord[im1shapeid]
      

      im2shp_in_each_shp_coord = {}
      for im2shapeid in ano_im_shapes:
         im2shape_in_shp_coord, im2smallest_xy = pixel_shapes_functions.get_shapes_pos_in_shp_coord( { im2shapeid: ano_im_shapes[im2shapeid] }, 
                                                 image_width, im1_2colors[1], param_shp_type=1 )
         im2shp_in_each_shp_coord[im2shapeid] = im2shape_in_shp_coord[im2shapeid]      
      
      
      im_total_match_count = 0
      for t_im_shape in im1shp_in_each_shp_coord:
         cur_highest_match_count = 0
         
         cur_im_s_color = im1shp_in_each_shp_coord[t_im_shape].pop(0)
         cur_im_s_pixels = set( im1shp_in_each_shp_coord[t_im_shape] )
         

         for ano_im_shape in im2shp_in_each_shp_coord:
            ano_im_s_color = im2shp_in_each_shp_coord[ano_im_shape].pop(0)
            got_ano_im_clr = True
            
            ano_im_s_pixels = set( im2shp_in_each_shp_coord[ano_im_shape] )

            if cur_im_s_color == ano_im_s_color:            

               matched_pixels = cur_im_s_pixels.intersection( ano_im_s_pixels )
               cur_t_s_match_count = len( matched_pixels )
             
               if check_both_sides is False:
                  # check if current image1shape and current image2 matched. if so, take their pixels and their matched pixels count
                  if cur_t_s_match_count > 0 and cur_t_s_match_count / len( im1shp_in_each_shp_coord[t_im_shape] ) >= 0.4:
                     if cur_t_s_match_count > cur_highest_match_count:
                        cur_highest_match_count = cur_t_s_match_count

               else:
                  # check if current image1shape and current image2 matched. if so, take their pixels and their matched pixels count
                  if cur_t_s_match_count > 0 and cur_t_s_match_count / len( im1shp_in_each_shp_coord[t_im_shape] ) >= 0.4 and \
                     cur_t_s_match_count / len( im2shp_in_each_shp_coord[ano_im_shape] ) >= 0.4:
                     if cur_t_s_match_count > cur_highest_match_count:
                        cur_highest_match_count = cur_t_s_match_count                  
         
            im2shp_in_each_shp_coord[ano_im_shape].insert(0, ano_im_s_color )
            
         # at the end of current image1 shape
         im_total_match_count += cur_highest_match_count
         
         im1shp_in_each_shp_coord[t_im_shape].insert( 0, cur_im_s_color )
               


      if im_total_match_count / im1shapes_total > 0.6:
         # match found
         match[0].extend( list(im1shp_in_each_shp_coord.keys()) )
         match[1].extend( list(im2shp_in_each_shp_coord.keys()) )


      return match, im_total_match_count



#                            algorithms
#
# the shapes given to this function are located at top left.
# get rightmost pixel of both shapes. get the one that has the greater rightmost pixel
# get bottom pixel of both shapes. get the one that has the greater bottom pixel.
# 
# example. shape1 rightmost pixel 20.  shape2 rightmost pixel 30
# move shape1 to pixel up to 30
# shape1 bottom pixel 50.  shape2 bottom 40
# move shape2 up to 50
#
# first move
# move shape2 up to 50
# second move
# move shape1 2 pixels to the right. move shape2 up to 50
# third move
# move shape1 2 pixels to the right. move shape2 up to 50
# do this until shape1 rightmost pixel gets to 30.
#
#                        parameters
# im1pixels and im2pixels have the following form
# [(12, 15), (11, 15), ... ].   [ (x,y), (x,y), ... ]
def match_shape_while_moving_it( im1pixels, im2pixels, match_threshold=0.5, return_matched_pix=False):

   # get image1 and image2 rightmost pixel
   im1_Rmost_x = max( [ xy[0] for xy in im1pixels ] )
   im2_Rmost_x = max( [ xy[0] for xy in im2pixels ] )
   
   im1_bottom_y = max( [ xy[1] for xy in im1pixels ] )
   im2_bottom_y = max( [ xy[1] for xy in im2pixels ] )
   
   Rmost_x = None
   bottom_y = None

   if im1_Rmost_x >= im2_Rmost_x:
      Rmost_x = im1_Rmost_x - im2_Rmost_x
   else:
      Rmost_x = im2_Rmost_x - im1_Rmost_x
   
   if im1_bottom_y >= im2_bottom_y:
      bottom_y = im1_bottom_y - im2_bottom_y
   else:
      bottom_y = im2_bottom_y - im1_bottom_y
   
   # do at least one time.
   if Rmost_x < 2:
      Rmost_x = 2
   if bottom_y < 2:
      bottom_y = 2

   
   for move_right in range( 0, Rmost_x, 2 ):
      cur_im1pixels = None
      cur_im2pixels = None
      if im1_Rmost_x >= im2_Rmost_x:
         # move image2 shape to the right
         cur_im2pixels = [ ( xy[0] + move_right, xy[1] ) for xy in im2pixels ]
         cur_im1pixels = copy.deepcopy( im1pixels )
      else:
         cur_im1pixels = [ ( xy[0] + move_right, xy[1] ) for xy in im1pixels ]
         cur_im2pixels = copy.deepcopy( im2pixels )
      
      for move_down in range( 0, bottom_y, 2 ):
         
         if im1_bottom_y >= im2_bottom_y:
            cur_im2pixels = [ ( xy[0], xy[1] + move_down ) for xy in cur_im2pixels ]
         else:
            cur_im1pixels = [ ( xy[0], xy[1] + move_down ) for xy in cur_im1pixels ]
   
         # finished moving shapes. right now, shapes are in the right location to be compared
         found_pixels = set( cur_im1pixels ).intersection( set( cur_im2pixels ) )

         #input_im = "shapes/videos/street6/resized/min/temp/test.png"
         #image_functions.cr_im_from_pixels( "1", "videos/street6/resized/min/", cur_im1pixels, pixels_rgb=(0,255,0), input_im=input_im )
         #image_functions.cr_im_from_pixels( "2", "videos/street6/resized/min/", cur_im2pixels, pixels_rgb=(0,0,255), input_im=input_im )
         
         if len( found_pixels ) / len( cur_im1pixels ) >= match_threshold:

            if return_matched_pix is True:
               return ( True, found_pixels )
            else:
               return True
   
   # if the processing gets here, the found_pixels never reached match threshold value
   if return_matched_pix is True:
      return ( False, set() )
   else:
      return False



# im1pixels and im2pixels form
# { pixel index: pixel color } data types-> pixel index: int. pixel color ( r,g,b ). r, g, and b are int.
# im1pixels and im2pixels are NOT the shape coordinate pixels.
#
# # best_match means to not stop after finding the match at match_threshold but continue doing it and return the result of best match
def match_shape_while_moving_it2( im1pixels, im2pixels, im_size, min_colors, match_threshold=0.5, best_match=False, ignore_colors=False ):

   def reset_skip( skip_xy, cur_row_or_column ):
      if "pos" in cur_row_or_column:
         reset_value = 20
      elif "neg" in cur_row_or_column:
         reset_value = -20
      
      skip_xy[cur_row_or_column] = reset_value


   # im2pixels is the fixed pixels and im1pixels move.
   # if im1pixels move beyond max x or y of im2pixels, then there will be no pixels. so skip them
   fixed_max_x = fixed_max_y = 0
   fixed_min_x = im_size[0] - 1
   fixed_min_y = im_size[1] - 1
   threshold_pixels_len = len( im1pixels ) * match_threshold
   
   for pindex in im2pixels.keys():
      xy = pixel_functions.convert_pindex_to_xy( pindex, im_size[0] )
      
      if xy[0] > fixed_max_x:
         fixed_max_x = xy[0]
      if xy[0] < fixed_min_x:
         fixed_min_x = xy[0]
      if xy[1] > fixed_max_y:
         fixed_max_y = xy[1]
      if xy[1] < fixed_min_y:
         fixed_min_y = xy[1]

   #print("fixed_min_x " + str(fixed_min_x) + " fixed_max_x " + str(fixed_max_x) + " fixed_min_y " + str(fixed_min_y) + " fixed_max_y " + str(fixed_max_y) )
   
   save_filepath = top_shapes_dir + "videos/street3/resized/min1/temp/test1.png"
   #image_functions.cr_im_from_pixels( "27", "videos/street3/resized/min1/", im2pixels.keys(), pixels_rgb=(0,0,255), save_filepath=save_filepath ) 
   #image_functions.cr_im_from_pixels( "27", "videos/street3/resized/min1/", { (fixed_max_x, fixed_max_y), (fixed_min_x, fixed_min_y) } , pixels_rgb=(50,200,200), input_im=save_filepath ) 
   
   best_match_movement_values = None
   
   best_match_pixels = set()
   
   start_move = 0
   step_move = 1
   end_move = 20
   negative_start_move = -1
   # first one is for right and down. second tuple is for left and up.
   movements = [ ( start_move, end_move, step_move ), ( negative_start_move, -end_move, -step_move ) ]
   
   skip_xy = { "pos_x": 21, "neg_x": -21, "pos_y": 21, "neg_y": -21 }
   skip_beyond_lookup = { "max_x": "pos_x", "min_x": "neg_x", "max_y": "pos_y", "min_y": "neg_y" }
   for movement in movements:

      for left_right in range( movement[0], movement[1], movement[2] ):
         if left_right >= start_move and left_right > skip_xy["pos_x"]:
            # for the current movement, all threshold value of pixels are beyond fixed im2pixels
            if left_right == end_move:
               reset_skip( skip_xy, "pos_x" )
            break
         elif left_right < start_move and left_right < skip_xy["neg_x"]:
            if left_right == -end_move:
               reset_skip( skip_xy, "neg_x" )
            break
         
         for movement in movements:
            for down_up in range( movement[0], movement[1], movement[2] ):
               if down_up >= start_move and down_up > skip_xy["pos_y"]:
                  # skip up to the current end of pos_y for the current x
                  if down_up == end_move:
                     reset_skip( skip_xy, "pos_y" )
                  break
               elif down_up < start_move and down_up < skip_xy["neg_y"]:
                  if down_up == -end_move:
                     reset_skip( skip_xy, "neg_y" )
                  break

               # { index: pixel color, ... }
               moved_im1pixels = {}
               beyond_fixed_xy = { "max_x": 0, "min_x": 0, "max_y": 0, "min_y": 0 }
               for im1pindex in im1pixels:
                  xy = pixel_functions.convert_pindex_to_xy( im1pindex, im_size[0] )
                  moved_x = xy[0] + left_right
                  moved_y = xy[1] + down_up
                  
                  if moved_x > fixed_max_x:
                     beyond_fixed_xy["max_x"] += 1
                  if moved_y > fixed_max_y:
                     beyond_fixed_xy["max_y"] += 1
                  if moved_x < fixed_min_x:
                     beyond_fixed_xy["min_x"] += 1
                  if moved_y < fixed_min_y:
                     beyond_fixed_xy["min_y"] += 1

                  if moved_x < 0 or moved_x >= im_size[0] or moved_y < 0 or moved_y >= im_size[1]:
                     # out of image range
                     continue
               
                  moved_index = im1pindex + left_right + ( down_up * im_size[0] )
                  moved_im1pixels[ moved_index ] = im1pixels[im1pindex]
   
               
               # if more than the threshold % of moved_x or moved_y has gone beyond the fixed_max_x or fixed_max_y, this means that beyond this point,
               # match will not be made. likewise is true for fixed_min_x, fixed_min_y.
               for beyond_xy in beyond_fixed_xy:
                  if beyond_fixed_xy[beyond_xy] > threshold_pixels_len:
                     if "_x" in beyond_xy:
                        beyond_value = left_right
                     elif "_y" in beyond_xy:
                        beyond_value = down_up
                        
                     skip_xy[ skip_beyond_lookup[beyond_xy] ] = beyond_value
   
               
               #image_functions.cr_im_from_pixels( "", "", moved_im1pixels.keys(), pixels_rgb=(255,0,0), input_im=save_filepath ) 
               
               matched_pixels = set()
               for im1pindex in moved_im1pixels:
                  if im1pindex in im2pixels.keys():
                     if ignore_colors is False:
                        if min_colors is True:
                           if moved_im1pixels[im1pindex] == im2pixels[im1pindex]:
                              # color is the same
                              matched_pixels.add( im1pindex )
                        else:
                              appear_diff = pixel_functions.compute_appearance_difference( moved_im1pixels[im1pindex], im2pixels[im1pindex] )
                              if appear_diff is False:
                                 # same appearance
                                 matched_pixels.add( im1pindex )

                           
                     else:
                        matched_pixels.add( im1pindex )
               

               if len( matched_pixels ) / len( im1pixels ) >= match_threshold:
                  if best_match is False:
                     return True

                  if best_match is True:
                     if len( matched_pixels ) > len( best_match_pixels ):
                        best_match_pixels = matched_pixels
                        
                        best_match_movement_values = ( left_right, down_up )
                        
   if best_match is False:
      return False
   elif best_match is True:
      return best_match_pixels, best_match_movement_values


# function name: match target  shape with neighbors while moving it
#
# im1pixels, im2pixels, target_im1pixels and target_im2pixels data form
# { pixel index: pixel color, ... } data types-> pixel index: int. pixel color ( r,g,b ). r, g, and b are int.
# if target_im2pixels is None, then this is to find matching pixels with target_im1pixels
# matching pixels are found from im_data
#
# im1pixels and im2pixels are NOT the shape coordinate pixels.
#
# added_shapes: for match difficulty variable. see documentation. match difficulty variable.docx
# added_shapes: [ [ image1 shapes pixels ], [ image2 shapes pixels ] ]. with data.  [ [ 20, 15, ... ], [ 10, ... ] ]
# if you don't intend to use added_shapes, then put None in it.
# 
# best_match requires im_data_shapeids_by_pindex and im_data_shapes
# best_match returns best_match_pixels
def match_t_shape_w_nbrs_while_moving_it( im1pixels, im2pixels, target_im1pixels, target_im2pixels, im_size, min_colors, added_shapes, match_threshold=0.5, 
                                          ignore_colors=False, im_data=None, return_pixels=False, best_match=False, im_data_shapeids_by_pindex=None, 
                                          im_data_shapes=None ):

   def reset_skip( skip_xy, cur_row_or_column ):
      if "pos" in cur_row_or_column:
         reset_value = 20
      elif "neg" in cur_row_or_column:
         reset_value = -20
      
      skip_xy[cur_row_or_column] = reset_value
      
   
   def get_matched_pixels( moved_im1pixels, pixels_to_match ):
      matched_pixels = set()
      for im1pindex in moved_im1pixels:
         if im1pindex in pixels_to_match.keys():
            if ignore_colors is False:
               if min_colors is True:
                  if moved_im1pixels[im1pindex] == pixels_to_match[im1pindex]:
                     # color is the same
                     matched_pixels.add( im1pindex )
               else:
                  appear_diff = pixel_functions.compute_appearance_difference( moved_im1pixels[im1pindex], pixels_to_match[im1pindex] )
                  if appear_diff is False:
                     # same appearance
                     matched_pixels.add( im1pindex )
                        
            else:
               matched_pixels.add( im1pindex )

      return matched_pixels


   target_match_threshold = match_threshold + 0.05

   # im2pixels is the fixed pixels and im1pixels move.
   # if im1pixels move beyond max x or y of im2pixels, then there will be no pixels. so skip them
   fixed_max_x = fixed_max_y = 0
   fixed_min_x = im_size[0] - 1
   fixed_min_y = im_size[1] - 1
   threshold_pixels_len = len( im1pixels ) * match_threshold
   
   for pindex in im2pixels.keys():
      xy = pixel_functions.convert_pindex_to_xy( pindex, im_size[0] )
      
      if xy[0] > fixed_max_x:
         fixed_max_x = xy[0]
      if xy[0] < fixed_min_x:
         fixed_min_x = xy[0]
      if xy[1] > fixed_max_y:
         fixed_max_y = xy[1]
      if xy[1] < fixed_min_y:
         fixed_min_y = xy[1]

   #print("fixed_min_x " + str(fixed_min_x) + " fixed_max_x " + str(fixed_max_x) + " fixed_min_y " + str(fixed_min_y) + " fixed_max_y " + str(fixed_max_y) )
   
   save_filepath = top_shapes_dir + "videos/street3/resized/min1/temp/test1.png"
   #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", im2pixels.keys(), pixels_rgb=(0,0,255), save_filepath=save_filepath ) 
   #image_functions.cr_im_from_pixels( "27", "videos/street3/resized/min1/", { (fixed_max_x, fixed_max_y), (fixed_min_x, fixed_min_y) } , pixels_rgb=(50,200,200), input_im=save_filepath ) 
   
   best_match_movement = None
   best_match_pixels = set()
   best_match_score = 0
   
   show_debug_im = False
   
   start_move = 0
   step_move = 1
   end_move = 20
   negative_start_move = -1
   # first one is for right and down. second tuple is for left and up.
   movements = [ ( start_move, end_move, step_move ), ( negative_start_move, -end_move, -step_move ) ]
   
   skip_xy = { "pos_x": 21, "neg_x": -21, "pos_y": 21, "neg_y": -21 }
   skip_beyond_lookup = { "max_x": "pos_x", "min_x": "neg_x", "max_y": "pos_y", "min_y": "neg_y" }
   for movement in movements:

      for left_right in range( movement[0], movement[1], movement[2] ):
         if left_right >= start_move and left_right > skip_xy["pos_x"]:
            # for the current movement, all threshold value of pixels are beyond fixed im2pixels
            if left_right == end_move:
               reset_skip( skip_xy, "pos_x" )
            break
         elif left_right < start_move and left_right < skip_xy["neg_x"]:
            if left_right == -end_move:
               reset_skip( skip_xy, "neg_x" )
            break
         
         for movement in movements:
            for down_up in range( movement[0], movement[1], movement[2] ):
               if down_up >= start_move and down_up > skip_xy["pos_y"]:
                  # skip up to the current end of pos_y for the current x
                  if down_up == end_move:
                     reset_skip( skip_xy, "pos_y" )
                  break
               elif down_up < start_move and down_up < skip_xy["neg_y"]:
                  if down_up == -end_move:
                     reset_skip( skip_xy, "neg_y" )
                  break

               # { index: pixel color, ... }
               moved_im1pixels = {}
               beyond_fixed_xy = { "max_x": 0, "min_x": 0, "max_y": 0, "min_y": 0 }
               for im1pindex in im1pixels:
                  xy = pixel_functions.convert_pindex_to_xy( im1pindex, im_size[0] )
                  moved_x = xy[0] + left_right
                  moved_y = xy[1] + down_up
                  
                  if moved_x > fixed_max_x:
                     beyond_fixed_xy["max_x"] += 1
                  if moved_y > fixed_max_y:
                     beyond_fixed_xy["max_y"] += 1
                  if moved_x < fixed_min_x:
                     beyond_fixed_xy["min_x"] += 1
                  if moved_y < fixed_min_y:
                     beyond_fixed_xy["min_y"] += 1

                  if moved_x < 0 or moved_x >= im_size[0] or moved_y < 0 or moved_y >= im_size[1]:
                     # out of image range
                     continue
               
                  moved_index = im1pindex + left_right + ( down_up * im_size[0] )
                  moved_im1pixels[ moved_index ] = im1pixels[im1pindex]
   
               
               # if more than the threshold % of moved_x or moved_y has gone beyond the fixed_max_x or fixed_max_y, this means that beyond this point,
               # match will not be made. likewise is true for fixed_min_x, fixed_min_y.
               for beyond_xy in beyond_fixed_xy:
                  if beyond_fixed_xy[beyond_xy] > threshold_pixels_len:
                     if "_x" in beyond_xy:
                        beyond_value = left_right
                     elif "_y" in beyond_xy:
                        beyond_value = down_up
                        
                     skip_xy[ skip_beyond_lookup[beyond_xy] ] = beyond_value
   
               if show_debug_im is True:
                  image_functions.cr_im_from_pixels( "", "", moved_im1pixels.keys(), pixels_rgb=(255,0,0), input_im=save_filepath ) 
                  show_debug_im = False
               
               # match difficulty variable calculation. for details, refer to documentation. match difficulty variable.docx
               match_difficulty_variable = 0
               if added_shapes is not None:
                  for im1or2 in range(2):
                     total_pixels_len = sum( added_shapes[im1or2] )
                     largest_shape_len = max( added_shapes[im1or2] )
                  
                     for each_shape_len in added_shapes[im1or2]:
                        if each_shape_len == largest_shape_len:
                           continue
                     
                        cur_shape_percent = each_shape_len / total_pixels_len
                        cur_shape_diff = largest_shape_len - each_shape_len
                        cur_shape_score = cur_shape_diff * cur_shape_percent
                     
                        match_difficulty_variable += cur_shape_score
               
               
               matched_pixels = get_matched_pixels( moved_im1pixels, im2pixels )
               matched_pixels_len = len(matched_pixels) + match_difficulty_variable

               #print("match_difficulty_variable " + str(match_difficulty_variable) + " matched_pixels " + str( len(matched_pixels) ) )
               #image_functions.cr_im_from_pixels( "28", "videos/street3/resized/min1/", matched_pixels, pixels_rgb=(0,255,255) ) 
               
               # when target_im2pixels is None, im2pixels do not contain target_im2pixels, so the match is determined by how many im2pixels matched instead of im1pixels
               if target_im2pixels is None:
                  judge_match_len = min( [ len(im1pixels) - len(target_im1pixels), len(im2pixels) ] )
               else:
                  judge_match_len = len(im1pixels)
               
               if matched_pixels_len / judge_match_len >= match_threshold:

                  moved_target1pixels = {}
                  for target_im1pixel in target_im1pixels:
                     xy = pixel_functions.convert_pindex_to_xy( target_im1pixel, im_size[0] )
                     moved_x = xy[0] + left_right
                     moved_y = xy[1] + down_up

                     if moved_x < 0 or moved_x >= im_size[0] or moved_y < 0 or moved_y >= im_size[1]:
                        # out of image range
                        continue
               
                     moved_index = pixel_functions.get_pindex_with_xy_input( target_im1pixel, (left_right, down_up ), im_size[0] )
                     moved_target1pixels[ moved_index ] = target_im1pixels[target_im1pixel]
                  
                  #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", moved_target1pixels.keys(), pixels_rgb=(255,255,0) ) 
                  if target_im2pixels is None:
                     _target_im2pixels = {}
                     for moved_index in moved_target1pixels:
                        _target_im2pixels[moved_index] = im_data[moved_index]
                     
                  else:
                     _target_im2pixels = target_im2pixels

                  #image_functions.cr_im_from_pixels( "29", "videos/street3/resized/min1/", _target_im2pixels, pixels_rgb=(255,0,255) ) 
                  matched_pixels = get_matched_pixels( moved_target1pixels, _target_im2pixels )

                  if len( matched_pixels ) == 0:
                     continue
                  if best_match is True:
                     # { shapeid: matched count, ... }
                     matched_shapes = {}
                     cur_matched_score = 0
                     for matched_pindex in matched_pixels:
                        for matched_shapeid in im_data_shapeids_by_pindex[matched_pindex]:
                           if matched_shapeid not in matched_shapes:
                              matched_shapes[matched_shapeid] = 1
                           else:
                              matched_shapes[matched_shapeid] += 1
                     
                     for matched_shapeid in matched_shapes:
                        shape_len_matched_percent = matched_shapes[matched_shapeid] / len( im_data_shapes[matched_shapeid] )
                        matched_len_percent = matched_shapes[matched_shapeid] / len(matched_pixels)
                        
                        cur_shape_score = shape_len_matched_percent * matched_shapes[matched_shapeid] * matched_len_percent
                        cur_matched_score += cur_shape_score
                     
                     if cur_matched_score > best_match_score:
                        best_match_score = cur_matched_score
                        best_match_pixels = matched_pixels
                  
                  else:
                     if len( matched_pixels ) / len( moved_target1pixels ) >= target_match_threshold or len(matched_pixels) / len(_target_im2pixels) >= target_match_threshold:
                        if return_pixels is False:
                           return True
                        else:
                           return matched_pixels

   if best_match is True:
      return best_match_pixels
   
   elif return_pixels is True:
      return set()
   else:
      return False









# im1pixels and im2pixels form
# {(236, 97), (236, 94), ... }
#
# # best_match means to not stop after finding the match at match_threshold but continue doing it and return the result of best match
def match_moving_shape( im1pixels, im2pixels, disappeared_pixels, appeared_pixels, im_size, match_threshold=0.4 ):

   def get_pixels_in_all_movements():
      pixels_in_all_movements = {}
      
      for move_right in range( 0, move_threshold, 2 ):
         for move_up in range( 0, move_threshold, 2 ):

            # finished moving shapes. right now, shapes are in the right location to be compared
            moved_im1pixels = set()
            for xy in im1pixels:
               moved_x = xy[0] + move_right
               if moved_x  >= im_size[0]:
                  continue
               moved_y = xy[1] - move_up
               if moved_y < 0:
                  continue
            
               moved_im1pixels.add( ( moved_x, moved_y ) )
            
            pixels_in_all_movements[ str(move_right) + "." + str(move_up * -1) ] = moved_im1pixels

         for move_down in range( 2, move_threshold, 2 ):
            # finished moving shapes. right now, shapes are in the right location to be compared
            moved_im1pixels = set()
            for xy in im1pixels:
               moved_x = xy[0] + move_right
               if moved_x  >= im_size[0]:
                  continue
               moved_y = xy[1] + move_down
               if moved_y >= im_size[1]:
                  continue
            
               moved_im1pixels.add( ( moved_x, moved_y ) )   

            pixels_in_all_movements[ str(move_right) + "." + str(move_down) ] = moved_im1pixels

      for move_left in range( 2, move_threshold, 2 ):
         for move_up in range( 0, move_threshold, 2 ):

            # finished moving shapes. right now, shapes are in the right location to be compared
            moved_im1pixels = set()
            for xy in im1pixels:
               moved_x = xy[0] - move_left
               if moved_x  < 0:
                  continue
               moved_y = xy[1] - move_up
               if moved_y < 0:
                  continue
            
               moved_im1pixels.add( ( moved_x, moved_y ) )

            pixels_in_all_movements[ str(move_left * -1) + "." + str(move_up * -1) ] = moved_im1pixels

         for move_down in range( 2, move_threshold, 2 ):
            # finished moving shapes. right now, shapes are in the right location to be compared
            moved_im1pixels = set()
            for xy in im1pixels:
               moved_x = xy[0] - move_left
               if moved_x < 0:
                  continue
               moved_y = xy[1] + move_down
               if moved_y >= im_size[1]:
                  continue
            
               moved_im1pixels.add( ( moved_x, moved_y ) )

            pixels_in_all_movements[ str(move_left * -1) + "." + str(move_down) ] = moved_im1pixels

      return pixels_in_all_movements


   def get_rest_pixels( partial_pixels, partial_movement ):
      # check if many pixels remain unmatched
      rest_of_im2pixels = im2pixels.difference( partial_pixels )
      #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", rest_of_im2pixels, pixels_rgb=(0,255,255) )
      
      rest_of_im2pixels_len = len( rest_of_im2pixels )
      
      most_matched_im2pixels_len = 0
      
      most_matched_rest_pixels = matched_rest_movement = None
      if rest_of_im2pixels_len / len(im2pixels) >= 0.45:
         # many pixels remain unmatched. so check if these pixels can be matched in other movements.

         for movement, pixels in pixels_in_all_movements.items():
            movement_x = int( movement.split(".")[0] )
            movement_y = int( movement.split(".")[1] )
            movement = ( movement_x, movement_y )
            
            # skip if rest movement is close enought o partial_movement
            distance_x = abs( partial_movement[0] - movement_x )
            distance_y = abs( partial_movement[1] - movement_y )
            if distance_x + distance_y <= 3:
               continue

            rest_im2pixels_matched = rest_of_im2pixels.intersection(pixels)
            rest_im2pixels_matched_len = len(rest_im2pixels_matched)

            if rest_im2pixels_matched_len / rest_of_im2pixels_len >= 0.7:
               if rest_im2pixels_matched_len > most_matched_im2pixels_len:
                  most_matched_im2pixels_len = rest_im2pixels_matched_len
                  
                  matched_rest_movement = movement
                  
                  most_matched_rest_pixels = rest_im2pixels_matched
            
         
      
      return most_matched_rest_pixels, matched_rest_movement



   def get_large_conn_pixels( dis_appeared_pixels ):
      # generated_disappeared_shapes
      
      if len(dis_appeared_pixels) == 0:
         return set()
      
      gen_dis_appeared_shapes = pixel_functions.find_shapes( dis_appeared_pixels, im_size  )
            
      largest_conn_pixels_len = 0
      for generated_shapeid in gen_dis_appeared_shapes:
         if len( gen_dis_appeared_shapes[generated_shapeid] ) > largest_conn_pixels_len:
            largest_conn_pixels_len = len( gen_dis_appeared_shapes[generated_shapeid] )
            
      large_dis_apprd_pixels = set()
      for generated_shapeid in gen_dis_appeared_shapes:
         if len( gen_dis_appeared_shapes[generated_shapeid] ) / largest_conn_pixels_len >= 0.6:
            large_dis_apprd_pixels |= gen_dis_appeared_shapes[generated_shapeid]

      large_dis_apprd_pixels_cp = copy.deepcopy( large_dis_apprd_pixels )
      large_dis_apprd_pixels = set()
      for pixel in large_dis_apprd_pixels_cp:
         xy = pixel_functions.convert_pindex_to_xy( pixel, im_size[0] )
      
         large_dis_apprd_pixels.add(xy)
      
      return large_dis_apprd_pixels



   # take large connected pixels from disappeared_pixels and appeared_pixels
   large_conn_disapprd_pixels = get_large_conn_pixels( disappeared_pixels )
   large_conn_appeared_pixels = get_large_conn_pixels( appeared_pixels )


   def determine_most_matched_movement( param_moved_im1pixels, most_matched_pixels_len, debug=False ):
      
      partial_movement = False
      partial_pixels = set()      

      #save_temp_file = top_shapes_dir + "videos/street3/resized/min1/temp/test1.png"
      #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", im2pixels, save_filepath=save_temp_file , pixels_rgb=(0,0,255) )
      #image_functions.cr_im_from_pixels( "", "", param_moved_im1pixels, input_im=save_temp_file, pixels_rgb=(255,0,0) )
      
      matched_pixels = param_moved_im1pixels.intersection( im2pixels )

      if len(matched_pixels) >= 1:
      
         cur_score = len( matched_pixels ) * 1.3
         if cur_score > most_matched_pixels_len:
            most_matched_pixels_len = cur_score
            
         # larger value of moved_out_pixels indicates that the param_moved_im1pixels have gotten out of the large_conn_disapprd_pixels
         moved_out_pixels = large_conn_disapprd_pixels.difference( param_moved_im1pixels )
         moved_out_pixels_len = len(moved_out_pixels)
            
         # the bigger value of the moved_into_pixels the more param_moved_im1pixels moved into large_conn_appeared_pixels
         moved_into_pixels = large_conn_appeared_pixels.intersection( param_moved_im1pixels )
         moved_into_pixels_len = len(moved_into_pixels)
            
         if debug is True:
            pass


         # check if this is partial movement of the partial shapes
         # if disappeared and appeared_pixels are both 0 means that im1pixels did not move at all. and im1pixels and im2pixels match more than 80%
         if  moved_out_pixels_len >= 1 and moved_out_pixels_len / len( large_conn_disapprd_pixels ) >= match_threshold + 0.2:
            if moved_into_pixels_len >= 1 and moved_into_pixels_len / len(large_conn_appeared_pixels) >= match_threshold + 0.2:
               # possible partial movement. now, get all pixels that are connected to large_conn_appeared_pixels
               

                  #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", matched_pixels, pixels_rgb=(0,0,255) )
                  pix_in_Lconn_apprd = large_conn_appeared_pixels.intersection( matched_pixels )

                  partial_movement = True
                  conn_pixels = pixel_functions.get_connected_pixels( pix_in_Lconn_apprd, matched_pixels, im_size )
                  for each_conn_pixels in conn_pixels:
                     partial_pixels |= each_conn_pixels

                  


         if len(matched_pixels) / len(im1pixels) < match_threshold + 0.15 and len( matched_pixels ) / len( im2pixels ) < match_threshold + 0.15 :      
            if moved_out_pixels_len >= 1 and moved_out_pixels_len / len( large_conn_disapprd_pixels )  >= match_threshold:
               moved_out_score = moved_out_pixels_len * ( moved_out_pixels_len / len( large_conn_disapprd_pixels ) )
            
                  
               if moved_into_pixels_len < 1 or moved_into_pixels_len / len(large_conn_appeared_pixels) < match_threshold:
                  return most_matched_pixels_len, partial_movement, partial_pixels
                  
               moved_into_score = moved_into_pixels_len * ( moved_into_pixels_len / len(large_conn_appeared_pixels) )
               
               cur_score = len(matched_pixels) + ( ( moved_out_score + moved_into_score ) / 2 )
               if cur_score > most_matched_pixels_len:
                  most_matched_pixels_len = cur_score


      return most_matched_pixels_len, partial_movement, partial_pixels
   



   move_threshold = 17


   most_matched_pixels_len = 0
   most_matched_movement = None
   
   most_matched_partial_movement = None
   
   partial_movement_largest_pixels_len = 0
   
   all_partial_matches = []
   '''
   save_temp_file = top_shapes_dir + "videos/street3/resized/min1/temp/test1.png"
   image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", large_conn_appeared_pixels, pixels_rgb=(255,0,255), save_filepath=save_temp_file )
   save_temp_file2 = top_shapes_dir + "videos/street3/resized/min1/temp/test2.png"
   image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", im2pixels, pixels_rgb=(255,0,255), save_filepath=save_temp_file2 )
   '''
   # pixels_in_all_movements[ str(move_right) + "." + str(move_up * -1) ] = moved_im1pixels
   pixels_in_all_movements = get_pixels_in_all_movements()
   
   
   for movement_str, moved_im1pixels in pixels_in_all_movements.items():
      movement_x = int( movement_str.split(".")[0] )
      movement_y = int( movement_str.split(".")[1] )
      movement = ( movement_x, movement_y )
      
      '''
      if ( movement_x > 3 or movement_x < -3 or movement_y > 3 or movement_y < -3 ) and movement != (0, 14):
         continue
      print("current movement " + str(movement) )
      '''
      
      cur_most_m_pixels_len, partial_movement, partial_pixels = determine_most_matched_movement( moved_im1pixels, most_matched_pixels_len )   
      if cur_most_m_pixels_len > most_matched_pixels_len:
         most_matched_pixels_len = cur_most_m_pixels_len
         most_matched_movement = movement

      if partial_movement is True:

         # current partial movement is true. check if rest of pixels match in other movements.
         rest_pixels, rest_movement = get_rest_pixels( partial_pixels, movement )

         if rest_pixels is None:
            continue
         
         assert len( partial_pixels ) >= 1 and len( rest_pixels ) >= 1
         assert partial_pixels != rest_pixels
         
         
         matched_total = len(partial_pixels) * 1.5 + len(rest_pixels)
         if matched_total > partial_movement_largest_pixels_len :            
            partial_movement_largest_pixels_len = matched_total

            all_partial_matches.append( [ partial_pixels, rest_pixels, movement, rest_movement ] )
            
            #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", partial_pixels, pixels_rgb=(0,255,255), input_im=save_temp_file )
            #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", rest_pixels, pixels_rgb=(0,255,255), input_im=save_temp_file2 )

         elif matched_total / partial_movement_largest_pixels_len >= 0.95:
            # current partial movement shapes has 90% or more close in size with the current biggest match. so include this as well
            all_partial_matches.append( [ partial_pixels, rest_pixels, movement, rest_movement ] )

            #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", partial_pixels, pixels_rgb=(0,255,255), input_im=save_temp_file )    
            #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", rest_pixels, pixels_rgb=(0,255,255), input_im=save_temp_file2 )            

   # make sure to take only partial movement shapes that have 90% or more of the same size as the largest partial shapes match
   all_partial_matches_cp = copy.deepcopy( all_partial_matches )
   deleted = 0
   for index, partial_match in enumerate(all_partial_matches_cp):
      cur_match_count = len( partial_match[0] ) * 1.5 + len( partial_match[1] )
      
      if cur_match_count / partial_movement_largest_pixels_len < 0.95:
         all_partial_matches.pop( index - deleted )
         deleted += 1


   return most_matched_movement, all_partial_matches





# boundary and attached_pixels should be list or set of xy.

def pixels_are_near( boundary1, attached_pixels1, boundary2, attached_pixels2, im_size, attached_threshold = 0.4, boundary_threshold=0.5 ):
   # overall boundaries match means that both shapes are structually the same.
   if type(boundary1) is not set:
      boundary1 = set(boundary1)
   if type(attached_pixels1) is not set:
      attached_pixels1 = set(attached_pixels1)
   if type(boundary2) is not set:
      boundary2 = set(boundary2)
   if type(attached_pixels2) is not set:
      attached_pixels2 = set(attached_pixels2)

   if len(boundary1) > len(boundary2):
      bigger_boundary = boundary1 
      smaller_boundary = boundary2 
   else:
      bigger_boundary = boundary2
      smaller_boundary = boundary1
   
   if len(attached_pixels1) > len(attached_pixels2):
      bigger_attached_pix = attached_pixels1
      smaller_attached_pix = attached_pixels2
   else:
      bigger_attached_pix = attached_pixels2
      smaller_attached_pix = attached_pixels1   

   matched_boundaries = set()
   for pixel in smaller_boundary:
      
      vicinity_pixels = pixel_functions.get_vicinity_pixels( pixel, 2, im_size )
      matched_pixels = set(vicinity_pixels).intersection( bigger_boundary )
      if len(matched_pixels) >= 1:
         matched_boundaries.add(pixel)

   matched_boundary_percent = len(matched_boundaries) / len( smaller_boundary )
   if matched_boundary_percent >= boundary_threshold:
      return True
   elif matched_boundary_percent < boundary_threshold / 2:
      return False
   
   # the smaller the matched_boundary_percent is, the bigger the match_threshold becomes. if boundary matches small, attached_pixels need to match
   # more to compensate for the not matched boundaries.
   boundary_factor = matched_boundary_percent / boundary_threshold
   match_threshold = attached_threshold / boundary_factor
   if match_threshold > 1:
      # because attached pixels can not match more than 100%
      match_threshold = 1
  
   # smaller matched pixels
   near_attached_pixels = set()
   for pixel in smaller_attached_pix:
      
      vicinity_pixels = pixel_functions.get_vicinity_pixels( pixel, 2, im_size )
      matched_pixels = set(vicinity_pixels).intersection( bigger_attached_pix )
      if len(matched_pixels) >= 1:
         near_attached_pixels.add(pixel)

   if len(near_attached_pixels) / len( smaller_attached_pix ) < match_threshold:
      return False
   else:
      return True
   



# all pixels should be xy.
# common_nbr_matches { (79689, 65674), (55299, 70906), ... }
# app_im_shapes_nbr_pixels are the one returned by pixel_shapes_functions.get_only_nbr_pixels
# app_im_shapes_movement: ( x,y )
def check_by_pixels_attachment( common_nbr_matches, im_shapes, app_im_shapes_nbr_pixels, im_size, 
                                 app_im_shapes_boundaries, im_pixels, shapes_movement, min_colors ):

   result = None

   for neighbor_match in common_nbr_matches:

      im1neighbor_pixels = set( im_shapes[0][ neighbor_match[0] ] )
      im2neighbor_pixels = set( im_shapes[1][ neighbor_match[1] ] )  
      
      im1attached_pixels = pixel_shapes_functions.get_attached_pixels( app_im_shapes_nbr_pixels[0], im1neighbor_pixels ) 
      im2attached_pixels = pixel_shapes_functions.get_attached_pixels( app_im_shapes_nbr_pixels[1], im2neighbor_pixels )

      if len(im1attached_pixels) == 0 or len(im2attached_pixels) == 0:
         continue
      
      #image_functions.cr_im_from_pixels( "29", "videos/street3/resized/min1/", im1neighbor_pixels, pixels_rgb=(255,0,0) )
      #image_functions.cr_im_from_pixels( "30", "videos/street3/resized/min1/", im2neighbor_pixels, pixels_rgb=(0,0,255) )           
      
      size_diff = check_size_by_pixels( im1neighbor_pixels, im2neighbor_pixels, size_threshold=1, im_size=im_size )
      if size_diff is True:
         # size too different
         continue

      neighbor_movement = [ temp_data[2] for temp_data in shapes_movement if temp_data[0]  == {neighbor_match[0]} and
                                 temp_data[1] == {neighbor_match[1]} ]
      if len( neighbor_movement ) == 0:
         # can not find movement for the cur_im_shapeids. so get it newly
   
      
         # { pixel index: pixel color }
         im1shapes_pixels_wk = {}
         im2shapes_pixels_wk = {}
         for temp_pixel in im1neighbor_pixels:
            pindex = pixel_functions.convert_xy_to_pindex( temp_pixel, im_size[0] )
            im1shapes_pixels_wk[pindex] = im_pixels[0][ pindex ]
         
         for temp_pixel in im2neighbor_pixels:
            pindex = pixel_functions.convert_xy_to_pindex( temp_pixel, im_size[0] )
            im2shapes_pixels_wk[pindex] = im_pixels[1][ pindex ]

         # im1im2_match {8192, 8193, 8198, 8208, ... }. movement (0,0). movement ( right left, up down )
         im1im2_match, movement = match_shape_while_moving_it2( im1shapes_pixels_wk, im2shapes_pixels_wk, im_size, min_colors,  best_match=True )
         if len(im1im2_match) == 0:
            continue

         neighbor_movement = movement
      else:
         neighbor_movement = neighbor_movement[0]
 
      moved_im1attached_pixels = set()
      moved_im1boundaries = set()
   
      for pixel in im1attached_pixels:
         moved_xy = ( pixel[0] + neighbor_movement[0], pixel[1] + neighbor_movement[1] )
         moved_im1attached_pixels.add( moved_xy )
   
      for pixel in app_im_shapes_boundaries[0]:
         moved_xy = ( pixel[0] + neighbor_movement[0], pixel[1] + neighbor_movement[1] )
         moved_im1boundaries.add( moved_xy )

      '''
      im1save_filepath = top_shapes_dir + "videos/street3/resized/min1/temp/test2.png"
      image_functions.cr_im_from_pixels( "30", "videos/street3/resized/min1/", moved_im1boundaries, pixels_rgb=(255,0,0), save_filepath=im1save_filepath )  
      im2save_filepath = top_shapes_dir + "videos/street3/resized/min1/temp/test3.png"
      image_functions.cr_im_from_pixels( "30", "videos/street3/resized/min1/", app_im_shapes_boundaries[1], pixels_rgb=(0,0,255), save_filepath=im2save_filepath )  
      image_functions.cr_im_from_pixels( "", "", moved_im1attached_pixels, pixels_rgb=(50,50,200), input_im=im1save_filepath ) 
      image_functions.cr_im_from_pixels( "", "", im2attached_pixels, pixels_rgb=(0,150,150), input_im=im2save_filepath )          
      '''
   
      attached_near = pixels_are_near( moved_im1boundaries, moved_im1attached_pixels, app_im_shapes_boundaries[1], im2attached_pixels , im_size )
      if attached_near is True:
         return True
      elif attached_near is False:
         result = False
         
   return result
   

# find match by moving shape against image pixels
# matching target_pixels against image pixels. return the matched shapeid when return_shapeids is true
# im_shapes_colors: [ target_shapes_colors, im_data_shapes_colors ]
# im_shapeids_by_pindex: [ target_shapeids_by_pindex, im_data_shapeids_by_pindex ]
# whole_pixels and target_pixels are set of pixel indexes.
# whole_pixels contain pixels of one or more neighbors of target_pixels
def match_by_mov_shape_against_im( im_shapes_colors, im_shapeids_by_pindex, whole_pixels, target_pixels, im_size, min_colors, im_data_shapes, 
                                   return_shapeids=False, return_matched_pixels=False ):

   move_amount = 16
   match_threshold = 0.55
   whole_threshold = 0.6
   each_threshold = 0.4
   
   most_matched_score = 0
   #  { matched image data shapeid: score, ... }
   most_matched_shapeids = {}
   
   # [ most_matched_t_pixels, most_matched_nont_pixels, most_matched_movement ]
   most_matched_pixels = [ set(), set(), None ]
   
   for pos_neg_RL in [ 1, -1 ]:
      if pos_neg_RL == 1:
         start_position_RL = 0
      else:
         start_position_RL = 1
   
      for move_RL in range( start_position_RL, move_amount ):
         move_RL *= pos_neg_RL
      
         for pos_neg_UD in [ 1, - 1 ]:
            if pos_neg_UD == 1:
               start_position_UD = 0
            else:
               start_position_UD = 1
         
            for move_UD in range( start_position_UD, move_amount ):
               move_UD *= pos_neg_UD

               non_t_matched_pixels = set()
               # target_matched_mv_pixels contain image data pixel when it matched target pixel
               target_matched_mv_pixels = set()
               
               matched_pixels = set()

               # matched image data shapeids.
               # this is for taking all image shapes pixels that matched with non and target pixels.
               # { matched im_data_shapeid: matched count, ... } 
               matched_t_im_shapeids = {}
               # because nont may contain multiple shapes, matched image data shapes need to be matched with their own matched nont shapes
               # { matched image data shapeid: [ matched nont shapeids ], ... }
               matched_non_t_im_shapeids = {}
               
               
               debug_moved_pixels = set()
               for whole_pixel in whole_pixels:
                  pixel_matched = False
                  
                  cur_pixel_colors = set()
                  
                  for whole_shapeid in im_shapeids_by_pindex[0][whole_pixel]:
                     cur_pixel_colors.add( im_shapes_colors[0][whole_shapeid] )

                  whole_pixel_xy = pixel_functions.convert_pindex_to_xy( whole_pixel, im_size[0] )
                  if whole_pixel_xy[0] + move_RL >= im_size[0] or whole_pixel_xy[0] + move_RL < 0:
                     # out of image range
                     continue
                  if whole_pixel_xy[1] + move_UD >= im_size[1] or whole_pixel_xy[1] + move_UD < 0:
                     continue
                  
                  moved_pindex = pixel_functions.get_pindex_with_xy_input( whole_pixel, (move_RL,move_UD), im_size[0] )
                  debug_moved_pixels.add(moved_pindex)
                  
                  for im_data_shapeid in im_shapeids_by_pindex[1][moved_pindex]:
                     cur_im_color = im_shapes_colors[1][im_data_shapeid]
                     
                     if min_colors is True:
                        if cur_im_color in cur_pixel_colors:
                           pixel_matched = True
                           break
         
                     else:
                        for cur_pixel_color in cur_pixel_colors:
                           appearance_diff = pixel_functions.compute_appearance_difference(cur_im_color, cur_pixel_color )
                           if appearance_diff is False:
                              # same color
                              pixel_matched = True
                              break                       
                        if pixel_matched is True:
                           break
                       

                  if pixel_matched is True:
                     matched_pixels.add(moved_pindex)
                     if whole_pixel in target_pixels:
                        target_matched_mv_pixels.add(moved_pindex)                       
                        
                        for im_data_shapeid in im_shapeids_by_pindex[1][moved_pindex]:
                           if im_data_shapeid not in matched_t_im_shapeids:
                              matched_t_im_shapeids[im_data_shapeid] = 1
                           else:
                              matched_t_im_shapeids[im_data_shapeid] += 1                           
                        
                     else:
                        non_t_matched_pixels.add(moved_pindex) 
                        cur_matched_nont_shapeids = im_shapeids_by_pindex[0][whole_pixel]
                        
                        for im_data_shapeid in im_shapeids_by_pindex[1][moved_pindex]:
                           if im_data_shapeid not in matched_non_t_im_shapeids:
                              matched_non_t_im_shapeids[im_data_shapeid] = list(cur_matched_nont_shapeids)
                           else:
                              matched_non_t_im_shapeids[im_data_shapeid].extend( cur_matched_nont_shapeids )

        
               #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", matched_pixels, pixels_rgb=(0,255,255) ) 
               
               #print( "target_matched_mv_pixels " + str( len(target_matched_mv_pixels) ) + " target_pixels " + str(len(target_pixels)) + 
               #       " non_t_matched_pixels " + str(len(non_t_matched_pixels)) + " non_target_pixels " + str( ( len(whole_pixels) - len(target_pixels) ) ) + \
               #       " movement " + str(move_RL) + "," + str(move_UD) )
               
               target_matched_score = len(target_matched_mv_pixels) / len(target_pixels)
               if len(whole_pixels) == len(target_pixels):
                  nont_matched_score = len(non_t_matched_pixels)  / len(whole_pixels)
               else:
                  nont_matched_score = len(non_t_matched_pixels)  / ( len(whole_pixels) - len(target_pixels) )
               
               if target_matched_score < match_threshold or nont_matched_score < match_threshold:
                  each_match_condition = False
               else:
                  each_match_condition = True
               
               if len(matched_pixels) / len(whole_pixels) < whole_threshold or target_matched_score < each_threshold or nont_matched_score < each_threshold:
                  whole_match_condition = False
               else:
                  # all whole_match_conditions have been met
                  whole_match_condition = True
               
               if each_match_condition is False and whole_match_condition is False :
                  # not matched 
                  continue
               
               #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", matched_pixels, pixels_rgb=(0,255,255) ) 
               
               cur_total_score = target_matched_score + nont_matched_score
               
               # get image data shapeid that matched with target_pixels.
               # { shapeid: matched count, ... }
               candidate_imd_shapeids = {}
               for imd_pixel in target_matched_mv_pixels:
                  for imd_shapeid in im_shapeids_by_pindex[1][imd_pixel]:
                     if imd_shapeid not in candidate_imd_shapeids.keys():
                        candidate_imd_shapeids[imd_shapeid] = 1
                     else:
                        candidate_imd_shapeids[imd_shapeid] += 1
                     
               # { shapeid: score, ... }
               cur_matched_imd = {}
               cur_best_score = None
               for imd_shapeid in candidate_imd_shapeids:
                  
                  cur_sizes = [ len( im_data_shapes[imd_shapeid] ), len(target_pixels) ]
                        
                  cur_imd_shapeid_score = candidate_imd_shapeids[imd_shapeid] / cur_sizes[0]
                  cur_target_score = candidate_imd_shapeids[imd_shapeid] / cur_sizes[1]

                  size_diff = abs( cur_sizes[0] - cur_sizes[1] )
                  smaller_size = min( cur_sizes )
                  size_diff_score = size_diff / smaller_size
        
                  cur_imd_score = cur_imd_shapeid_score + cur_target_score - size_diff_score
                  cur_matched_imd[imd_shapeid] = cur_imd_score
                  if cur_best_score is None or cur_imd_score > cur_best_score:
                     cur_best_score = cur_imd_score
               
               cur_total_score += cur_best_score
               if cur_total_score > most_matched_score:
                  most_matched_score = cur_total_score      
                  
                  if return_matched_pixels is True:
                     most_matched_pixels = [ target_matched_mv_pixels, non_t_matched_pixels, ( move_RL, move_UD ) ]
                  elif return_shapeids is True:
                     most_matched_shapeids = cur_matched_imd
                  
               if return_matched_pixels is False and return_shapeids is False:
                  # matched. so return True immidiately
                  return True
                  

   if return_shapeids is True:   
      # sort by values. ordered by best score. best score comes first.
      most_matched_shapeids = sorted(most_matched_shapeids.items(), key=lambda x:x[1], reverse=True)
      
      return most_matched_shapeids      
      
   elif return_matched_pixels is True:
      return most_matched_pixels

   else:
      return False



# im_shapes_pixels -> [ { image1 shapes pixels }, { image2 shapes pixels } ]
# im_shapes_pixch -> [ { pixch on image1 shapes }, { pixch on image2 shapes } ]
# all pixels are pixel indexes
def get_shapes_movement_by_pixch( im_shapes_pixels, im_shapes_pixch, im_size ):
   
   best_match_percent = 0
   best_movement = None

   move_amount = 16
   
   debug_file = top_shapes_dir + "videos/street3/resized/min1/temp/test.png"

   for pos_neg_RL in [ 1, -1 ]:
      if pos_neg_RL == 1:
         start_position_RL = 0
      else:
         start_position_RL = 1
   
      for move_RL in range( start_position_RL, move_amount ):
         move_RL *= pos_neg_RL
      
         for pos_neg_UD in [ 1, - 1 ]:
            if pos_neg_UD == 1:
               start_position_UD = 0
            else:
               start_position_UD = 1
         
            for move_UD in range( start_position_UD, move_amount ):
               move_UD *= pos_neg_UD
      
               #print("move_RL " + str(move_RL) + " move_UD " + str(move_UD) )
               
               # { pixel indexes }
               moved_im1pixels = pixel_functions.move_pixels( im_shapes_pixels[0], move_RL, move_UD, input_xy=False, im_width=im_size[0] )
               
               matched_pixels = moved_im1pixels.intersection( im_shapes_pixels[1] )
               
               #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", moved_im1pixels, pixels_rgb=(255,0,0), save_filepath=debug_file )
               #image_functions.cr_im_from_pixels( "", "", im_shapes_pixch[0], pixels_rgb=(255,255,0), save_filepath=debug_file, input_im=debug_file )
               #image_functions.cr_im_from_pixels( "", "", im_shapes_pixch[1], pixels_rgb=(255,0,255), input_im=debug_file )

               # moved_im1pixels should be out of pixch on image1 shapes and they should move into enough amount of pixch on image2 shapes.
               out_pixels = im_shapes_pixch[0].intersection(moved_im1pixels)
               if len(im_shapes_pixch[0]) == 0:
                  out_p_matched_percent = 1
               else:
                  out_p_matched_percent = 1 - ( len(out_pixels) / len(im_shapes_pixch[0]) )
               
               into_pixels = im_shapes_pixch[1].intersection(moved_im1pixels)
               if len(im_shapes_pixch[1]) == 0:
                  into_p_matched_percent = 0
               else:
                  into_p_matched_percent = len(into_pixels) / len(im_shapes_pixch[1])
               
               pixch_match = out_p_matched_percent + into_p_matched_percent
               pixels_match = len(matched_pixels) / len(im_shapes_pixels[0])
               cur_match_percent = pixch_match + pixels_match
               if cur_match_percent > best_match_percent:
                  best_match_percent = cur_match_percent
                  best_movement = ( move_RL, move_UD )
                  

   return best_movement             


# movements -> { movement: score, ... }. with example data. { (-1,2): 0.1253..., ... }
# param_im_shapes_pixels -> [ { image1 shapes pixels }, { image2 shapes pixels } ].  pixels are indexes
def match_from_given_movements( mv_scores, param_im_shapes_pixels, im_size, match_threshold=0.5 ):

   best_score = 0
   best_movement = None

   for movement in mv_scores:
      moved_im1pixels = set()
      for pindex in param_im_shapes_pixels[0]:
         moved_pindex = pixel_functions.get_pindex_with_xy_input( pindex, movement, im_size[0] )
         moved_im1pixels.add(moved_pindex)
      
      matched_pixels = param_im_shapes_pixels[1].intersection( moved_im1pixels )
      
      if len(matched_pixels) >= 1 and ( len(matched_pixels) / len(param_im_shapes_pixels[0]) >= match_threshold or 
         len(matched_pixels) / len(param_im_shapes_pixels[1]) >= match_threshold ):
         
         match_score = len(matched_pixels) * mv_scores[movement]
         if match_score > best_score:
            best_score = match_score
            best_movement = movement
   
   return best_movement


# documentation: libraries/same_shapes_functions/check_combined_match.docx
def check_combined_match( im_shapes_pixels, nbr_pixch, im_size ):
   pass






























