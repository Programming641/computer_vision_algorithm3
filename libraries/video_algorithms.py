
from PIL import Image
import os
import math


  
   




def process_tentative_row_matches(matched_rows, empty_flag):


   if empty_flag:
      x_label = 'empty_matched_x'
      y_label = 'empty_matched_y'
      pixel_count_lable = 'empty_pixel_count'
      original_total_lable = 'empty_original_totals'
      matched_orig_num_lable = 'empty_matched_original_num'
   else:
      x_label = 'matched_x'
      y_label = 'matched_y'
      pixel_count_lable = 'matched_pixel_count'
      original_total_lable = 'matched_original_totals'
      matched_orig_num_lable = 'matched_original_num'      



   def calculate_x_distances(multiple_consec_comp_in_row, comp_consec_pix):

      temp = {}
      temp['id_num'] = comp_consec_pix['id_num']
      temp['id_num2'] = multiple_consec_comp_in_row['id_num']
                  
               
      # checking direction of matched original x
      if multiple_consec_comp_in_row[matched_orig_num_lable] < comp_consec_pix[matched_orig_num_lable]:
                     
         if comp_consec_pix[x_label] - multiple_consec_comp_in_row[x_label] > 0:
            temp['x_direction'] = True
                        
            comp_x_distance = abs( comp_consec_pix[x_label] - multiple_consec_comp_in_row[x_label] )
            orig_x_distance = comp_consec_pix['original_x'] - multiple_consec_comp_in_row['original_x']
            x_distance_diff = abs( comp_x_distance - orig_x_distance )
                        
            temp['x_distance_diff'] = x_distance_diff
            temp[pixel_count_lable + str(comp_consec_pix['id_num'])] = comp_consec_pix[pixel_count_lable]
            temp[pixel_count_lable + str(multiple_consec_comp_in_row['id_num']) ] = multiple_consec_comp_in_row[pixel_count_lable]
         
         else:
            temp['x_direction'] = False
         
      else:
                     
         if multiple_consec_comp_in_row[x_label] - comp_consec_pix[x_label] > 0:
            temp['x_direction'] = True
                        
            comp_x_distance = abs( multiple_consec_comp_in_row[x_label] - comp_consec_pix[x_label] )
            orig_x_distance = multiple_consec_comp_in_row['original_x'] - comp_consec_pix['original_x']
            x_distance_diff = abs( comp_x_distance - orig_x_distance )
                   
            temp['x_distance_diff'] = x_distance_diff                   
            temp[pixel_count_lable + str(comp_consec_pix['id_num'])] = comp_consec_pix[pixel_count_lable]
            temp[pixel_count_lable + str(multiple_consec_comp_in_row['id_num'])] = multiple_consec_comp_in_row[pixel_count_lable]                        
                        
         else:
            temp['x_direction'] = False     

      if temp['x_direction'] != False:
          
         comp_count = ( temp[pixel_count_lable + str(comp_consec_pix['id_num'])] + temp[pixel_count_lable + str(multiple_consec_comp_in_row['id_num'])] ) * 4
         x_distance = comp_count - ( temp['x_distance_diff'] * 2 )
         
         #print("x_distance")
         #print( " id_num " + str(temp['id_num']) + " id_num2 " + str(temp['id_num2']) + " id_num pixel count " + str(temp[pixel_count_lable + str(comp_consec_pix['id_num'])] ) + " id_num2 pixel count " + str(temp[pixel_count_lable + str(multiple_consec_comp_in_row['id_num'])] ) + " x_distance_diff " + str(temp['x_distance_diff']) + " result " + str(x_distance) )
         return x_distance


      else:
         return 0
         
         
         
   def find_n_put_biggest_pix(cur_row, biggest_pixel_count_list, compare_row_nums ):    
      temp = {}
      biggest_pixel_count = 0
      for orig_pair in cur_row:
         for consec_pixels in orig_pair:
            if 'original_y' in consec_pixels:
               cur_original_y = consec_pixels['original_y']
               cur_original_x = consec_pixels['original_x']
                  
            if pixel_count_lable in consec_pixels:
                     
               if consec_pixels[pixel_count_lable] > biggest_pixel_count:
                  present = False
                        
                  # putting into empty biggest_pixel_count_list
                  if not biggest_pixel_count_list:
                     comp_present = None
                     for comp_matched in compare_row_nums:
                        if consec_pixels[y_label] == comp_matched[y_label] and consec_pixels[x_label] == comp_matched[x_label]:
                           comp_present = True
                     if not comp_present:
                        biggest_pixel_count = consec_pixels[pixel_count_lable]
                        temp = {}
                        temp['original_y'] = cur_original_y
                        temp['original_x'] = cur_original_x
                        temp['id_num'] = consec_pixels['id_num']
                        temp[pixel_count_lable] = biggest_pixel_count                        
                  else:

                     for comp_row in biggest_pixel_count_list:
                        if consec_pixels['id_num'] == comp_row['id_num']:
                           present = True
                                 
                     comp_present = None
                     for comp_matched in compare_row_nums:
                        if consec_pixels[y_label] == comp_matched[y_label] and consec_pixels[x_label] == comp_matched[x_label]:
                           comp_present = True
                        
                     # this compare consecutive pixels have not already added in biggest_pixel_count_list or compare_row_nums
                     if present == False and not comp_present:
                        
                        biggest_pixel_count = consec_pixels[pixel_count_lable]
                        temp = {}
                        temp['original_y'] = cur_original_y
                        temp['original_x'] = cur_original_x
                        temp['id_num'] = consec_pixels['id_num']
                        temp[pixel_count_lable] = biggest_pixel_count

         
      if temp:
         
         for one_pair in cur_row:
            inner_temp = {}  
            for one_consec_pixels in one_pair:

               if 'original_y' in one_consec_pixels:
             
                  original_row_nums.append( one_consec_pixels['original_y'])
                  inner_temp['original_y'] = one_consec_pixels['original_y']

               if 'id_num' in one_consec_pixels:
                  if temp['id_num'] == one_consec_pixels['id_num']:

                     inner_temp[y_label] = one_consec_pixels[y_label]
                     inner_temp[x_label] = one_consec_pixels[x_label]
                                                      
                     compare_row_nums.append( inner_temp )
            
            
         biggest_pixel_count_list.append(temp)           
         return True
         
         
         
         
         
         
         
         

   final_results = 0
   biggest_pixel_count_list = []
   x_distance = 0
   matched_row_counts = 0
   row_counts = 0
   
   # this stores all matched original row numbers
   original_row_nums = []
   
   # this stores all matched compare row numbers. Once matched, it can not match another original row.
   compare_row_nums = []

   # this is used for checking consecutiveness of of original and matched compare rows. if original row 150 matched with compare 160.
   # for this to be consecutive, original row 151 matched with compare 171 or any other row that is not next to it does not make it a consecutive match.
   consecutive_row_matches = []
   
   for matched_row in matched_rows:
      row_counts += 1
      # this will contain all original consecutive pixels with their pairing compare consecutive pixels
      cur_row = []
    
      original_num = 0
      comp_id_num = 0
                 
      # first need to match with every original and compare consecutive pixels based on pixel count threshold
      for one_consec_pixels in matched_row:

         if 'original_y' in one_consec_pixels:
         
            cur_original = []
            original_num += 1
            
            temp = {}
            temp['original_y'] = one_consec_pixels['original_y']
            temp['original_x'] = one_consec_pixels['original_x']
            temp['original_count'] = one_consec_pixels['original_count']
            
            cur_original.append(temp)
            
            
            
   
            # this is for getting compare consecutive pixels for comparing with current original consecutive pixels
            for comp_one_consec_pixels in matched_row:
               
               # make sure to add only matched compare consecutive pixels to its original
               if y_label in comp_one_consec_pixels:
                  if comp_one_consec_pixels[matched_orig_num_lable] == original_num:
                  
                     pixel_count_threshold = comp_one_consec_pixels[pixel_count_lable] + 1.5 + round( comp_one_consec_pixels[pixel_count_lable] * 0.1 )
                     minus_pixel_count_threshold = comp_one_consec_pixels[pixel_count_lable] - 1.5 - round( comp_one_consec_pixels[pixel_count_lable] * 0.1 )
   
                     if one_consec_pixels['original_count'] <= pixel_count_threshold and one_consec_pixels['original_count'] >= minus_pixel_count_threshold:
                        comp_id_num += 1
                        temp = {}
                        temp['id_num'] = comp_id_num
                        temp[y_label] = comp_one_consec_pixels[y_label]
                        temp[x_label] = comp_one_consec_pixels[x_label]
                        temp[pixel_count_lable] = comp_one_consec_pixels[pixel_count_lable]
                        temp[matched_orig_num_lable] = comp_one_consec_pixels[matched_orig_num_lable]
                        temp[original_total_lable] = comp_one_consec_pixels[original_total_lable]
                     
                        cur_original.append(temp)
                  
            # one original consecutive pixels of current row has finished putting all its matching compare consecutive pixels into cur_original
            cur_row.append(cur_original)
            
      #print("cur_row")
      #print(cur_row)
      # now cur_row contains all original consecutive pixels with their matching compare consecutive pixels
      # 1. matching by pixel count threshold is done at this point.
      
      # check if there is big enough pixel counts in every matching pairs in current row
      p_c_big_enough_threshold = 4
      pixel_count_big_enough = False
      for one_pair in cur_row:
         for one_consec_pixels in one_pair:
         
            if 'original_count' in one_consec_pixels:
            
               if one_consec_pixels['original_count'] >= p_c_big_enough_threshold:
                  pixel_count_big_enough = True
                  
      # if there is not any consecutive pixels with big enough pixel counts, then check if there is only one pair in the current row.
      # if there are multiple original consecutive pixels and there is only one pair with the small pixel count compare consecutive pixels, then 
      # current row is not a match
      if not pixel_count_big_enough:
         # there is no big enough pixel count   
         continue
                     

      # at this point, either current row contains big enough pixel count or there are multiple pairs of small pixel count consecutive pixels
      # now comes the "2. matching by x distance direction."
      
      # x direction is only needed if current row has multiple matching pairs of the same row. this means that there are two or more same original_y pairs
      # example. [{'original_y': 104, 'original_x': 61, 'original_count': 12}], [{'original_y': 104, 'original_x': 74, 'original_count': 5}.....
      # in this case there are two same original_y value pairs but first one does not have any matching compare consecutive pixels.
      
      check_pair = 0
      # check if current row matches contain more than 1 original consecutive pixels and their pairs.
      if len(cur_row) > 1:
         for one_pair in cur_row:
            for one_consec_pixels in one_pair:
              
              # check if current pair contains its pairing compare consecutive pixels
              if y_label in one_consec_pixels:
                 check_pair += 1
                 
                 # current pair contains its pairing compare consecutive pixels. break to move to check next pair
                 break
                 
      
      if check_pair > 1:
      
         # this list stores all original x values. index 0 contains nothing.
         # index 1 contains first original's x value, 2 index contains 2nd original's x value and so on.
         original_x_distance = []
         
         comp_y_list = []
      
         for one_pair in cur_row:
            for one_consec_pixels in one_pair:
               if 'original_x' in one_consec_pixels:
                  original_x_distance.append( one_consec_pixels['original_x'] )
                  
               if y_label in one_consec_pixels:

                  # from every original pair, we need to get y value of compare consecutive pixels so that we know which compare has the multiple consecutive pixels 
                  # on the same y value
                  comp_y_list.append(one_consec_pixels[y_label])


         original_x_distance.sort()         
                     
         # at this point comp_y_list contains all y values of the current original row. now we need to get multiple y values only.
         temp = []
         multiple_comp = []
         for i in comp_y_list:
            if i not in temp:
               temp.append(i)
            else:
               # adding duplicate y values
               multiple_comp.append(i)
            
         
         # multiple_comp contains multiple compare consecutive pixels.
         # now we need to get their x values and choose the ones that match the best for the current original row
         # so that current original row has the best match of its corresponding compare shape's row
         
         multiple_comp_consec_pix = []
         for one_pair in cur_row:
            for one_consec_pixels in one_pair:
            
               if 'original_x' in one_consec_pixels:
                  x = one_consec_pixels['original_x']
                  count = one_consec_pixels['original_count']
            
               if y_label in one_consec_pixels:
                  if  one_consec_pixels[y_label] in multiple_comp:
                     # current compare consecutive pixels contain multiple consecutive pixels on the same y value
                     
                     temp = {}
                     temp['id_num'] = one_consec_pixels['id_num']
                     temp[y_label] = one_consec_pixels[y_label]
                     temp[x_label] = one_consec_pixels[x_label]
                     temp[pixel_count_lable] = one_consec_pixels[pixel_count_lable]
                     temp['original_x'] = x
                     temp['original_pixel_count'] = count
                     temp[matched_orig_num_lable] = one_consec_pixels[matched_orig_num_lable]
                     temp[original_total_lable] = one_consec_pixels[original_total_lable]
                     
                     multiple_comp_consec_pix.append(temp)
                     

         if not multiple_comp_consec_pix:
            # current row has multiple original consecutive pixels but there are no multiple compare consecutive pixels with same y value.
            # because there are no multiple compare consecutive pixels with the same row, each one of the compare consecutive pixels
            # matching only one original consecutive pixels. so evaluation will be only one pixel count.
            
            success = find_n_put_biggest_pix(cur_row, biggest_pixel_count_list, compare_row_nums )
            if success:
               matched_row_counts += 1
         
         
         y_done = []
         for same_y in multiple_comp_consec_pix:
            
            # make sure x_distance is cotained in only one compare consecutive pixels for each row.
            if same_y[y_label] in y_done:
               continue
            
            compare_x_distace = []
            # if there is one in the multiple_comp, there are two in the multiple_comp_consec_pix but one is itself.
            cur_same_y_count = multiple_comp.count( same_y[y_label] ) 
            
            for another_same_y in multiple_comp_consec_pix:
               # make sure it is not itself and comparing with other compare consecutive pixels
               if same_y != another_same_y and same_y[y_label] == another_same_y[y_label]:
                  cur_same_y_count -= 1
                  
                  temp = {}
                  temp['id_num'] = another_same_y['id_num']
                  temp[y_label] = another_same_y[y_label]
                  temp[x_label] = another_same_y[x_label]
                  temp['original_x'] = another_same_y['original_x']
                  temp['original_pixel_count'] = another_same_y['original_pixel_count']
                  temp[pixel_count_lable] = another_same_y[pixel_count_lable]
                  temp[matched_orig_num_lable] = another_same_y[matched_orig_num_lable]
                  
                  compare_x_distace.append(temp)
                  
                  if cur_same_y_count == 0:
                     
                     temp = {'x_distance': compare_x_distace }
                     same_y.update( temp )
                     
                     y_done.append( same_y[y_label] )


         #print("multiple_comp_consec_pix")
         #print(multiple_comp_consec_pix)

         
         temp = 0
         temp_compare_consec_pix = {}
         for multiple_consec_comp_in_row in multiple_comp_consec_pix:
            if 'x_distance' in multiple_consec_comp_in_row:
               # all compare consecutive pixels of each row are contained in the same dictionary as the one with 'x_distance'

               
               for comp_consec_pix in multiple_consec_comp_in_row['x_distance']:
                  comp_present = None
                  for comp_matched in compare_row_nums:
                     if multiple_consec_comp_in_row[y_label] == comp_matched[y_label] and multiple_consec_comp_in_row[x_label] == comp_matched[x_label]:
                        comp_present = True
                  
                     if comp_consec_pix[y_label] == comp_matched[y_label] and comp_consec_pix[x_label] == comp_matched[x_label]:
                        comp_present = True
                     
                  if not comp_present:
                     # both of the current multiple_consec_comp_in_row and comp_consec_pix have not matched yet.
                     cur_temp = calculate_x_distances(multiple_consec_comp_in_row, comp_consec_pix)
                  
                     if cur_temp > temp:
                        temp_compare_consec_pix[y_label] = multiple_consec_comp_in_row[y_label]
                        temp_compare_consec_pix[x_label] = multiple_consec_comp_in_row[x_label]
                        temp_compare_consec_pix['another_x'] = comp_consec_pix[x_label]
                        temp = cur_temp
                  
                  # now for comparing compare consecutive pixels with each other inside x_distance list
                  for another_comp_consec_pix in multiple_consec_comp_in_row['x_distance']:                   
                  
                     comp_present = None
                     for comp_matched in compare_row_nums:
                        if comp_consec_pix[y_label] == comp_matched[y_label] and comp_consec_pix[x_label] == comp_matched[x_label]:
                           comp_present = True
                  
                        if another_comp_consec_pix[y_label] == comp_matched[y_label] and another_comp_consec_pix[x_label] == comp_matched[x_label]:
                           comp_present = True
                           
                           
                     if not comp_present:
                           
                        cur_temp = calculate_x_distances(comp_consec_pix, another_comp_consec_pix)
                     
                        if cur_temp > temp:
                           temp_compare_consec_pix[y_label] = comp_consec_pix[y_label]
                           temp_compare_consec_pix[x_label] = comp_consec_pix[x_label]
                           temp_compare_consec_pix['another_x'] = another_comp_consec_pix[x_label]
                           temp = cur_temp                  

         if temp:
            matched_row_counts += 1
            original_y = None
            for one_pair in cur_row:
               for one_consec_pixels in one_pair:
                  if 'original_y' in one_consec_pixels:
                     original_row_nums.append( one_consec_pixels['original_y'])
                     original_y = one_consec_pixels['original_y']

            inner_temp = {}
            inner_temp[y_label] = temp_compare_consec_pix[y_label]
            inner_temp[x_label] = temp_compare_consec_pix[x_label]
            inner_temp['original_y'] = original_y
                                                      
            compare_row_nums.append( inner_temp )
            
            inner_temp = {}
            inner_temp[y_label] = temp_compare_consec_pix[y_label]
            inner_temp[x_label] = temp_compare_consec_pix['another_x']
            inner_temp['original_y'] = original_y
                                                      
            compare_row_nums.append( inner_temp )            

            x_distance += temp
      else:
         # current row has only one filled pair. either current row has multile pairs but only one pair has its matching compare consecutive pixels or 
         # there is only one pair and it is filled.
         # because there is only one matching pair, evaluation of this will be the same as when multiple_comp_consec_pix was empty above.
         success = find_n_put_biggest_pix(cur_row, biggest_pixel_count_list, compare_row_nums )
         if success:
            matched_row_counts += 1


         
   #print("biggest_pixel_count_list")
   #print(biggest_pixel_count_list)
   for pixel_count in biggest_pixel_count_list:
      final_results += pixel_count[pixel_count_lable] * 2
   

   # removing duplicates
   original_row_nums = list( dict.fromkeys(original_row_nums) )
   #print("matched rows " + str(original_row_nums) )
   #print("compare_row_nums " + str(compare_row_nums) )
   
   consecutive_rows = []
   consecutive_row_counter = 1
   counts = 0
   for matched_row in compare_row_nums:
      counts += 1
      found = False
      cur_original_y = matched_row['original_y']
      cur_compare_y = matched_row['matched_y']

      for another_mached_row in compare_row_nums:
   
         if cur_original_y + 1 == another_mached_row['original_y']:
            if cur_compare_y + 1 == another_mached_row['matched_y']:
               consecutive_row_counter += 1
               found = True
      
      if not found:

         if consecutive_row_counter > 1:
            consecutive_rows.append(consecutive_row_counter)
            consecutive_row_counter = 1
   
      if counts >= len(compare_row_nums):
         if consecutive_row_counter > 1:
            consecutive_rows.append(consecutive_row_counter)


   #print("consecutive_rows " + str(consecutive_rows) )
   
   for consecutive_row in consecutive_rows:
      temp = ( consecutive_row * consecutive_row ) * 2
      final_results += temp

   unmatched_row_counts = row_counts - matched_row_counts
   final_results += (matched_row_counts * 1.5) - (unmatched_row_counts * 1.5)
   final_results += x_distance    
   return final_results
      


def process_real_p_rows( comparison_result, original_shape_height, compare_shape_height, shape_ids ):

   comparison_result = sorted( comparison_result , key=lambda item: ( item[0]['original_y'],item[0]['original_x'] )  )


   if original_shape_height >= compare_shape_height:
      rows_needed = math.floor( compare_shape_height / 3)
      larger_shape_height = original_shape_height
   else:
      rows_needed = math.floor( original_shape_height / 3)
      larger_shape_height = compare_shape_height

   if rows_needed < 3:
      return None


   p_t_r_m_result = process_tentative_row_matches(comparison_result, False)

   return p_t_r_m_result
   








def find_boundary_matches(comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids ):

   # sorting by original_y. starting with smallest going up to the largest
   comparison_result = sorted( comparison_result , key=lambda item: ( item[0]['original_y'],item[0]['original_x'] ) )
   empty_comparison_result = sorted( empty_comparison_result , key=lambda item: ( item[0]['original_y'],item[0]['original_x'] ) )


   empty_result = 0
   if empty_comparison_result:
      empty_result = process_tentative_row_matches(empty_comparison_result, True)

   real_pix_result = process_tentative_row_matches(comparison_result, False)
   
   result = real_pix_result + empty_result

   # start of finding matches in comparison_result
   
   if original_shape_height >= compare_shape_height:
      rows_needed = math.floor( compare_shape_height / 5)
   else:
      rows_needed = math.floor( original_shape_height / 5)

   if rows_needed < 3:
      return
      
   return result






def compare_orig_comp_row(cur_original_row, cur_compare_row, matched_rows, empty_flag):

   if empty_flag:
      x_label = 'empty_matched_x'
      y_label = 'empty_matched_y'
      pixel_count_lable = 'empty_pixel_count'
      original_total_lable = 'empty_original_totals'
      matched_orig_num_lable = 'empty_matched_original_num'
   else:
      x_label = 'matched_x'
      y_label = 'matched_y'
      pixel_count_lable = 'matched_pixel_count'
      original_total_lable = 'matched_original_totals'
      matched_orig_num_lable = 'matched_original_num'      

              
   for i_compare in range(len(cur_compare_row)):
                        
      for i_original in range( len(cur_original_row) ):
          
         # here, each one of consecutive pixels of compare shape compares with every one of consecutive pixels of original one.
                        
         pixel_count_threshold = cur_compare_row[i_compare].get('count') + 1.5 + round( cur_compare_row[i_compare].get('count') * 0.1 )
         minus_pixel_count_threshold = cur_compare_row[i_compare].get('count') - 1.5 - round( cur_compare_row[i_compare].get('count') * 0.1 )
                          
         if cur_original_row[i_original].get('original_count') <= pixel_count_threshold and cur_original_row[i_original].get('original_count') >= minus_pixel_count_threshold:
                              
            temp = {}
            temp[x_label] = cur_compare_row[i_compare].get('start_x')
            temp[y_label] = cur_compare_row[i_compare].get('start_y')                           
            temp[pixel_count_lable] = cur_compare_row[i_compare].get('count')
            temp[original_total_lable] = len(cur_original_row)
            # which original consecutive pixels matched. not how many original consecutive pixels matched but which position of it.
            temp[matched_orig_num_lable] = i_original + 1
                                 
            matched_rows.append(temp)
            


                              


# called from find_shapes_in_diff_frames
# this method is for comparing and finding same shape in different frames of video.

# I copied code from find_shapes_in_diff_frames for getting pixels in current row (y) so it is horrible
# but I stick with it for now. fix it later when I get time or feel the need.

# return is the result of comparison. return is dictionary with following form
# search_ended, single_pixel_count_match, matched_x, matched_y, matched_pixel_count, empty_matched_x, empty_matched_y
# search_ended is boolean. single_pixel_count_match's value is boolean. matched_x, y, count are values where original pixels matched.

def compare_w_shape(compare_pixels_dict, search_until, original_count_from_top, original_pixels_in_current_y, original_empty_pixels_in_current_y, shape_ids):

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

               compare_orig_comp_row(original_pixels_in_current_y, pixels_in_current_y, comparison_result, False)

               break

            x_counter_in_current_running_y += 1            
            continue
  
         # checking to see if x value is the last one in current running y
         if x_counter_in_current_running_y == x_numbers_in_current_running_y:


            # if current x value is next to the previous x value, x_value - 1 should equal prev_x_value. if there is any
            # empty pixels, x_value - 1 will be greater than prev_x_value
            if x_value - 1 > prev_x_value:
               
               # this is for previous pixels
               temp['count'] =  consecutive_x_counter
               pixels_in_current_y.append( temp )

               # now this is for the current pixel
               temp = {}
               temp['start_x'] = x_value
               temp['start_y'] = y
               temp['count'] = 1
               pixels_in_current_y.append( temp )
               

               empty_temp = {}
               empty_temp['start_x'] = prev_x_value + 1
               empty_temp['start_y'] = y
               empty_temp['count'] = x_value  - ( prev_x_value + 1) 
               empty_pixels_in_current_y.append( empty_temp )

            else:
               # current pixel is consecutive pixel with previous pixels
               # + 1 from "consecutive_x_counter + 1" is for the current pixel
               temp['count'] = consecutive_x_counter + 1
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
                     compare_orig_comp_row(original_pixels_in_current_y, pixels_in_current_y, comparison_result, False)
                 
                     compare_orig_comp_row(original_empty_pixels_in_current_y, empty_pixels_in_current_y, comparison_empty_result, True)


                     # comparing current row from original shape and compare shape has finished. go to next compare shape row and compare it with current original row if still left.
                     break

                  if len(original_empty_pixels_in_current_y) > 1 or len(empty_pixels_in_current_y) > 1:
                     # either one of shapes contain more than 1 empty pixels
                     
                     # if one row contains 4 consecutive pixels and another contains only 1, then it is not a match.
                     # all original consecutive pixels have to be satisfied. so if number of compare consecutive pixels are less than the number of original then, skip this.
                     if abs( len(original_pixels_in_current_y) - len(pixels_in_current_y) ) <= 2 and len(original_pixels_in_current_y) < len(pixels_in_current_y):
                        # when comparing consecutive pixels, the position matters. Above explained it so I'm not going to
                        # repeat here. But in here, there may be multiple consecutive pixels. 
                        # for example.
                        # 4 consecutive pixels. 2 consecutive pixels
                        # first one from 2 consecutive pixels will compare with first one from 4 consecutive pixels.
                        # if matched, go to next one. if matched, match is found, if not, start over. there is still 2 left in 
                        # 4 consecutive pixels, so third one frmo 4 consecutive pixels compare with first one from 2 consecutive pixels.
                        # if not matched, then it is not a match.
                        
                        '''
                        4 larger. 2. smaller
                        looping. first 0 - 3 last

                        0 from 4 compares with 0 from 2

                           if matched, increase needed_for_match_counter
                              check if needed_for_match_counter is greater than or equal to needed_for_match
                              if so, put all cnosecutive pixels into comparison_result
                              if not, because it's a match, increase needed_for_match_counter by 1

                           if not matched, make needed_for_match_counter 0
                              larger - 1 - i = number of consecutive pixels left for comparing
                              4 - 1 - 0 = 3 left
                              4 - 1 - 1 = 2 left

                              check if number of consecutive pixels left for comparing is greater than or equal to needed_for_match. if less,
                              then it means that not enough left for comparing, no match

                        1 from 4 compares with 1 from 2
                           
                           if matched, increase needed_for_match_counter
                              check if needed_for_match_counter is greater than or equal to needed_for_match
                              if so, put all cnosecutive pixels into comparison_result
                              
                        '''

                        compare_orig_comp_row(original_pixels_in_current_y, pixels_in_current_y, comparison_result, False)

                        compare_orig_comp_row(original_empty_pixels_in_current_y, empty_pixels_in_current_y, comparison_empty_result, True)
                            
                                                         
                        break
                        
                  
               else:
                  # compare shape has no empty pixels
                  
                  
                  if len(original_empty_pixels_in_current_y) == 1:
                     # row (y) in original shape contains only one consecutive empty pixels

                     compare_orig_comp_row(original_pixels_in_current_y, pixels_in_current_y, comparison_result, False)

                     # because compare shape has no empty pixels for comparing, the current original row is automatically unmatched.
                     
            else:
               # current original row does not have empty pixels

               if len(empty_pixels_in_current_y ) > 0:
                  # row (y) in compare shape contains empty pixels

                  if len(empty_pixels_in_current_y) == 1:
                     # row (y) in compare shape contains only one consecutive empty pixels
                     
                     compare_orig_comp_row(original_pixels_in_current_y, pixels_in_current_y, comparison_result, False)


               else:
                  # compare shape has no empty pixels
                  # both shapes have no empty pixels. so there is only one consecutive pixels
                  
                  compare_orig_comp_row(original_pixels_in_current_y, pixels_in_current_y, comparison_result, False)
                                 

            # go to next compare shape row
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
               matched_y_in_compare_shape, empty_matched_y_in_compare_shape = compare_w_shape(compare_pixels_dict, search_until, y - original_smallest_y, pixels_in_current_y, empty_pixels_in_current_y, shape_ids )
               
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


            
            # if last x value is next to the previous x value, x_value - 1 should equal prev_x_value. if there is any empty pixels
            # x_value - 1 will be greater than prev_x_value
            if x_value - 1 > prev_x_value:
               
               # this is for the previous pixels
               temp['original_count'] =  consecutive_x_counter
               pixels_in_current_y.append( temp )
               
               # now this is for the current pixel
               temp = {}
               temp['original_x'] = x_value
               temp['original_y'] = y
               temp['original_count'] = 1
               pixels_in_current_y.append(temp)

               empty_temp = {}
               empty_temp['original_x'] = prev_x_value + 1
               empty_temp['original_y'] = y
               empty_temp['original_count'] = x_value  - ( prev_x_value + 1) 
               empty_pixels_in_current_y.append( empty_temp )

            else:
               # current pixel is consecutive pixel with previous pixels
               # + 1 from "consecutive_x_counter + 1" is for the current pixel
               temp['original_count'] =  consecutive_x_counter + 1
               pixels_in_current_y.append( temp )

            
            # this temporary dictionary is for storing matched rows of original shape and compare shape
            #temp = {}
            # all consecutive pixels (both real pixels and empty pixels ) should have same y number
            #temp['original_y'] = pixels_in_current_y[0]['original_y']
                    
            # compare with another shape in different frame of image
            matched_y_in_compare_shape, empty_matched_y_in_compare_shape = compare_w_shape(compare_pixels_dict, search_until, y - original_smallest_y, pixels_in_current_y, empty_pixels_in_current_y, shape_ids)

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

                  # this count is for previous pixels
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
      result = process_real_p_rows(comparison_result, original_shape_height, compare_shape_height, shape_ids)
      if result:
         return result - ( pixel_count_diff * 0.5 )
      else:
         return result




















































































































































