

import math


# returns Boolean, Boolean, brightness value
# first boolean is color change
# second boolean is within brightness threshold value
# third value is actual brightness change value
def compute_appearance_difference(orig_pix, comp_pix, brit_thres):

   color_ch_threshold = 10
   
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
      
   if clr_change <= color_ch_threshold :
      if average_britch <= brit_thres:
         # color stayed and brightness is within threshold value
         return False, True, average_britch
      else:
         # color stayed but not within threshold value
         return False, False, average_britch
            

   # color changed
   return True, None, None





def get_nbr_pixels(pixel_index, image_size):

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





