
from libraries import pixel_shapes_functions, read_files_functions, pixel_functions, image_functions
from libraries.cv_globals import third_smallest_pixc

from PIL import Image
import math
import os, sys
import copy




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




#
#
# what is different from find_shapes_match.
# find_shapes_match only checks if the image1 shape's pixels can be found in the same positions as image2 shape's
#
# in this function, it also considers not found pixels. if the image2 shape's pixels can't be found, then it looks at the 
# image1's original image pixels and checks if image2 shape's pixels can be found in the same locations.
#
# target_im_shapes -> {'5588': [(128, 128, 128), (10, 13), (10, 12), ... }
#                     { shapeid: [ shape color , (x,y), (x,y), ... ], ... }
# ano_im_shapes same as target_im_shapes
# 
# above data form is the one that returned by pixel_shapes_functions.get_shapes_pos_in_shp_coord
#
# im1smallest_xy is one returned by pixel_shapes_functions.get_shapes_pos_in_shp_coord
# [ ( image1 smallest x, image1 smallest y ), ( image2 smallestx, image2 smallest y ) ]
# 
# im1data -> list containing image 1 and 2 data
# example ->  [ image1data, image2data ]
# image data is one that is obtained from pillow image object.getdata()
def find_shapes_match2( target_im_shapes, ano_im_shapes, shapeid, im1smallest_xy, im1data, image_size, im1shapes ):
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
      
      extra_im1shapes = []
      
      im_total_match_count = 0
      for t_im_shape in target_im_shapes:
         cur_highest_match_count = 0
         
         cur_im_s_color = target_im_shapes[t_im_shape].pop(0)
         cur_im_s_pixels = set( target_im_shapes[t_im_shape] )
         
         cur_extra_im1shapes = []
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
              
              else:
                 # current image1 shape pixels did not match the current image2 shape's pixels.
                 # check if image2 shape's pixels can be found from other image1 shapes pixels in the same locations
                 # first, get not matched pixels
                 im2nfnd_pix_in_im1 = ano_im_s_pixels.difference( cur_im_s_pixels )
                 
                 # check if not found pixels are 60% or more of the current image1 shape's pixels
                 if len( im2nfnd_pix_in_im1 ) / len( cur_im_s_pixels ) > 0.6:
                    # image2 pixels are in image2 shape's coordinate. I need to get image1's pixels in the same locations as 
                    # image2 shape's coordinate
                    im2pixels_in_im1coord = [ (pixel[0] + im1smallest_xy[0], pixel[1] + im1smallest_xy[1] ) for pixel in im2nfnd_pix_in_im1 ]
                    
                    # convert xy to pindex
                    im2pixels_in_im1coord_pindex = []
                    for xy in im2pixels_in_im1coord:
                       if xy[0] < 0 or xy[0] >= image_size[0] or xy[1] < 0 or xy[1] >= image_size[1]:
                          # current xy is out of image range
                          continue
                       pindex = pixel_functions.convert_xy_to_pindex( xy, image_size[0] )
                       im2pixels_in_im1coord_pindex.append( pindex )
                       
                    
                    matched_pixels = []
                    # now that pixels are in image1's image coordinate, check if pixels match
                    for im2pixel_in_im1coord in im2pixels_in_im1coord_pindex:

                       if im1data[ im2pixel_in_im1coord ] == ano_im_s_color:
                          matched_pixels.append( im2pixel_in_im1coord )
                    
                    # match is found for current image1 shape and image2 shape
                    # I need to get image1 shapes that matched
                    matched_im1shapes = {}
                    for pixel in matched_pixels:
                       for shapeid in im1shapes:
                          if str(pixel) in im1shapes[shapeid]:
                             if shapeid in matched_im1shapes.keys():
                                matched_im1shapes[shapeid].append( str(pixel) )
                             else:
                                matched_im1shapes[shapeid] = [ str(pixel) ]
                             
                             break
                          
                    matched_count = 0                          
                    for shapeid in matched_im1shapes:
                       if len( matched_im1shapes[shapeid] ) / len( im1shapes[shapeid] ) >= 0.4:
                          matched_count += len( matched_im1shapes[shapeid] )
                          cur_extra_im1shapes.append( shapeid )
                          
                    if matched_count > 0 and matched_count / len( target_im_shapes[t_im_shape] ) >= 0.4:
                       if matched_count > cur_highest_match_count:
                          cur_highest_match_count = matched_count
                          
                          extra_im1shapes.extend( cur_extra_im1shapes )
                          
                          print("extra_im1shapes found")
                          
                    #image_functions.cr_im_from_pixels( "12", "videos/street3/resized/min/", im2nfnd_pix_in_im1, save_filepath=None , pixels_rgb=(255, 255, 0 ) )
                    #image_functions.cr_im_from_pixels( "12", "videos/street3/resized/min/", im2pixels_in_im1coord, save_filepath=None , pixels_rgb=(0, 255, 0 ) )
                    #sys.exit()
                 
         
            ano_im_shapes[ano_im_shape].insert(0, ano_im_s_color )
            
         # at the end of current image1 shape
         im_total_match_count += cur_highest_match_count
         
         target_im_shapes[t_im_shape].insert( 0, cur_im_s_color )
               


      if im_total_match_count / im1shapes_total > 0.6:
         # match found
         
         im1shapes_matches = []
         im1shapes_matches.extend( extra_im1shapes )
         im1shapes_matches.extend( list(target_im_shapes.keys()) )
         
         match[0].extend( im1shapes_matches )
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
def match_shape_while_moving_it( im1pixels, im2pixels ):

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
         
         if len( found_pixels ) / len( cur_im1pixels ) >= 0.5:
            #image_functions.cr_im_from_pixels( "12", "videos/street3/resized/min/", cur_im1pixels, save_filepath=None , pixels_rgb=(255,0,0) )
            #image_functions.cr_im_from_pixels( "12", "videos/street3/resized/min/", cur_im2pixels, save_filepath=None , pixels_rgb=(255,0,0) )
            
            return True
   
   # if the processing gets here, the found_pixels never reached match threshold value
   return False


# param_shapes
# list of tuple image1 shape and image2 shape
# [ ( image1 shapeid, image2 shapeid ), ... ]
# tuple can be list also.
# outer list can also be set.
# list of tuple or set of tuple or list of list.
#
# returns verified_shapes
# { ( image1 shapeid, image2 shapeid ), ... }
def verify_matches( param_shapes, im_shapes, im_colors, im_neighbors, im_width ):

   verified_shapes = set()

   progress_counter = len( param_shapes )
   for each_shapes in param_shapes:
      print( str( progress_counter ) + " remaining")
      progress_counter -= 1

      if each_shapes[0] != "73262":
         continue
         
      # neighbor match counting needs to be done from smaller shape.
      total_neighbors = 0
      if len( each_shapes[0] ) > len( each_shapes[1] ):
         for im1nbr in im_neighbors[0][each_shapes[0]]:
            if len( im_shapes[0][im1nbr] ) < third_smallest_pixc:
               continue
            total_neighbors += 1
      else:
         for im2nbr in im_neighbors[1][each_shapes[1]]:
            if len( im_shapes[1][im2nbr] ) < third_smallest_pixc:
               continue
            total_neighbors += 1
            
      
      print("total_neighbors " + str( total_neighbors ) )
      if total_neighbors < 3:
         # insufficient number of neighbors for judging the match
         continue

      cur_nbr_match_counter = 0
      matched = False
      matched_im2neighbors = []
      for im1nbr in im_neighbors[0][each_shapes[0]]:
         if len( im_shapes[0][im1nbr] ) < third_smallest_pixc:
            continue
         
         for im2nbr in im_neighbors[1][each_shapes[1]]:
         
            if len( im_shapes[1][im2nbr] ) < third_smallest_pixc and im2nbr in matched_im2neighbors:
               continue
               
            if im_colors[0][im1nbr] != im_colors[1][im2nbr]:
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
            
            
            # [(12, 15), (11, 15), ... ]
            im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[0][im1nbr], im_width, param_shp_type=0 )  
            im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im_shapes[1][im2nbr], im_width, param_shp_type=0 )
            
            # match from smaller shape
            if im1shapes_total > im2shapes_total:
               im1_im2_nbr_match = match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy )
            else:
               im1_im2_nbr_match = match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy )
            if im1_im2_nbr_match is True:     
               print("matched im1nbr " + im1nbr + " im2nbr " + im2nbr )
               cur_nbr_match_counter += 1
               matched_im2neighbors.append( im2nbr )
            
               if cur_nbr_match_counter >= 1 and cur_nbr_match_counter / total_neighbors >= 0.35:
                  verified_shapes.add( (each_shapes[0], each_shapes[1]) )
                  matched = True
                  break
            
         if matched is True:
            break


   return verified_shapes




















































