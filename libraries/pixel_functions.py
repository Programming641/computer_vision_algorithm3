
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
# pixel_index -> string
# image size contains width and height
# returns list of pixel indexes as integer
def get_nbr_pixels(pixel_index, image_size):

   pixel_index = int( pixel_index )

   # list for storing neighbor index numbers
   neighbors = []
   
   

   # assigning the positions for comparing neighbor pixels. starting with top going clockwise.
   ignore_neighbor_position_dict = { 'top' : False, 'top_right' : False, 'right' : False, 'bottom_right': False, 'bottom': False, 'bottom_left' : False, 'left': False, 'top_left': False }

   y = math.floor(pixel_index / image_size[0])

   x  = pixel_index % image_size[0]
   
   # determining if the current pixel is the leftmost pixel
   # no need to compare with top left, left, bottom left
   if x == 0:
 
      ignore_neighbor_position_dict['top_left'] = True
      ignore_neighbor_position_dict['left'] = True
      ignore_neighbor_position_dict['bottom_left'] = True
    
   # determing the first row
   # no need to compare with top left, top, top right
   if pixel_index <= image_size[0] -1:
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
      top_neighbor = pixel_index - image_size[0]
      neighbors.append(top_neighbor)


   if ignore_neighbor_position_dict['top_right'] == False:     
      top_right_neighbor = pixel_index - image_size[0] + 1
      neighbors.append(top_right_neighbor)


   if ignore_neighbor_position_dict['right'] == False:  
      right_neighbor = pixel_index + 1
      neighbors.append(right_neighbor)

   if ignore_neighbor_position_dict['bottom_right'] == False:
      bottom_right_neighbor = pixel_index + image_size[0] + 1
      neighbors.append(bottom_right_neighbor)      

   if ignore_neighbor_position_dict['bottom'] == False:
      bottom_neighbor = pixel_index + image_size[0]
      neighbors.append(bottom_neighbor)   

   if ignore_neighbor_position_dict['bottom_left'] == False:    
      bottom_left_neighbor = pixel_index + image_size[0] - 1 
      neighbors.append(bottom_left_neighbor) 

   if ignore_neighbor_position_dict['left'] == False:   
      left_neighbor =    pixel_index - 1
      neighbors.append(left_neighbor) 

   if ignore_neighbor_position_dict['top_left'] == False:  
      top_left_neighbor =  pixel_index - image_size[0] - 1
      neighbors.append(top_left_neighbor) 

   return neighbors


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





























