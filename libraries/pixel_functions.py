
'''
Example of use.

total_appearance_difference_threshold = 20

appearance_difference = compute_appearance_difference(current_pixel_shape_RGB, top_pixel_RGB)

# check to see if total appearance difference value is within the threshold. if so, this neighbor pixel will be put in current pixel's shape          
if total_appearance_difference_threshold - appearance_difference >= 0:
   # appearance did not change more than threshold value


'''
def compute_appearance_difference(current_pix, compare_pixel):

   if len(current_pix) == 3 and len(compare_pixel) == 3:
      original_red, original_green, original_blue = current_pix
      compare_red, compare_green, compare_blue = compare_pixel
   else:
      original_red, original_green, original_blue, alpha = current_pix
      compare_red, compare_green, compare_blue, alpha = compare_pixel      
    
    
   red_difference = abs(original_red - compare_red)
   green_difference = abs(original_green - compare_green)
   blue_difference = abs(original_blue - compare_blue)
    
   total_difference = red_difference + green_difference + blue_difference

   average = total_difference / 3

   # exclude 0 or negative values because 0 or negative values mean that difference is smaller than average.
   red_how_far = exclude_negative_Num( red_difference - average )
   green_how_far = exclude_negative_Num( green_difference - average )
   blue_how_far = exclude_negative_Num( blue_difference - average )

   total_appearance_difference = total_difference + red_how_far * 1.3 + green_how_far * 1.3 + blue_how_far * 1.3

   return total_appearance_difference





def exclude_negative_Num(num):

   if num > 0:
      return num
   else:
      return 0



def find_brightness_change(current_shape_id_color, current_neighbor_color, brightness_threshold):

   all_positive = False
   all_negative = False
   
   if type(current_shape_id_color) is dict and type(current_neighbor_color) is dict:
      red_difference = current_shape_id_color['r'] - current_neighbor_color['r']
      green_difference = current_shape_id_color['g'] - current_neighbor_color['g']
      blue_difference = current_shape_id_color['b'] - current_neighbor_color['b']
  
   elif type(current_shape_id_color) is tuple and type(current_neighbor_color) is tuple:
      red_difference = current_shape_id_color[0] - current_neighbor_color[0]
      green_difference = current_shape_id_color[1] - current_neighbor_color[1]
      blue_difference = current_shape_id_color[2] - current_neighbor_color[2]      
  
  
  
  
   # make sure that all signs are the same otherwise it is considered color change
   # checking here for all positive signs
   if red_difference > 0 and green_difference > 0 and blue_difference > 0:
      all_positive = True
  
   # checking here for all negative signs
   if red_difference < 0 and green_difference < 0 and blue_difference < 0:
      all_negative = True
  

   # proceed to process if different signs are not present
   if all_negative == True or all_positive == True:
     
      average_difference = ( abs(red_difference) + abs(green_difference) + abs(blue_difference) ) / 3
      
      red_difference = average_difference - abs(red_difference)
      green_difference = average_difference - abs(green_difference)
      blue_difference = average_difference - abs(blue_difference)
      
      total_difference = abs(red_difference) + abs(green_difference) + abs(blue_difference)
      
      if total_difference <= brightness_threshold:
         # current neighbor has the brightness change from the current running shape
         return True


   return False





