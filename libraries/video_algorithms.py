
from PIL import Image
import os
import math



# called from find_shapes_in_diff_frames
# this method is for comparing and finding same shape in different frames of video.

# I copied code from find_shapes_in_diff_frames for getting pixels in current row (y) so it is horrible
# but I stick with it for now. fix it later when I get time or feel the need.

# return is the result of comparison. return is dictionary with following form
# search_ended, single_pixel_count_match, matched_x, matched_y, matched_pixel_count, empty_matched_x, empty_matched_y
# search_ended is boolean. single_pixel_count_match's value is boolean. matched_x, y, count are values where original pixels matched.

def compare_w_shape(compare_pixels_dict, search_until, original_count_from_top, original_pixels_in_current_y, original_empty_pixels_in_current_y):


   compare_smallest_y = min(int(d['y']) for d in compare_pixels_dict.values())
   compare_largest_y = max(int(d['y']) for d in compare_pixels_dict.values())


   # if original pixel and compare pixels are more than pixel_count_threshold amount apart, then skip this row
   #pixel_count_threshold = count + 2 + round( count * 0.1 )
   # this calculation ensures that small value gets enough threshold. Threshold values only gradually increase for larger values.
   
   comparison_result = []
   comparison_empty_result = []
   
   # as we go down from top original pixels to the bottom pixels, the rows in original shape to be compared will decrease. so we need to increase the rows of pixels to be compared in 
   # comparing shape.
   search_until += original_count_from_top


   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(compare_smallest_y, compare_largest_y + 1):
   

      if search_until == 0:

         return comparison_result, comparison_empty_result
         
   
      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in compare_pixels_dict  if (int(compare_pixels_dict[k]['y'])) == y]
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y_values:
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(compare_pixels_dict[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
         
         
      rightMost_x = max( x_values_list_in_current_y )       
      
      
      pixels_in_current_y = []
      empty_pixels_in_current_y = []
         
         
      
      # this is for getting the largest x value in current running y. largest x value is the last one in current running y because
      # x values are sorted from smallest to largest
      x_counter_in_current_running_y = 1
      
      consecutive_x_counter = 0
      
      x_numbers_in_current_running_y = len(x_values_list_in_current_y)

      first = True

         
      for x_value in x_values_list_in_current_y:
      
         # is this the first x value?
         if first != False:
            consecutive_x_counter +=1

            temp = {}
            temp['start_x'] = x_value
            temp['start_y'] = y


            prev_x_value = x_value 
            first = False     
            # for this row(y), there is only one pixel?
            if x_counter_in_current_running_y == x_numbers_in_current_running_y:

               temp['count'] =  consecutive_x_counter
               pixels_in_current_y.append( temp )
               
               for original_pixels_dict in original_pixels_in_current_y:
               
                  pixel_count_threshold = pixels_in_current_y[0]['count'] + 1 + round( pixels_in_current_y[0]['count'] * 0.1 )
                  minus_pixel_count_threshold = pixels_in_current_y[0]['count'] - 1 - round( pixels_in_current_y[0]['count'] * 0.1 )
   
                  if original_pixels_dict.get('original_count') <= pixel_count_threshold and  original_pixels_dict.get('original_count') >= minus_pixel_count_threshold:
                  
                     temp = {}
                     

                     temp['single_pixel_count_match'] = True
                     temp['matched_x'] = pixels_in_current_y[0]['start_x']
                     temp['matched_y'] = pixels_in_current_y[0]['start_y']                           
                     temp['matched_pixel_count'] = pixels_in_current_y[0]['count']

                     comparison_result.append(temp)

               

               break

            x_counter_in_current_running_y += 1            
            continue
  
         # checking to see if x value is the last one in current running y
         if x_counter_in_current_running_y == x_numbers_in_current_running_y:

            temp['count'] =  consecutive_x_counter + 1
            pixels_in_current_y.append( temp )

            # check if there is empty pixels in either one of shapes
            if len(original_empty_pixels_in_current_y) > 0:
               # row (y) in original shape contains empty pixels
               
               '''
               when there is unequal number of emtpy pixels between both shapes, bellow are strategies to deal with them
               
               One shape has one empty pixels, another shape has no empty pixels.
               take pixel counts and make it matched/unmatched pixel count and unmatched empty pixels
               
               One shape has two or more empty pixels, another shape has no empty pixels
               take pixel count in shape that does not have empty pixels. add up all pixel counts in shape with empty pixels and 
               make it matched/unmatched pixel count and unmatched empty counts for all number of empty pixels
               
               One shape has one empty pixels, another has two empty pixels
               take pixel counts and empty pixel counts in both shapes and make them matched/unmatched pixels and empty pixels. Also take their positions 
               into calculations as well.
               
               One shape has one empty pixels, another has more than two empty pixels
               same as one right before this
               
               One shape has two empty pixels, another has more than two empty pixels
               same as above
               
               One shape has multle empty pixels, another has multiple but unequal amount of empty pixels
               same as above
               '''

               if len(empty_pixels_in_current_y ) > 0:
                  # row (y) in compare shape also contains empty pixels
                  
                  
                  if len(original_empty_pixels_in_current_y) == 1 and len(empty_pixels_in_current_y) == 1:
                     # both shapes contain only one consecutive emtpy pixels
                     
                     # when there is only one consecutive empty pixels in  current rows (y) of both shapes, there will be exactly two consecutive pixels in both shapes
                     # 1. count first consecutive pixels from both shapes, count consecutive empty pixels from both shapes, count last consecutive pixels from both shapes.
                     # if count is within threshold, then make it matched.
                     
                     for original_pixels_dict in original_pixels_in_current_y:
               

                        for compare_dict in pixels_in_current_y:
                        
                           pixel_count_threshold = compare_dict.get('count') + 2 + round( compare_dict.get('count') * 0.1 )
                           minus_pixel_count_threshold = compare_dict.get('count') - 2 - round( compare_dict.get('count') * 0.1 )
                           
                           if original_pixels_dict.get('original_count') <= pixel_count_threshold and original_pixels_dict.get('original_count') >= minus_pixel_count_threshold  :

                              temp = {}
                              temp['matched_x'] = compare_dict.get('start_x')
                              temp['matched_y'] = compare_dict.get('start_y')                           
                              temp['matched_pixel_count'] = compare_dict.get('count')

                              comparison_result.append(temp)
                              
                        
                     for original_emtpy_dict in original_empty_pixels_in_current_y:
                        pixel_empty_count_threshold = empty_pixels_in_current_y[0]['count'] + 2 + round( empty_pixels_in_current_y[0]['count'] * 0.1 )
                        minus_pixel_count_threshold = empty_pixels_in_current_y[0]['count'] - 2 - round( empty_pixels_in_current_y[0]['count'] * 0.1 )
 
                        if original_emtpy_dict.get('original_count') <= pixel_empty_count_threshold and original_emtpy_dict.get('original_count') >= minus_pixel_count_threshold :
                     
                           for compare_empty_current_y in  empty_pixels_in_current_y:

                              temp = {}
                              temp['empty_matched_x'] = empty_pixels_in_current_y[0]['start_x']
                              temp['empty_matched_y'] = empty_pixels_in_current_y[0]['start_y']                           
                              temp['empty_matched_pixel_count'] = empty_pixels_in_current_y[0]['count']
                              temp['empty_original_totals'] = len(empty_pixels_in_current_y)                              
                              temp['empty_pixels_missed'] = len(original_empty_pixels_in_current_y) - 1

                              comparison_empty_result.append(temp)

                        else:
                           temp = {}
                           temp['empty_original_totals'] = len(empty_pixels_in_current_y)
                           comparison_empty_result.append(temp)



                  if len(original_empty_pixels_in_current_y) > 1 or len(empty_pixels_in_current_y) > 1:
                     # either one of shapes contain more than 1 empty pixels
                     

                     for original_pixels_dict in original_pixels_in_current_y:
               

                        for compare_dict in pixels_in_current_y:
                        
                           pixel_count_threshold = compare_dict.get('count') + 2 + round( compare_dict.get('count') * 0.1 )
                           minus_pixel_count_threshold = compare_dict.get('count') - 2 - round( compare_dict.get('count') * 0.1 )
                           
                           if original_pixels_dict.get('original_count') <= pixel_count_threshold and original_pixels_dict.get('original_count') >= minus_pixel_count_threshold  :

                              temp = {}
                              temp['matched_x'] = compare_dict.get('start_x')
                              temp['matched_y'] = compare_dict.get('start_y')                           
                              temp['matched_pixel_count'] = compare_dict.get('count')    

                              comparison_result.append(temp)                              
                        
                     for original_emtpy_dict in original_empty_pixels_in_current_y:
                     
                        for compare_empty_dict in empty_pixels_in_current_y:
                           pixel_empty_count_threshold = compare_empty_dict.get('count') + 2 + round( compare_empty_dict.get('count') * 0.1 )
                           minus_pixel_count_threshold = compare_empty_dict.get('count') - 2 - round( compare_empty_dict.get('count') * 0.1 )
 
                           if original_emtpy_dict.get('original_count') <= pixel_empty_count_threshold and  original_emtpy_dict.get('original_count') >= minus_pixel_count_threshold:

                              temp = {}
                              temp['empty_matched_x'] = compare_empty_dict.get('start_x')
                              temp['empty_matched_y'] = compare_empty_dict.get('start_y')                           
                              temp['empty_matched_pixel_count'] = compare_empty_dict.get('count')
                              temp['empty_original_totals'] = len(empty_pixels_in_current_y)                          
                              temp['empty_pixels_missed'] = len(original_empty_pixels_in_current_y) - 1

                              comparison_empty_result.append(temp)

                           else:
                              temp = {}
                              temp['empty_original_totals'] = len(empty_pixels_in_current_y)

                              comparison_empty_result.append(temp)
                  
                  
               else:
                  # compare shape has no empty pixels
                  
                  
                  if len(original_empty_pixels_in_current_y) == 1:
                     # row (y) in original shape contains only one consecutive empty pixels
                  
                     for original_pixels_dict in original_pixels_in_current_y:
               
                        pixel_count_threshold = pixels_in_current_y[0]['count'] + 2 + round( pixels_in_current_y[0]['count'] * 0.1 )
                        minus_pixel_count_threshold = pixels_in_current_y[0]['count'] - 2 - round( pixels_in_current_y[0]['count'] * 0.1 )
   
                        # there is only one consecutive pixels in current row of compare shape so pixels_in_current_y[0]
                        if original_pixels_dict.get('original_count') <= pixel_count_threshold and original_pixels_dict.get('original_count') >=  minus_pixel_count_threshold :

                           temp = {}
                           temp['matched_x'] = pixels_in_current_y[0]['start_x']
                           temp['matched_y'] = pixels_in_current_y[0]['start_y']                           
                           temp['matched_pixel_count'] = pixels_in_current_y[0]['count']     

                           comparison_result.append(temp)

                  
            else:
               # row (y) in original shape does not have empty pixels

               if len(empty_pixels_in_current_y ) > 0:
                  # row (y) in compare shape contains empty pixels

                  if len(empty_pixels_in_current_y) == 1:
                     # row (y) in compare shape contains only one consecutive empty pixels

                     for original_pixels_dict in original_pixels_in_current_y:
               
                        for compare_dict in pixels_in_current_y:
                           # because there is only one consecutive empty pixels in compare shape, pixels_in_current_y should contain two consecutive pixels.
                           # compare each one of two consecutive pixels of current row of compare shape with consecutive pixels of current row of original shape
                        
                           pixel_count_threshold = compare_dict.get('count') + 2 + round( compare_dict.get('count') * 0.1 )
                           minus_pixel_count_threshold = compare_dict.get('count') - 2 - round( compare_dict.get('count') * 0.1 )
   
                           if original_pixels_dict.get('original_count') <= pixel_count_threshold and original_pixels_dict.get('original_count') >= minus_pixel_count_threshold :

                              temp = {}
                              temp['matched_x'] = compare_dict.get('start_x')
                              temp['matched_y'] = compare_dict.get('start_y')                           
                              temp['matched_pixel_count'] = compare_dict.get('count')     

                              comparison_result.append(temp)


               else:
                  # compare shape has no empty pixels
                  # both shapes have no empty pixels. so there is only one consecutive pixels

                  
                  for original_pixels_dict in original_pixels_in_current_y:
               
                     pixel_count_threshold = pixels_in_current_y[0]['count'] + 2 + round( pixels_in_current_y[0]['count'] * 0.1 )
                     minus_pixel_count_threshold = - pixels_in_current_y[0]['count'] - 2 - round( pixels_in_current_y[0]['count'] * 0.1 )
   
                     if original_pixels_dict.get('original_count') <= pixel_count_threshold and original_pixels_dict.get('original_count') >= minus_pixel_count_threshold:

                        temp = {}
                        temp['matched_x'] = pixels_in_current_y[0]['start_x']
                        temp['matched_y'] = pixels_in_current_y[0]['start_y']                           
                        temp['matched_pixel_count'] = pixels_in_current_y[0]['count']                          

                        comparison_result.append(temp)
                                 

                  
            break
            
         else:
         
            # if two consecutive pixels are right next to each other, the difference of them should produce 1
            if abs( x_value - prev_x_value ) > 1:
               # boundary is found

               if x_value - prev_x_value < 0:
                  # result is negative, this means current x value is smaller ( it is on the left relative to previous )
                  # then, current x value is the boundary pixel " on the left side "
                   
                  # this should never be executed because x values are sorted from smallest to the biggest so previous_x_value should always be 
                  # smaller than current x_value.
                   
                  print("this should never be printed")
                   
                

               else:
                  # result is positive, this means current x value is larger than previous ( it is on the right relative 
                  # to previous ). Then, current x value is the boundary pixel " on the right side " relative to previous

                  # empty pixel found. empty pixel starts from previous_x_value + 1 and ends at x_value - 1.
                   
                  # consecutive shape pixels ended at previous_x_value.

                  temp['count'] =  consecutive_x_counter
                  pixels_in_current_y.append( temp )  
                  

                  empty_temp = {}
                  empty_temp['start_x'] = prev_x_value + 1
                  empty_temp['start_y'] = y
                  empty_temp['count'] = x_value  - ( prev_x_value + 1) 
                  empty_pixels_in_current_y.append( empty_temp )

                  # after boundary is found, consecutive shape pixel starts at current x_value. Also this pixel is not the last pixel, so don't call compare_w_shape
                  consecutive_x_counter = 1
                  
                  temp = {}
                  temp['start_x'] = x_value
                  temp['start_y'] = y


            else:
               # current x value is right next to previous pixel and also it is not the last pixel in the current row (y)
               consecutive_x_counter +=1
                
  
         prev_x_value = x_value               

         x_counter_in_current_running_y += 1
         
         
      # after looping through all comparing shape's x values in current row (y)
      search_until -= 1
         
      prev_rightMost_x = rightMost_x


      if y == compare_largest_y:

         return comparison_result, comparison_empty_result




def find_consecutive_matches( comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids ):


   if original_shape_height >= compare_shape_height:
      rows_needed = math.floor( compare_shape_height / 3)
      larger_shape_height = original_shape_height
   else:
      rows_needed = math.floor( original_shape_height / 3)
      larger_shape_height = compare_shape_height

   if rows_needed < 3:
      return None, None
      
   
   row_match_result = 0
      
   for row in comparison_result:

      for one_consecutive_pixels in row:

         
         if 'original_y' in one_consecutive_pixels:
        
            cur_original_y = one_consecutive_pixels['original_y']
            

         if 'matched_y' in one_consecutive_pixels:
            cur_compare_y = one_consecutive_pixels['matched_y'] 

         else:
            # Both of original_y and matched_y from current row are needed. so loop current row until both are found.
            continue
            
         cur_row_counter = 1
         row_matches = 0
         next_original_row = False
         mismatched_cur_row = False
         
         for other_row in comparison_result:

                        
            for other_one_consecutive_pixels in other_row:
         

               if 'original_y' in other_one_consecutive_pixels:
                  if cur_original_y + cur_row_counter == other_one_consecutive_pixels['original_y'] :
                     
                     next_original_row = True


               # check only if current row of original shape is found
               if 'matched_y' in other_one_consecutive_pixels and next_original_row:
                  if cur_compare_y + cur_row_counter == other_one_consecutive_pixels['matched_y']:

                     # current original row's match is found. start looking for next row starting with original shape's row.
                     cur_row_counter += 1
                     next_original_row = False

                     mismatched_cur_row = False
                     row_matches += 1
                     
                     if row_matches > row_match_result:
                        row_match_result = row_matches

                  else:
                  
                     mismatched_cur_row = True
                     
            # check at the end of the row if match was found. if not start with another original row
            if   mismatched_cur_row:
               break            
            

   unmatched_rows = larger_shape_height - row_match_result
   if row_match_result > rows_needed:
      return row_match_result, unmatched_rows
   else:
      return None, None
















def find_boundary_matches(comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids ):


   # sorting by original_y. starting with smallest going up to the largest
   comparison_result = sorted( comparison_result , key=lambda item: item[0]['original_y'] )

   '''

   rows_needed = math.floor(original_shape_height / 3)


   for row in comparison_result:

      for one_consecutive_pixels in row:
         
         
         if 'original_y' in one_consecutive_pixels:
        
            cur_original_y = one_consecutive_pixels['original_y']
            

         if 'matched_y' in one_consecutive_pixels:
            cur_compare_y = one_consecutive_pixels['matched_y'] 

         else:
            # Both of original_y and matched_y from current row are needed. so loop current row until both are found.
            continue
            
         for empty_row in empty_comparison_result:
         
            for empty_one_consecutive_pixels in empty_row:
            
               if 'original_y' in empty_one_consecutive_pixels:
                  # original pixels and empty original pixels should be on the same row
                  if cur_original_y == empty_one_consecutive_pixels['original_y']:
                  
                     empty_original_row =  cur_original_y              
                  
               if 'empty_matched_y' in empty_one_consecutive_pixels:
                  # matched pixels in compare shape and matched empty pixels in the compare shape should be on the same row
                  if cur_compare_y == empty_one_consecutive_pixels['empty_matched_y']:
                     empty_compare_row = cur_compare_y
                     
               if 'empty_pixels_missed' in empty_one_consecutive_pixels:
               
                  if empty_one_consecutive_pixels['empty_pixels_missed'] == 0:
                     rows_needed -= 1

   # if unsuccessful, return nothing
   if rows_needed > 0:
      return
   '''
   if original_shape_height >= compare_shape_height:
      rows_needed = math.floor( compare_shape_height / 3)
   else:
      rows_needed = math.floor( original_shape_height / 3)

   if rows_needed < 3:
      print("can not determine with boundary consecutive row match algorithm")
      return
      

   
   consective_row_match_result = 0
   for row in comparison_result:

      for one_consecutive_pixels in row:

         consecutive_row_matches = 0
         
         if 'original_y' in one_consecutive_pixels:
        
            cur_original_y = one_consecutive_pixels['original_y']
            cur_original_x = one_consecutive_pixels['original_x']
            cur_original_count = one_consecutive_pixels['original_count']

         if 'matched_y' in one_consecutive_pixels:
            cur_compare_y = one_consecutive_pixels['matched_y']
            cur_compare_x = one_consecutive_pixels['matched_x']
            cur_compare_count = one_consecutive_pixels['matched_pixel_count']

         else:
            # Both of original_y and matched_y from current row are needed. so loop current row until both are found.
            continue

         cur_original_counter = 1
         next_original_row = False
         
         
         for other_row in comparison_result:
            
            mismatched_cur_original_row = False
            # sometimes, matched_y for the next_original_row can not be found in the same row as original_y and processing goes to the next row and gets here.
            # in that case, next_original_row is True. Initializations of original_start_x, compare_start_x_diff, pixel_diff_threshold should occur before original_y.
            # so put "if not next_original_row:"
            if not next_original_row:
               original_start_x_diff = compare_start_x_diff = pixel_diff_threshold = None    
               
            for other_one_consecutive_pixels in other_row:

      
               if 'original_y' in other_one_consecutive_pixels:
                  # get next row from original shape
                  if cur_original_y + cur_original_counter == other_one_consecutive_pixels['original_y']:


                     pixel_diff_threshold = other_one_consecutive_pixels['original_count'] + 2 + round( other_one_consecutive_pixels['original_count'] * 0.1 )
                     original_start_x_diff = cur_original_x - other_one_consecutive_pixels['original_x']
                     original_end_x_diff = cur_original_count - other_one_consecutive_pixels['original_count']

                     next_original_row = True
      
               if 'matched_y' in other_one_consecutive_pixels and next_original_row:
               
                  
                  # make sure matched_y is the corresponding row of current original row
                  if cur_compare_y + cur_original_counter == other_one_consecutive_pixels['matched_y']:
                  
                     compare_start_x_diff = cur_compare_x - other_one_consecutive_pixels['matched_x']
                     compare_end_x_diff = cur_compare_count - other_one_consecutive_pixels['matched_pixel_count']


                     cur_original_counter += 1
                     next_original_row = False

                     if original_start_x_diff - compare_start_x_diff <= pixel_diff_threshold:
               
                        if original_end_x_diff - compare_end_x_diff <= pixel_diff_threshold:

                           
                           mismatched_cur_original_row = False
                           consecutive_row_matches += 1
                           
                           if consecutive_row_matches > consective_row_match_result:
                           
                              consective_row_match_result = consecutive_row_matches
                           
    
                           # current row is the match. go to next row
                           break
                        
                        
                        else:
                           # current original row did not have consecutive row matches. start with next original row
                           mismatched_cur_original_row = True


            # at the end of each row, if consecutive match was not found, start with next original row.
            if mismatched_cur_original_row:
               break

   if consective_row_match_result > rows_needed:
      return consective_row_match_result










# this method compares two shapes from different frames of video and tries to determine if they are both the same 
# same in different frames of video.

#  two parameters in, Both are a dictionary with following form.
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
    
def find_shapes_in_diff_frames(original_pixels_dict, compare_pixels_dict, algorithm, shape_ids):


   original_smallest_y = min(int(d['y']) for d in original_pixels_dict.values())
   original_largest_y = max(int(d['y']) for d in original_pixels_dict.values())
   
   original_shape_height = original_largest_y - original_smallest_y

   original_smallest_x = min(int(d['x']) for d in original_pixels_dict.values())
   original_largest_x = max(int(d['x']) for d in original_pixels_dict.values())


   compare_smallest_y = min(int(d['y']) for d in compare_pixels_dict.values())
   compare_largest_y = max(int(d['y']) for d in compare_pixels_dict.values())
   
   compare_shape_height = compare_largest_y - compare_smallest_y

   # as we take each one of original pixels and compare it with compare shape, there is no need to look at every pixel of the compare shape. Because for example, if I 
   # take top original pixel and compare it with every pixel of compare shape, there is no way I find top original pixel at the bottom of the compare shape.
   # + 1 is added because same height becomes 0 so adding 1 enables 1 top pixel comparison with 1 top pixel in compare shape
   search_until = abs( original_shape_height - compare_shape_height ) + 1

   
   # this list will have matched rows from both shapes. matched rows will be pairs. Pair consists of one row from original shape and another row from compare shape
   comparison_result = []
   empty_comparison_result = []


   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(original_smallest_y, original_largest_y + 1):
   
   
      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in original_pixels_dict  if (int(original_pixels_dict[k]['y'])) == y]
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y_values:
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(original_pixels_dict[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
         
         
      rightMost_x = max( x_values_list_in_current_y )
      leftMost_x = min( x_values_list_in_current_y )
      
      
      pixels_in_current_y = []
      empty_pixels_in_current_y = []
         
         
      
      # this is for getting the largest x value in current running y. largest x value is the last one in current running y because
      # x values are sorted from smallest to largest
      x_counter_in_current_running_y = 1
      
      consecutive_x_counter = 0
      
      x_numbers_in_current_running_y = len(x_values_list_in_current_y)

      first = True
         
      for x_value in x_values_list_in_current_y:
      
         matched_y_in_compare_shape = {}

         # is this the first x value?
         if first != False:
            consecutive_x_counter +=1

            temp = {}
            temp['original_x'] = x_value
            temp['original_y'] = y


            prev_x_value = x_value 
            first = False     
            # for this row(y), there is only one pixel?
            if x_counter_in_current_running_y == x_numbers_in_current_running_y:

               temp['original_count'] =  consecutive_x_counter
               pixels_in_current_y.append( temp )

               # this temporary dictionary is for storing matched rows of original shape and compare shape
               #temp = {}
               # all consecutive pixels (both real pixels and empty pixels ) should have same y number
               #temp['original_y'] = pixels_in_current_y[0]['original_x']
               
               # compare with another shape in different frame of image
               # row with one pixel so returned value of empty is empty
               matched_y_in_compare_shape, empty_matched_y_in_compare_shape = compare_w_shape(compare_pixels_dict, search_until, y - original_smallest_y, pixels_in_current_y, empty_pixels_in_current_y )
               
               # return result of one pixel row, so this will not contain empty pixels
          
               # add current rows of original shape and compare shape only when match is found
               if matched_y_in_compare_shape:

                  # merging row from original and compare shapes
                  original_compare_pixels = pixels_in_current_y + matched_y_in_compare_shape

            
                  comparison_result.append(original_compare_pixels)


               break

            x_counter_in_current_running_y += 1            
            continue
  
         # checking to see if x value is the last one in current running y
         if x_counter_in_current_running_y == x_numbers_in_current_running_y:

            temp['original_count'] =  consecutive_x_counter + 1
            pixels_in_current_y.append( temp )
            
            # this temporary dictionary is for storing matched rows of original shape and compare shape
            #temp = {}
            # all consecutive pixels (both real pixels and empty pixels ) should have same y number
            #temp['original_y'] = pixels_in_current_y[0]['original_y']
                    
            # compare with another shape in different frame of image
            matched_y_in_compare_shape, empty_matched_y_in_compare_shape = compare_w_shape(compare_pixels_dict, search_until, y - original_smallest_y, pixels_in_current_y, empty_pixels_in_current_y )

            # add current rows of original shape and compare shape only when match is found
            if matched_y_in_compare_shape:

               # merging row from original and compare shapes
               original_compare_pixels = pixels_in_current_y + matched_y_in_compare_shape

            
               comparison_result.append(original_compare_pixels)
            
            # add current rows of original shape and compare shape only when match is found
            if empty_matched_y_in_compare_shape:
               # merging row from original and compare shapes            
               empty_original_compare_pixels = empty_pixels_in_current_y + empty_matched_y_in_compare_shape

               empty_comparison_result.append(empty_original_compare_pixels)
               

               
               
            #print("comparison result")
            #print(matched_y_in_compare_shape)
            
            break
            
         else:
         
            # if two consecutive pixels are right next to each other, the difference of them should produce 1
            if abs( x_value - prev_x_value ) > 1:
               # boundary is found

               if x_value - prev_x_value < 0:
                  # result is negative, this means current x value is smaller ( it is on the left relative to previous )
                  # then, current x value is the boundary pixel " on the left side "
                   
                  # this should never be executed because x values are sorted from smallest to the biggest so previous_x_value should always be 
                  # smaller than current x_value.
                   
                  print("this should never be printed")
                   
                

               else:
                  # result is positive, this means current x value is larger than previous ( it is on the right relative 
                  # to previous ). Then, current x value is the boundary pixel " on the right side " relative to previous

                  # empty pixel found. empty pixel starts from previous_x_value + 1 and ends at x_value - 1.
                   
                  # consecutive shape pixels ended at previous_x_value.

                  temp['original_count'] =  consecutive_x_counter
                  pixels_in_current_y.append( temp )  
                  

                  empty_temp = {}
                  empty_temp['original_x'] = prev_x_value + 1
                  empty_temp['original_y'] = y
                  empty_temp['original_count'] = x_value  - ( prev_x_value + 1) 
                  empty_pixels_in_current_y.append( empty_temp )

                  # after boundary is found, consecutive shape pixel starts at current x_value. Also this pixel is not the last pixel, so don't call compare_w_shape
                  consecutive_x_counter = 1
                  
                  temp = {}
                  temp['original_x'] = x_value
                  temp['original_y'] = y


            else:
               # current x value is right next to previous pixel and also it is not the last pixel in the current row (y)
               consecutive_x_counter +=1
                
  
         prev_x_value = x_value               

         x_counter_in_current_running_y += 1
         
         
      # after looping through all original x values in current row (y)


      # updating for each row (y) of compare shape
         
         
      #updating for each row (y) of original shape
   
      prev_rightMost_x = rightMost_x
      prev_leftMost_x = leftMost_x

      
   # check if both shapes are same shapes in different frames of video

   pixel_count_diff = abs(len(original_pixels_dict) - len(compare_pixels_dict) )

   if algorithm == "boundary":
      return find_boundary_matches(comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids)
   elif algorithm == "consecutive_count":
      temp1, temp2 = find_consecutive_matches(comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids)
      return temp1, temp2, pixel_count_diff





















































































































































