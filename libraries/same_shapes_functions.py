
from libraries import pixel_shapes_functions, read_files_functions, pixel_functions, image_functions
from libraries.cv_globals import third_smallest_pixc, frth_smallest_pixc

from PIL import Image
import math
import os, sys
import copy
from collections import Counter




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

         #input_im = "images/videos/street3/resized/min/test.png"
         #image_functions.cr_im_from_pixels( "10", "videos/street3/resized/min/", cur_im1pixels, pixels_rgb=(255,0,0), input_im=input_im )
         #image_functions.cr_im_from_pixels( "11", "videos/street3/resized/min/", cur_im2pixels, pixels_rgb=(255,0,0), input_im=input_im )
         
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
# { xy in string: shape color }
#
# # best_match means to not stop after finding the match at match_threshold but continue doing it and return the result of best match
def match_shape_while_moving_it2( im1pixels, im2pixels, im_size, match_threshold=0.5, best_match=False):


   # get image1 and image2 most virtically abundant column
   im1_xes = [ int( xy.split(".")[0] ) for xy in im1pixels.keys() ]
   im2_xes = [ int( xy.split(".")[0] ) for xy in im2pixels.keys() ]
   
   # { 0: 3, 1: 0, ... }
   # { x: how many pixels on this x ... }
   im1xes_abundances = Counter( im1_xes )
   im2xes_abundances = Counter( im2_xes )
   
   im1most_abundant_x = max( im1xes_abundances, key=im1xes_abundances.get )
   im2most_abundant_x = max( im2xes_abundances, key=im2xes_abundances.get )

   # get image1 and image2 most horizontally abundant row
   im1_y_s = [ int( xy.split(".")[1] ) for xy in im1pixels.keys() ]
   im2_y_s = [ int( xy.split(".")[1] ) for xy in im2pixels.keys() ]
   
   im1ys_abundances = Counter( im1_y_s )
   im2ys_abundances = Counter( im2_y_s )
   
   im1most_abundant_y = max( im1ys_abundances, key=im1ys_abundances.get )
   im2most_abundant_y = max( im2ys_abundances, key=im2ys_abundances.get )
   
   Rmost_x = 0
   bottom_y = 0

   if im1most_abundant_x >= im2most_abundant_x:
      Rmost_x = im1most_abundant_x - im2most_abundant_x
   else:
      Rmost_x = im2most_abundant_x - im1most_abundant_x
      
   
   if im1most_abundant_y >= im2most_abundant_y:
      bottom_y = im1most_abundant_y - im2most_abundant_y
   else:
      bottom_y = im2most_abundant_y - im1most_abundant_y
   
   # do at least one time or one more time in addition.
   Rmost_x += 2
   bottom_y += 2


   best_match_len = 0
   best_match_pixels = None
   
   for move_right in range( 0, Rmost_x, 2 ):
      cur_im1pixels_right = {}
      im1src_moved_pix_right = {}
      
      cur_im2pixels_right = {}
      im2src_moved_pix_right = {}
      
      if im1most_abundant_x >= im2most_abundant_x:
         # move image2 shape to the right
         for xy in im2pixels:
         
            if int( xy.split(".")[0] ) + move_right >= im_size[0]:
               continue
         
            moved_xy = ( int( xy.split(".")[0] ) + move_right, int( xy.split(".")[1] ) )
            cur_im2pixels_right[ str( moved_xy[0] ) + "." + str( moved_xy[1] ) ] = im2pixels[ xy ]
            
            im2src_moved_pix_right[ str( moved_xy[0] ) + "." + str( moved_xy[1] ) ] = xy
            
         # im1shape does not move
         for xy in im1pixels:
            im1src_moved_pix_right[xy] = xy
            
         cur_im1pixels_right = copy.deepcopy( im1pixels )
         

      else:
         for xy in im1pixels:
         
            if int( xy.split(".")[0] ) + move_right >= im_size[0]:
               continue
         
            moved_xy = ( int( xy.split(".")[0] ) + move_right, int( xy.split(".")[1] ) )
            cur_im1pixels_right[ str( moved_xy[0] ) + "." + str( moved_xy[1] ) ] = im1pixels[ xy ]
            
            im1src_moved_pix_right[ str( moved_xy[0] ) + "." + str( moved_xy[1] ) ] = xy

         cur_im2pixels_right = copy.deepcopy( im2pixels )
         
         # im2shape does not move
         for xy in im2pixels:
            im2src_moved_pix_right[xy] = xy


      for move_down in range( 0, bottom_y, 2 ):
         cur_im1pixels_right_down = {}
         im1src_moved_pix_right_down = {}
         
         cur_im2pixels_right_down = {}
         im2src_moved_pix_right_down = {}
         
         if im1most_abundant_y >= im2most_abundant_y:
         
            for xy in cur_im2pixels_right:
            
               if int( xy.split(".")[1] ) + move_down >= im_size[1]:
                  continue            
            
               moved_topDown_xy = ( int( xy.split(".")[0] ), int( xy.split(".")[1] ) + move_down )
               cur_im2pixels_right_down[ str( moved_topDown_xy[0] ) + "." + str( moved_topDown_xy[1] ) ] = cur_im2pixels_right[ xy ]
               
               moved_right_source_pix = im2src_moved_pix_right[xy]
               im2src_moved_pix_right_down[ str( moved_topDown_xy[0] ) + "." + str( moved_topDown_xy[1] ) ] = moved_right_source_pix
               
               
            for xy in im1src_moved_pix_right:
               im1src_moved_pix_right_down[xy] = im1src_moved_pix_right[xy]
            
            cur_im1pixels_right_down = copy.deepcopy( cur_im1pixels_right )
            
         else:
            for xy in cur_im1pixels_right:

               if int( xy.split(".")[1] ) + move_down >= im_size[1]:
                  continue     

               moved_topDown_xy = ( int( xy.split(".")[0] ), int( xy.split(".")[1] ) + move_down )
               cur_im1pixels_right_down[ str( moved_topDown_xy[0] ) + "." + str( moved_topDown_xy[1] ) ] = cur_im1pixels_right[ xy ] 

               moved_right_source_pix = im1src_moved_pix_right[xy]
               im1src_moved_pix_right_down[ str( moved_topDown_xy[0] ) + "." + str( moved_topDown_xy[1] ) ] = moved_right_source_pix
               
            
            cur_im2pixels_right_down = copy.deepcopy( cur_im2pixels_right )
            
            for xy in im2src_moved_pix_right:
               im2src_moved_pix_right_down[xy] = im2src_moved_pix_right[xy]


         # finished moving shapes. right now, shapes are in the right location to be compared
         
         matched_pixels = set()
         # matching from smaller shape
         if len( cur_im1pixels_right_down ) > len( cur_im2pixels_right_down ):
            smaller_im_shape = cur_im2pixels_right_down
            bigger_im_shape = cur_im1pixels_right_down
         else:
            smaller_im_shape = cur_im1pixels_right_down
            bigger_im_shape = cur_im2pixels_right_down
         

         for xy in smaller_im_shape:
            if xy in bigger_im_shape.keys():
                  
               smaller_shape_color = smaller_im_shape[ xy ]
               bigger_shape_color = bigger_im_shape[ xy ]
                  
               if smaller_shape_color == bigger_shape_color:
                  matched_pixels.add( xy )

         # for debugging purposes, turning current xy form, "x.y" into x,y
         debug_im1pixels = set()
         for xy in smaller_im_shape:
            x = int( xy.split(".")[0] )
            y = int( xy.split(".")[1] )
            debug_im1pixels.add( ( x,y ) )

         debug_im2pixels = set()
         for xy in bigger_im_shape:
            x = int( xy.split(".")[0] )
            y = int( xy.split(".")[1] )
            debug_im2pixels.add( ( x,y ) )        

         #image_functions.cr_im_from_pixels( "test2", "videos/street3/resized/min/", debug_im1pixels, pixels_rgb=(255,0,0) )
         #image_functions.cr_im_from_pixels( "test2", "videos/street3/resized/min/", debug_im2pixels, pixels_rgb=(0,0,255) )
         
         match_condition = False
         if best_match is False:
            if len( matched_pixels ) / len( smaller_im_shape ) >= match_threshold:
               match_condition = True
         elif best_match is True:
            if len( matched_pixels ) > best_match_len:
               match_condition = True
            
         
         if match_condition is True:
            
            # shapes matched. return the source pixels. so convert moved pixels to pixels before moved.
            
            im1matched_source_pixels = set()
            im2matched_source_pixels = set()
            
            # matched_pixels -> {'14.3', '5.3', '4.4', '7.4', ... }
            for xy in matched_pixels:
               if xy in im1src_moved_pix_right_down.keys():
                  str_x = im1src_moved_pix_right_down[ xy ].split(".")[0]
                  str_y = im1src_moved_pix_right_down[ xy ].split(".")[1]
                  
                  int_xy = ( int( str_x ), int( str_y ) )
                  
                  im1matched_source_pixels.add( int_xy )
               
               else:
                  print("ERROR at same_shapes_functions.match_shape_while_moving_it2. im1pixel has to be found")
                  sys.exit()

               if xy in im2src_moved_pix_right_down.keys():
                  str_x = im2src_moved_pix_right_down[ xy ].split(".")[0]
                  str_y = im2src_moved_pix_right_down[ xy ].split(".")[1]
                  
                  int_xy = ( int( str_x ), int( str_y ) )
                  
                  im2matched_source_pixels.add( int_xy )       

               else:
                  print("ERROR at same_shapes_functions.match_shape_while_moving_it2. im2pixel has to be found")
                  sys.exit()

            if best_match is False:
               return ( True, [im1matched_source_pixels, im2matched_source_pixels]  )
            elif best_match is True:
               best_match_len = len( matched_pixels )
               best_match_pixels = [im1matched_source_pixels, im2matched_source_pixels]
   
   
   # if the processing gets here, the found_pixels never reached match threshold value
   if best_match is False:
      return ( False, set() )
   elif best_match is True:
      return best_match_pixels


























































