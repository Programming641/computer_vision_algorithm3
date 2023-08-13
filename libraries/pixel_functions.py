
import sys
import math


# returns Boolean, Boolean, brightness value
# first boolean is color change
# second boolean is within brightness threshold value
# third value is actual brightness change value
def compute_appearance_difference(orig_pix, comp_pix, brit_thres, clr_thres=None, get_values=None):

   if not clr_thres:
      color_ch_threshold = 10
   else:
      color_ch_threshold = clr_thres
   
   if type(orig_pix) is dict and type(comp_pix) is dict:
      red_difference = orig_pix['r'] - comp_pix['r']
      green_difference = orig_pix['g'] - comp_pix['g']
      blue_difference = orig_pix['b'] - comp_pix['b']
  
   elif type(orig_pix) is tuple and type(comp_pix) is tuple:
      red_difference = orig_pix[0] - comp_pix[0]
      green_difference = orig_pix[1] - comp_pix[1]
      blue_difference = orig_pix[2] - comp_pix[2]      

  
   if red_difference >= 0:
      if green_difference >= 0:
         rg_diff = abs( red_difference - green_difference )
      else:
         # red_difference is 0 or positive, green_difference is negative
         rg_diff = abs(green_difference) + red_difference
        
      if blue_difference >= 0:
         # red_difference is 0 or positive, blue_difference is also 0 or positive
         rb_diff = abs( red_difference - blue_difference )
      else:
         # red_difference is 0 or positive, blue_difference is negative
         rb_diff = abs(blue_difference) + red_difference
   else:
      if green_difference >= 0:
         # red_difference is negative and green_difference is 0 or positive
         rg_diff = abs(red_difference) + green_difference
      else:
         # red_difference is negative and green_difference is negative
         rg_diff = abs( red_difference - green_difference )
     
      if blue_difference >= 0:
         # red_difference is negative and blue_difference is 0 or positive
         rb_diff = abs(red_difference) + blue_difference
      else:
         # red_difference is negative and blue_difference is negative
         rb_diff = abs( red_difference - blue_difference )
   
   
   if green_difference >= 0:
      if blue_difference >= 0:
         gb_diff = abs( green_difference - blue_difference )
      else:
         # green_difference is 0 or positive and blue_difference is negative
         gb_diff = abs(blue_difference) + green_difference
   else:
      if blue_difference >= 0:   
         # green_difference is negative and blue_difference is 0 or positive
         gb_diff = abs(green_difference) + blue_difference
      else:
         # green_difference is negative and blue_difference is negative
         gb_diff = abs( green_difference - blue_difference )

   
   clr_change = rg_diff + rb_diff + gb_diff

      
   # this should be applied only if color change did not happen. average brightness change
   average_britch = ( abs(red_difference) + abs(green_difference) + abs(blue_difference) ) / 3      
   
   if get_values:
      return clr_change, average_britch
   
   if clr_change <= color_ch_threshold :
      if average_britch <= brit_thres:
         # color stayed and brightness is within threshold value
         return False, True, average_britch
      else:
         # color stayed but not within threshold value
         return False, False, average_britch
            

   # color changed
   return True, None, None




# in parameters
# param_pixel -> string
# image size contains width and height
# returns list of pixel indexes as integer
def get_nbr_pixels(param_pixel, image_size, convert2xy=False, input_xy=False):

   # list for storing neighbor index numbers
   neighbors = []
   

   # assigning the positions for comparing neighbor pixels. starting with top going clockwise.
   ignore_neighbor_position_dict = { 'top' : False, 'top_right' : False, 'right' : False, 'bottom_right': False, 'bottom': False, 'bottom_left' : False, 'left': False, 'top_left': False }

   if input_xy is False:
      param_pixel = int( param_pixel )
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
   sys.exit()



# xy -> ( x, y ) x and y are integers
# return pixel_index. pixel_index is integer
def convert_xy_to_pindex( xy, im_width ):
   pixel_index = xy[1] * im_width + xy[0]
   
   return pixel_index

def convert_pindex_to_xy( pindex, im_width ):
   y = math.floor( int(pindex) / im_width)
   x  = int(pindex) % im_width 

   return ( x,y )




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






























