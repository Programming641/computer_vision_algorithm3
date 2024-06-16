
import sys
import math
import copy
from libraries import image_functions


# return True if appearance changed, False if appearance did not change
def compute_appearance_difference(orig_pix, comp_pix, threshold=20 ):
   
   assert type(orig_pix) is tuple and type(comp_pix) is tuple
   
   red_difference = abs( orig_pix[0] - comp_pix[0] )
   green_difference = abs( orig_pix[1] - comp_pix[1] )
   blue_difference = abs( orig_pix[2] - comp_pix[2] )    

   total_diff = red_difference + green_difference + blue_difference
   
   if total_diff > threshold:
      return True
   else:
      return False
   




# in parameters
# param_pixel -> pixel index
# image size contains width and height
# returns list of pixel indexes as integer
def get_nbr_pixels(param_pixel, image_size, convert2xy=False, input_xy=False):

   # list for storing neighbor index numbers
   neighbors = []
   

   # assigning the positions for comparing neighbor pixels. starting with top going clockwise.
   ignore_neighbor_position_dict = { 'top' : False, 'top_right' : False, 'right' : False, 'bottom_right': False, 'bottom': False, 'bottom_left' : False, 'left': False, 'top_left': False }

   if input_xy is False:
      x  = param_pixel % image_size[0]
      y = math.floor(param_pixel / image_size[0])

   elif input_xy is True:
      x = param_pixel[0]
      y = param_pixel[1]
   
   
   # determining if the current pixel is the leftmost pixel
   # no need to compare with top left, left, bottom left
   if x == 0:
 
      ignore_neighbor_position_dict['top_left'] = True
      ignore_neighbor_position_dict['left'] = True
      ignore_neighbor_position_dict['bottom_left'] = True
    
   # determing the first row
   # no need to compare with top left, top, top right
   if y == 0:
      ignore_neighbor_position_dict['top_left'] = True
      ignore_neighbor_position_dict['top'] = True
      ignore_neighbor_position_dict['top_right'] = True  

   # determining the rightmost pixel. x counts from 0 to width - 1
   # no need to compare with top right, right, bottom right
   if x == image_size[0] - 1:
      ignore_neighbor_position_dict['top_right'] = True
      ignore_neighbor_position_dict['right'] = True
      ignore_neighbor_position_dict['bottom_right'] = True

   # determining last row . y counts from 0 to height - 1
   # no need to compare with bottom left, bottom, bottom right
   if y == image_size[1] - 1:
      ignore_neighbor_position_dict['bottom_left'] = True
      ignore_neighbor_position_dict['bottom'] = True
      ignore_neighbor_position_dict['bottom_right'] = True

   if ignore_neighbor_position_dict['top'] == False:   
      if input_xy is False:
         top_neighbor = param_pixel - image_size[0]
      elif input_xy is True:
         top_neighbor = ( x, y - 1 )
      
      if convert2xy is False:
         neighbors.append(top_neighbor)
      else:
         xy = convert_pindex_to_xy( top_neighbor, image_size[0] )
         neighbors.append( xy )


   if ignore_neighbor_position_dict['top_right'] == False:  
      if input_xy is False:   
         top_right_neighbor = param_pixel - image_size[0] + 1
      elif input_xy is True:
         top_right_neighbor = ( x + 1, y - 1 )
         
      if convert2xy is False:
         neighbors.append(top_right_neighbor)
      else:
         xy = convert_pindex_to_xy( top_right_neighbor, image_size[0] )
         neighbors.append( xy )
      


   if ignore_neighbor_position_dict['right'] == False:  
      if input_xy is False:
         right_neighbor = param_pixel + 1
      elif input_xy is True:
         right_neighbor = ( x + 1, y )
         
      if convert2xy is False:
         neighbors.append(right_neighbor)
      else:
         xy = convert_pindex_to_xy( right_neighbor, image_size[0] )
         neighbors.append( xy )
      

   if ignore_neighbor_position_dict['bottom_right'] == False:
      if input_xy is False:
         bottom_right_neighbor = param_pixel + image_size[0] + 1
      elif input_xy is True:
         bottom_right_neighbor = ( x + 1, y + 1 )
         
      if convert2xy is False:
         neighbors.append(bottom_right_neighbor)
      else:
         xy = convert_pindex_to_xy( bottom_right_neighbor, image_size[0] )
         neighbors.append( xy )
     

   if ignore_neighbor_position_dict['bottom'] == False:
      if input_xy is False:
         bottom_neighbor = param_pixel + image_size[0]
      elif input_xy is True:
         bottom_neighbor = ( x, y + 1 )
         
      if convert2xy is False:
         neighbors.append(bottom_neighbor)
      else:
         xy = convert_pindex_to_xy( bottom_neighbor, image_size[0] )
         neighbors.append( xy )


   if ignore_neighbor_position_dict['bottom_left'] == False:  
      if input_xy is False:   
         bottom_left_neighbor = param_pixel + image_size[0] - 1
      elif input_xy is True:
         bottom_left_neighbor = ( x - 1, y + 1 )
         
      if convert2xy is False:
         neighbors.append(bottom_left_neighbor)
      else:
         xy = convert_pindex_to_xy( bottom_left_neighbor, image_size[0] )
         neighbors.append( xy )

   if ignore_neighbor_position_dict['left'] == False:
      if input_xy is False:   
         left_neighbor =    param_pixel - 1
      elif input_xy is True:
         left_neighbor = ( x - 1, y )
         
      if convert2xy is False:
         neighbors.append(left_neighbor)
      else:
         xy = convert_pindex_to_xy( left_neighbor, image_size[0] )
         neighbors.append( xy )

   if ignore_neighbor_position_dict['top_left'] == False:
      if input_xy is False:
         top_left_neighbor =  param_pixel - image_size[0] - 1
      elif input_xy is True:
         top_left_neighbor = ( x - 1, y - 1 )
      
      if convert2xy is False:
         neighbors.append(top_left_neighbor)
      else:
         xy = convert_pindex_to_xy( top_left_neighbor, image_size[0] )
         neighbors.append( xy ) 

   return neighbors



# param_pixels -> { pixel indexes } or { pixel xyes }
def find_shapes( param_pixels, im_size  ):

   if type( list(param_pixels)[0] ) is tuple:
      # convert xy to indexes
      param_pixels_cp = copy.deepcopy( param_pixels )
      param_pixels = set()
      for pixel in param_pixels_cp:
         pindex = convert_xy_to_pindex( pixel, im_size[0] )
         
         param_pixels.add( pindex )
   

   #image_functions.cr_im_from_pixels( "1", directory, param_pixels )


   # [ { pixel index: shapeid }, ... ]
   # already_added_pixels is divided into indexes solely for speed!
   # each list index contains 1000 pixel indexes. for example, list index 0: pixel indexes up to 999. list index 1 1000 to 1999.
   # list index 2 contains 2000 up to 2999. and so on.
   already_added_pixels = [ ]
   dividing_num = 100

   # initialize already_added_pixels
   total_image_pixels_len = im_size[0] * im_size[1]
   index_needed_for_Alrdy_A_P = total_image_pixels_len / dividing_num
   for needed_index in range( math.ceil(index_needed_for_Alrdy_A_P) ):
      already_added_pixels.append( {} )




   result_shapes_pixels = {}
   for pixel in param_pixels:
      cur_pixel_shapeid = None

      # check if current pixel is in other pixel's shapes.
      already_added_pix_index = math.floor( pixel / dividing_num ) 
      if already_added_pixels[already_added_pix_index].get( pixel ):
         cur_pixel_shapeid = already_added_pixels[already_added_pix_index][ pixel ]
         result_shapes_pixels[ cur_pixel_shapeid ].add( pixel )

      if cur_pixel_shapeid is None:
         cur_pixel_shapeid = pixel
         result_shapes_pixels[ cur_pixel_shapeid ] = set()
         result_shapes_pixels[ cur_pixel_shapeid ].add( cur_pixel_shapeid )
         
         
         already_added_pixels[already_added_pix_index][ cur_pixel_shapeid ] = cur_pixel_shapeid
      
      
      # neighbor_pixels -> [544, 545, 1085, 1625, 1624, 1623, 1083, 543]
      neighbor_pixels = get_nbr_pixels( pixel, im_size )
   
      nbr_pixels_in_param_pixels = set( neighbor_pixels ).intersection( param_pixels )
      
      if len( nbr_pixels_in_param_pixels ) >= 1:
         found = False
         for nbr_pixels_in_param_pixel in nbr_pixels_in_param_pixels:

            # check if this neighbor is already in the shape
            already_added_pix_index = math.floor( nbr_pixels_in_param_pixel / dividing_num ) 
            if already_added_pixels[already_added_pix_index].get(nbr_pixels_in_param_pixel):
               cur_nbr_containing_shapeid = already_added_pixels[already_added_pix_index][nbr_pixels_in_param_pixel]
               result_shapes_pixels[ cur_nbr_containing_shapeid ].add( nbr_pixels_in_param_pixel )
               
               if cur_nbr_containing_shapeid != cur_pixel_shapeid:
                  
                  # updating all pixels from cur_pixel_shapeid in already_added_pixels
                  for _pixel in result_shapes_pixels[ cur_pixel_shapeid ]:
                     already_added_pix_index = math.floor( _pixel / dividing_num ) 
                     already_added_pixels[already_added_pix_index][_pixel] = cur_nbr_containing_shapeid

                  result_shapes_pixels[ cur_nbr_containing_shapeid ] |= result_shapes_pixels[ cur_pixel_shapeid ]                  
                  result_shapes_pixels.pop( cur_pixel_shapeid )    

                  cur_pixel_shapeid = cur_nbr_containing_shapeid

            else:
               result_shapes_pixels[ cur_pixel_shapeid ].add( nbr_pixels_in_param_pixel ) 
               
               already_added_pixels[already_added_pix_index][nbr_pixels_in_param_pixel] = cur_pixel_shapeid



   return result_shapes_pixels




# input parameters
# xy -> ( 190, 30 )
# vicinity_value is how many pixels for the pixel to be expanded.
# image_size -> image_size[0] is image width, image_size[1] is image height
def get_vicinity_pixels( xy, vicinity_value, image_size ):

   vicinity_pixels = [xy]
   
   for expanded_value in range( 1, vicinity_value + 1 ):
      # add if pixel is out of range of image size
      no_need2add = []
      
      upLeft =   ( xy[0] - expanded_value , xy[1] - expanded_value )
      upRight =  ( xy[0] + expanded_value , xy[1] - expanded_value )
      downRight = ( xy[0] + expanded_value , xy[1] + expanded_value )
      downLeft =  ( xy[0] - expanded_value , xy[1] + expanded_value )

      if xy[1] - expanded_value < 0:
         no_need2add.append('up')
      if xy[0] + expanded_value >= image_size[0]:
         no_need2add.append('right')
      if xy[1] + expanded_value >= image_size[1]:
         no_need2add.append('down')
      if xy[0] - expanded_value < 0:
         no_need2add.append('left')
      
      if "up" not in no_need2add:
         # if up is in no_need2add, then no need to add any of the up pixels at all.
         for upL2upR in range( upLeft[0] + 1, upRight[0] ):
            # keep addng pixel to the right until upRight x.
            # as I move to the right, make sure that pixel is within the image width and expanded upLeft is within image width
            if upL2upR < image_size[0] and upL2upR >= 0:
               vicinity_pixels.append( ( upL2upR, upLeft[1] ) )
            
      if "right" not in no_need2add:
         # if right is in no_need2add, then there is no need to add any of the pixels between "up right to down right" at all.
         for upR2downR in range( upRight[1] + 1, downRight[1] ):
            # y + upR2downR.
            # as I move down, make sure that the pixel is still within the image height and upRight is within image height
            if  upR2downR < image_size[1] and upR2downR >= 0:

               vicinity_pixels.append( ( upRight[0], upR2downR ) )
      
      if "down" not in no_need2add:
         for downL2downR in range( downLeft[0] + 1, downRight[0] ):
            # x + downL2downR
            if downL2downR < image_size[0] and downL2downR >= 0:
               vicinity_pixels.append( ( downL2downR, downLeft[1] ) )
      
      if "left" not in no_need2add:
         for upL2downL in range( upLeft[1] + 1, downLeft[1] ):
            # y + upL2downL
            if upL2downL < image_size[1] and upL2downL >= 0:
               vicinity_pixels.append( ( upLeft[0], upL2downL ) )

   
   return vicinity_pixels


# pixel_xy -> ( x, y ) x and y are both integers
def get_pixel_im_area(pixel_xy, image_areas):
   # im_area -> one image area. example -> {1: {'left': 0, 'right': 71, 'top': 0, 'bottom': 40}}
   for im_area in image_areas:
      # im_area_lrtb -> image area's left right top bottom. {'left': 0, 'right': 71, 'top': 0, 'bottom': 40}
      for im_area_lrtb in im_area.values():
         # check if pixel's x position is between the current image area's left and right values
         if pixel_xy[0] >= im_area_lrtb["left"] and pixel_xy[0] <= im_area_lrtb["right"]:
            # check if pixel's y position is between the current image area's top and bottom values
            if pixel_xy[1] >= im_area_lrtb["top"] and pixel_xy[1] <= im_area_lrtb["bottom"]:
            
               return im_area

  
   print("ERROR at pixel_functions.get_pixel_im_area. pixel_xy has to be in one of the image areas" )
   sys.exit(1)



# xy -> ( x, y ) x and y are integers
# return pixel_index. pixel_index is integer
def convert_xy_to_pindex( xy, im_width ):
   pixel_index = xy[1] * im_width + xy[0]
   
   return pixel_index

def convert_pindex_to_xy( pindex, im_width ):
   y = math.floor( pindex / im_width)
   x  = pindex % im_width 

   return ( x,y )


def get_pindex_with_xy_input( pindex, xy, im_width ):
   result_pindex = pindex + xy[0] + ( xy[1] * im_width )

   return result_pindex


# get pixels positions in pixel coordinate and not image coordinate
#
# pixels -> { (x,y), ... } or list of xy
# 
# shapes_colors is the one returned by get_all_shapes_colors
# 
# returns list of (x,y).   [ ( x,y ), ... ]
# x,y and r,g,b are all integers
def get_pixels_pos_in_pix_coord( pixels ): 
      
   smallest_x = min( [ xy[0] for xy in pixels ] )
   smallest_y = min( [ xy[1] for xy in pixels ] )

   pixel_coords = [ (xy[0] - smallest_x, xy[1] - smallest_y ) for xy in pixels ]

   return pixel_coords


# pixels -> [ (x,y), .... ] or set of xy. of pixels are provided in indexes, then im_width has to be present.
# move_x or move_y.   postive value. 1,2,3,4.... move right or down 1,2,3,4..... negative value -> -1,-2,-3,... move left or up 1,2,3,...
def move_pixels( pixels, move_x, move_y, input_xy=True, im_width=None ):
   moved_pixels = set()
   
   if input_xy is True:
      for pixel in pixels:
         x = pixel[0] + move_x
         y = pixel[1] + move_y
   
         moved_pixels.add( (x,y) )
   
   else:
      for pindex in pixels:
         result_pindex = get_pindex_with_xy_input( pindex, (move_x, move_y), im_width )
         moved_pixels.add( result_pindex )
   
   return moved_pixels
      

# src_pixels and whole_pixels data format: set or list of (x,y)
# pixels to start getting connected pixels are from src_pixels. connected pixels are from whole_pixels
def get_connected_pixels( src_pixels, whole_pixels, image_size, input_xy=True ):
   
   #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", whole_pixels, pixels_rgb=(0,0,255) )

   sys.setrecursionlimit(5000)
   
   if type(src_pixels) is list:
      src_pixels = set( src_pixels )
   if type(whole_pixels) is list:
      whole_pixels = set( whole_pixels )

   def traverse_all_neighbors( starting_pixel, connected_pixels, first=False ):

      if first is True:
         connected_pixels.add(starting_pixel)
      
      if input_xy is True:
         # [(188, 145), (189, 145), ... ]
         nbr_pixels = get_nbr_pixels(starting_pixel, image_size, input_xy=True)     
      else:
         nbr_pixels = get_nbr_pixels(starting_pixel, image_size )          
      
      nbr_pixels = set(nbr_pixels)
      
      already_done_pix = nbr_pixels.intersection( connected_pixels )

      nbr_pix_from_whole_pix = nbr_pixels.intersection( whole_pixels )
      
      will_traverse_pixels = nbr_pix_from_whole_pix.difference( already_done_pix )
      
      connected_pixels |= will_traverse_pixels

      #image_functions.cr_im_from_pixels( "26", "videos/street3/resized/min1/", will_traverse_pixels, pixels_rgb=(0,255,255) )
      
      for nbr_pix in will_traverse_pixels:
         traverse_all_neighbors( nbr_pix, connected_pixels )
      
      return connected_pixels


   already_done_pixels = set()
   all_connected_pixels = []
   for src_pixel in src_pixels:
      if src_pixel in already_done_pixels:
         continue
      
      cur_conn_pixels = traverse_all_neighbors( src_pixel, set(), first=True )
      all_connected_pixels.append( cur_conn_pixels )
      
      already_done_pixels |= cur_conn_pixels
      

   return all_connected_pixels

































