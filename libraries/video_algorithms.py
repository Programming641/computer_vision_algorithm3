
from PIL import Image
import os
import math

from libraries import pixel_shapes_functions


# boundary relative position matches. 
def boundary_rel_pos(original_boundary_pixels, compare_boundary_pixels, shape_ids):

   original_smallest_y = min(int(d['y']) for d in original_boundary_pixels.values())
   original_largest_y = max(int(d['y']) for d in original_boundary_pixels.values())
   
   original_height = original_largest_y - original_smallest_y
   
   compare_smallest_y = min(int(d['y']) for d in compare_boundary_pixels.values())
   compare_largest_y = max(int(d['y']) for d in compare_boundary_pixels.values())
   
   compare_height = compare_largest_y - compare_smallest_y
   
   height_diff = abs(original_height - compare_height)
   
   starting_pixel = {}
   
   threshold = 3
   
   relative_boundary_pix = []
   
   #  for y in range(start, stop) stop value is excluded
   for y in range(original_smallest_y, original_largest_y + 1):

   
   
      # pixel_ids_with_current_y contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y = [k for k in original_boundary_pixels  if (int(original_boundary_pixels[k]['y'])) == y]
      
      
      # we first obtain all x values for the current running y value
      x_es_in_current_y = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y:
         # putting all x values for all xy coordinates that have current running y vaule
         x_es_in_current_y.append(original_boundary_pixels[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_es_in_current_y.sort()
      
      if original_smallest_y == y:
         leftMost_x = min( x_es_in_current_y )

         
         starting_pixel['starting_x'] = leftMost_x
         starting_pixel['starting_y'] = y
      
         relative_boundary_pix.append(starting_pixel)
         
      for x_values in x_es_in_current_y:
         temp = {}
         temp['x'] = x_values - starting_pixel['starting_x']
         temp['y'] = y - starting_pixel['starting_y']
         
         relative_boundary_pix.append(temp)
   
   
   original_couter = 0
   

   
   matches = []
   consecutive_list = []
   
   
   orig_ended = False
   comp_starting_pixel = {}
   pixel_counter = 0
   for i in range( 0, height_diff):
      temp_matches =[]
      consecutive_counter = 0
      prev_consec_counter = None
      for comp_y in range(compare_smallest_y, compare_largest_y + 1):   
         if comp_y == compare_largest_y + 1: 
            break   
        
        # for consecutive matches, number of pixel matches will be added.
         if consecutive_counter == 0:
            cur_pix_counter = 0      
            
         if original_couter + i > len(relative_boundary_pix) / 2 or original_couter > len(relative_boundary_pix) / 2:
            if prev_consec_counter and cur_pix_counter:
               temp = {}
               temp['consecutive'] = prev_consec_counter
               temp['num_pix_hit'] = cur_pix_counter
               consecutive_list.append(temp)
            
            
            orig_ended = True
  
            break
            


         
         # comp_pixel_ids_with_current_y contains all xy coordinate pairs that have the current running y value.
         comp_pixel_ids_with_current_y = [k for k in compare_boundary_pixels  if (int(compare_boundary_pixels[k]['y'])) == comp_y]
      
      
         # we first obtain all x values for the current running y value
         comp_x_es_in_current_y = []
      
      
         # key is the coordinate pair id.  
         for key in comp_pixel_ids_with_current_y:
            
            # putting all x values for all xy coordinates that have current running y vaule
            comp_x_es_in_current_y.append(compare_boundary_pixels[key]['x'])

      
         # we need to sort x values so that we can work with neighbor x values
         comp_x_es_in_current_y.sort()

         cur_comp_coord = {}
         if compare_smallest_y == comp_y:
            comp_leftMost_x = min( comp_x_es_in_current_y )

         
            comp_starting_pixel['starting_x'] = comp_leftMost_x
            comp_starting_pixel['starting_y'] = comp_y

         else:
            cur_orig_x_es = []
            
            # getting all x values for current y
            for orig_pixels in relative_boundary_pix:
               if 'y' in orig_pixels:
                  if orig_pixels['y'] == original_couter + i:
                     cur_orig_x_es.append( orig_pixels['x'] )
            
            once = False
            for comp_x_es in comp_x_es_in_current_y:
               cur_comp_coord['x'] = comp_x_es - comp_starting_pixel['starting_x']
               cur_comp_coord['y'] = comp_y - comp_starting_pixel['starting_y']
               
               
               for cur_orig_x in cur_orig_x_es:
                  
                  if abs( cur_orig_x - cur_comp_coord['x'] ) < threshold:
                     temp = {}
                     temp['original_x'] = cur_orig_x + starting_pixel['starting_x']
                     temp['original_y'] = original_couter + i + starting_pixel['starting_y']
                     temp['compare_x'] = comp_x_es
                     temp['compare_y'] = comp_y
                  
                     temp_matches.append(temp)
                     
                     cur_pix_counter += 1
                     
                     if not once:
                        # count consecutive for each row, and not for each pixel on the same row.
                        consecutive_counter += 1
                        once = True
               
         if prev_consec_counter == None:
            prev_consec_counter = consecutive_counter
         elif prev_consec_counter == consecutive_counter:
            # consecutive_counter has not changed from prev_consec_counter. this means that current y did not match. consecutiveness ended
            # at current y
            temp = {}
            temp['consecutive'] = prev_consec_counter
            temp['num_pix_hit'] = cur_pix_counter
            consecutive_list.append(temp)
            
            consecutive_counter = 0
            
         prev_consec_counter = consecutive_counter   
         original_couter += 1
      
      if not matches:
         matches = temp_matches
      elif len(temp_matches) > len(matches):
         matches = temp_matches
      
      if orig_ended:
         break
   
   
   consecutive_counter = 0
   for consecutive in consecutive_list:
      if consecutive['consecutive'] != 0:
         consecutive_counter += consecutive['consecutive'] * ( consecutive['num_pix_hit'] * 0.3 )

   if len(original_boundary_pixels) > len(compare_boundary_pixels):
      possible_match_count = len(compare_boundary_pixels)
   else:
      possible_match_count = len(original_boundary_pixels)

  
   print("boundary_rel_pos matched " + str(len(matches)) + " out of " + str(possible_match_count) )
   return len(matches)
   




def find_direct_n_far_consecutives(row_column_results, row_or_column ):

   if row_or_column == "row":
      original_x_or_y = 'original_y'
      compare_x_or_y = 'compare_y'
   else:
      original_x_or_y = 'original_x'
      compare_x_or_y = 'compare_x'      

   consecutives_results = []
   prev_original_xy = None
   prev_compare_xy = None


   one_consecutive = []
   counter = 0
   for r_c_result in row_column_results:
      
      if not prev_original_xy:
         prev_original_xy = r_c_result[original_x_or_y]
         prev_compare_xy = r_c_result[compare_x_or_y]
      
      
      
      if r_c_result[original_x_or_y] == prev_original_xy + 1 and r_c_result[compare_x_or_y] == prev_compare_xy + 1:
         if not row_column_results[counter - 1] in one_consecutive:
            one_consecutive.append(row_column_results[counter - 1])
         
         one_consecutive.append(row_column_results[counter])
         
      else:
         if one_consecutive:
            consecutives_results.append(one_consecutive)
         
            one_consecutive = []
         
      
      prev_original_xy = r_c_result[original_x_or_y]
      prev_compare_xy =  r_c_result[compare_x_or_y]
      counter += 1
         
   
   consecutives_results = sorted( consecutives_results , key=lambda item: item[0][original_x_or_y]  )
   

   
   orig_distance_diff_threshold = 4 
   
   final_consecutive_results = []
   
   for consecutives_result in consecutives_results:
      final_consecutive_result = []

      cur_smallest_orig_xy = None
      cur_smallest_comp_xy = None
      cur_biggest_orig_xy = None
      cur_biggest_comp_xy = None


      for one_consec in consecutives_result:

         if cur_smallest_orig_xy == None:
             cur_smallest_orig_xy = one_consec[original_x_or_y]
             cur_smallest_comp_xy = one_consec[compare_x_or_y]
             cur_biggest_orig_xy = one_consec[original_x_or_y]
             cur_biggest_comp_xy = one_consec[compare_x_or_y]
             
             temp = {}
             temp[original_x_or_y] = one_consec[original_x_or_y]
             temp[compare_x_or_y] = one_consec[compare_x_or_y]
             
             final_consecutive_result.append(temp)
             
         else:
            if cur_smallest_orig_xy > one_consec[original_x_or_y]:
               cur_smallest_orig_xy = one_consec[original_x_or_y]
            if cur_smallest_comp_xy > one_consec[compare_x_or_y]:
               cur_smallest_comp_xy = one_consec[compare_x_or_y]
               
            if cur_biggest_orig_xy < one_consec[original_x_or_y]:
               cur_biggest_orig_xy = one_consec[original_x_or_y]
            if cur_biggest_comp_xy < one_consec[compare_x_or_y]:
               cur_biggest_comp_xy = one_consec[compare_x_or_y]

         
      for another_consecutive_result in consecutives_results:

         if another_consecutive_result == consecutives_result:
            # itself
            continue


         another_cur_smallest_orig_xy = None
         another_cur_smallest_comp_xy = None
         another_cur_biggest_orig_xy = None
         another_cur_biggest_comp_xy = None
         for another_one_consec in another_consecutive_result:
            
            if another_cur_smallest_orig_xy == None:
               another_cur_smallest_orig_xy = another_one_consec[original_x_or_y]
               another_cur_smallest_comp_xy = another_one_consec[compare_x_or_y]
               another_cur_biggest_orig_xy = another_one_consec[original_x_or_y]
               another_cur_biggest_comp_xy = another_one_consec[compare_x_or_y]
             
            else:
               if another_cur_smallest_orig_xy > another_one_consec[original_x_or_y]:
                  another_cur_smallest_orig_xy = another_one_consec[original_x_or_y]
               if another_cur_smallest_comp_xy > another_one_consec[compare_x_or_y]:
                  another_cur_smallest_comp_xy = another_one_consec[compare_x_or_y]
               
               if another_cur_biggest_orig_xy < another_one_consec[original_x_or_y]:
                  another_cur_biggest_orig_xy = another_one_consec[original_x_or_y]
               if another_cur_biggest_comp_xy < another_one_consec[compare_x_or_y]:
                  another_cur_biggest_comp_xy = another_one_consec[compare_x_or_y]


         consecutive = False

         if another_cur_smallest_orig_xy - cur_biggest_orig_xy > 0:
            # another_consecutive_result is bigger than consecutives_result. this means there there is no need to compare consecutives_result's smallest y.
            
            
            orig_distance_diff = another_cur_smallest_orig_xy - cur_biggest_orig_xy
            comp_distance_diff = another_cur_smallest_comp_xy - cur_biggest_comp_xy
            
            
            if comp_distance_diff < orig_distance_diff + orig_distance_diff_threshold:
               if comp_distance_diff > orig_distance_diff - orig_distance_diff_threshold and another_cur_smallest_comp_xy > cur_biggest_comp_xy:
                  consecutive = True
                  
                  
            if consecutive:
               temp = {}
               temp[original_x_or_y] = another_cur_smallest_orig_xy
               temp[compare_x_or_y] = another_cur_smallest_comp_xy
               
               final_consecutive_result.append(temp)
      
         else:
            # another_consecutive_result is smaller than consecutives_result
           
            orig_distance_diff = cur_smallest_orig_xy - another_cur_biggest_comp_xy
            comp_distance_diff = cur_smallest_comp_xy - another_cur_biggest_comp_xy

            if comp_distance_diff < orig_distance_diff + orig_distance_diff_threshold:
               if comp_distance_diff > orig_distance_diff - orig_distance_diff_threshold and cur_smallest_comp_xy > another_cur_biggest_comp_xy:
                  consecutive = True
                  
                  
            if consecutive:
               temp = {}
               temp[original_x_or_y] = another_cur_smallest_orig_xy
               temp[compare_x_or_y] = another_cur_smallest_comp_xy
                      
               final_consecutive_result.append(temp)
         
   
      final_consecutive_results.append(final_consecutive_result)

   
   # final_consecutive_results contains subsets. delete all subsets and keep only superset.
   # example. superset 1,2,3,4,5. subset. 1. subset 2.3.4. subset. 1.5.

   f_consec_results = list(final_consecutive_results)

   # final_consecutive_results contains subsets. delete all subsets and keep only superset.
   # example. superset 1,2,3,4,5. subset. 1. subset 2.3.4. subset. 1.5.
   for superset_list in final_consecutive_results:
   
      for subset_list in final_consecutive_results:

         subset_counter = 0
         for one_consec in superset_list:
      
            for another_consec in subset_list:

               if one_consec == another_consec:

                  # make sure this subset_list is not superset_list itself
                  if superset_list == subset_list:
                     break
            
                  subset_counter += 1
                  
                  if subset_counter == len(subset_list):
                     for delete_subset in f_consec_results:
                        if delete_subset == subset_list:
                           f_consec_results.remove(delete_subset)
                     
  
   
   # direct_consecutive_total is direct neighbors in consecutives_results
   # example. [{'original_y': 124, 'result': 1, 'compare_y': 272}, {'original_y': 125, 'result': 2, 'compare_y': 273}]
   # 124 -> 125. and compare is also + 1. 272 -> 273.
   direct_consecutive_total = None

   # consecutives are not direct neighbors but they are almost same distance away.
   # example. 
   #  [{'original_y': 171, 'result': 2, 'compare_y': 313}, {'original_y': 172, 'result': 2, 'compare_y': 314}],
   #  [{'original_y': 173, 'result': 2, 'compare_y': 317}, {'original_y': 174, 'result': 2, 'compare_y': 318}]
   #  original_y 172 -> 173. compare_y 314 -> 317
   #  original and compare are in the same direction and the changed amount is within the threshold
   far_consecutive_total = None

   for f_consec_result in f_consec_results:
      far_consecutives_counter = 0
      cur_far_consecutives_total = 0
   
      for each_result in f_consec_result:
      
         # current f_consec_result contains only one and already added everything in consecutives_result
         if len(f_consec_result) == 1 and far_consecutives_counter == 1:
            break      

         for consecutives_result in consecutives_results:
         
            # current f_consec_result contains only one and already added everything in consecutives_result
            if len(f_consec_result) == 1 and far_consecutives_counter == 1:
               break
            
            cur_direct_total = 0
            hit = False
            for each_consecutive in consecutives_result:
               if each_result[original_x_or_y] == each_consecutive[original_x_or_y]:
                  # this consecutives_result contains each_result. so we need to get all each_consecutive from consecutives_result
                  hit = True
                  far_consecutives_counter += 1
               
               if hit:
                  cur_direct_total += each_consecutive['result']
               
                  if len(f_consec_result) > 1 and far_consecutives_counter <= len(f_consec_result):
                     cur_far_consecutives_total += each_consecutive['result']

            if hit:
               cur_direct_total *= len(consecutives_result)
         
            if not direct_consecutive_total:
               direct_consecutive_total = cur_direct_total
            else:
               direct_consecutive_total += cur_direct_total
            

         # last one for the far away consecutives pixels
         if len(f_consec_result) > 1 and far_consecutives_counter == len(f_consec_result):
            cur_far_consecutives_total *= len(f_consec_result)
            far_consecutive_total = cur_far_consecutives_total * 0.5   
   
   
   return direct_consecutive_total, far_consecutive_total






def process_boundaries_vertically(original_boundary_pixels, compare_boundary_pixels, shape_ids, filenames):


   def get_compare_column(compare_boundary_pixels, compare_column_counter):
   

      # pixel_ids_with_current_x contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_x = [k for k in compare_boundary_pixels  if (int(compare_boundary_pixels[k]['x'])) == compare_column_counter]

      # we first obtain all x values for the current running x value
      y_values_list_in_current_x = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_x:
         # putting all x values for all xy coordinates that have current running x vaule
         y_values_list_in_current_x.append(compare_boundary_pixels[key]['y'])

      
      # we need to sort y values so that we can work with neighbor y values
      y_values_list_in_current_x.sort()      
      
      return y_values_list_in_current_x



   def get_column_consecutives(y_values_list_in_current_x):
   
      column_consecutives = {}
      prev_y_value = None
      consecutive_nums = None
      counter = 0
      for y_value in y_values_list_in_current_x:
         counter += 1
         if  prev_y_value == None:
            consecutive_nums = 1
            prev_y_value = y_value
            top = y_value
         else:
            if not y_value == prev_y_value + 1:

               bottom = prev_y_value
               temp = {'top': top, 'bottom': bottom}
               column_consecutives[consecutive_nums] = temp      
         
         
               top = y_value
   
               consecutive_nums += 1
      
         prev_y_value = y_value

         if counter >= len(y_values_list_in_current_x):
            bottom = prev_y_value
            temp = {'top': top, 'bottom': bottom}
            column_consecutives[consecutive_nums] = temp     
   
      return column_consecutives
   





   original_smallest_x = min(int(d['x']) for d in original_boundary_pixels.values())
   original_largest_x = max(int(d['x']) for d in original_boundary_pixels.values())
   
   original_shape_width = original_largest_x - original_smallest_x

   compare_smallest_x = min(int(d['x']) for d in compare_boundary_pixels.values())
   compare_largest_x = max(int(d['x']) for d in compare_boundary_pixels.values())
  
   
   compare_shape_width = compare_largest_x - compare_smallest_x
   
   # when original shape is smaller in width, every original x has to compare with at least
   # width_diff amount of compare shape from left. To be more safe, width_diff + ( original width / 5 ) would be more effective at finding matches.
   # when original shape is bigger in width, every original x has to compare with at least width_diff amount of compare shape from left.   
   width_diff = original_shape_width - compare_shape_width
   
   original_column_counter = 0
   
   prev_bottom_y = None
   comp_prev_bottom_y = None
   prev_top_y = None
   comp_prev_top_y = None

   consecutive_columns = []
   column_results = []
   debug_column_results = []
   # for loop for going from smallest x value to the largest x value
   # this means going from left to right
   #  for x in range(start, stop) stop value is excluded
   for x in range(original_smallest_x, original_largest_x + 1):
      
      original_column_counter += 1

      # pixel_ids_with_current_x contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_x = [k for k in original_boundary_pixels  if (int(original_boundary_pixels[k]['x'])) == x]
      
      
      # we first obtain all x values for the current running x value
      y_values_list_in_current_x = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_x:
         # putting all y values for all xy coordinates that have current running x vaule
         y_values_list_in_current_x.append(original_boundary_pixels[key]['y'])

      
      # we need to sort y values so that we can work with neighbor y values
      y_values_list_in_current_x.sort()
         
      #print("y_values_list_in_current_x " + str(y_values_list_in_current_x) )
      
      bottom_y = max( y_values_list_in_current_x )
      top_y = min( y_values_list_in_current_x )
 
      bottom_y_diff =  top_y_diff = None
      if prev_bottom_y != None:
         bottom_y_diff = bottom_y - prev_bottom_y
         
      if prev_top_y != None:
         top_y_diff = bottom_y - prev_top_y


      '''
      top and bottom pixel of every consecutive pixels.
      number of every consecutive pixels to know the locations of them.
      
      75, 76, 80, 89, 90
      top pixel 75, bottom pixel 76. top pixel 80. 1 pixel so no bottom pixel. top pixel 89, bottom pixel 90
      1:top pixel 75, bottom pixel 76.
      
      dictionary key is number of every consecutive pixels. value are top pixel and bottom pixel.

      once we know all pixels locations, we can get their relative locations from previous column. then we can use this relative locations
      to compare with compare shape's relative locations. if both relative locations match, the match is found.
      '''
      orig_consecutives = get_column_consecutives(y_values_list_in_current_x)


      #print("orig_consecutives " + str(orig_consecutives ) )

      # either original shape is wider or thinner than compare shape, every original x has to compare with at least the width difference amount 
      # from left of original or compare shape.
      for every_x in range( compare_smallest_x , original_column_counter + compare_smallest_x + abs(width_diff) ):
         if every_x == compare_largest_x + 1: 
            break         
            
         compare_cur_column = get_compare_column(compare_boundary_pixels, every_x)

         #print("compare_cur_column " + str(compare_cur_column ) )
      
         comp_bottom_y = max( compare_cur_column )
         comp_top_y = min( compare_cur_column )
      
         comp_bottom_y_diff = comp_top_y_diff = None
         if comp_prev_bottom_y != None:
            comp_bottom_y_diff = comp_bottom_y - comp_prev_bottom_y
      
         if comp_prev_top_y != None:
            comp_top_y_diff = comp_top_y - comp_prev_top_y
         
         
         if bottom_y_diff != None and top_y_diff != None and comp_bottom_y_diff != None and comp_top_y_diff != None:
            if abs( bottom_y_diff - comp_bottom_y_diff ) < 2 and abs( top_y_diff - comp_top_y_diff ) < 2:
               consecutive_columns.append(x - 1)
               consecutive_columns.append(x)
      
      
      
         comp_consecutives = get_column_consecutives(compare_cur_column)


         #print("comp_consecutives " + str(comp_consecutives ) )
      
         column_match = 0
         total_pixels = 0

         # comparing orig_consecutives and comp_consecutives
         # example. {1: {'top': 0, 'bottom': 5}}
         # first, number of consecutives must match. if matched, pixel counts for each consecutives must be within the threshold
         orig_consecutives= dict(sorted(orig_consecutives.items(), key=lambda item: item[0]))       
         comp_consecutives= dict(sorted(comp_consecutives.items(), key=lambda item: item[0]))         
      
         orig_prev_bottom = None
         comp_prev_bottom = None


         if len( orig_consecutives.keys()) == len( comp_consecutives.keys() ):
            for orig_location in orig_consecutives:
               for comp_location in comp_consecutives:

                  if orig_location == comp_location:
                     if orig_prev_bottom == None and comp_prev_bottom == None:

                        orig_prev_bottom = orig_consecutives[orig_location]['bottom']
                        comp_prev_bottom = comp_consecutives[comp_location]['bottom']
                              
                        orig_pixels = orig_consecutives[orig_location]['bottom'] - orig_consecutives[orig_location]['top']
                        comp_pixels = comp_consecutives[comp_location]['bottom'] - comp_consecutives[comp_location]['top']

                        if abs( orig_pixels - comp_pixels ) < 3:
                           column_match += 1
                           
                     else:
                        orig_gap = orig_consecutives[orig_location]['top'] - orig_prev_bottom
                        comp_gap = comp_consecutives[comp_location]['top'] - comp_prev_bottom
                        
                        if abs( orig_gap - comp_gap ) < 3:
                           column_match += 1
                              
                        orig_pixels = orig_consecutives[orig_location]['bottom'] - orig_consecutives[orig_location]['top']
                        comp_pixels = comp_consecutives[comp_location]['bottom'] - comp_consecutives[comp_location]['top']

                        if abs( orig_pixels - comp_pixels ) < 3:
                           column_match += 1                           

                        orig_prev_bottom = orig_consecutives[orig_location]['bottom']
                        comp_prev_bottom = comp_consecutives[comp_location]['bottom']
                        
                        
                  
         if column_match >= ( len( orig_consecutives.keys()) * 2 ) - 1:
            match = True
            for column_result in column_results:
               if column_result['compare_x'] == every_x or column_result['original_x'] == x:
                  match = False
            if match:
               temp = {}
               temp['original_x'] = x
               temp['result'] = len( orig_consecutives.keys())    # how many matched
               temp['compare_x'] = every_x
               
               #print("column matched")
               #print(temp)
               column_results.append( temp )
               

               # for debug displaying matched places in the image
               # getting all matched original xy values
               for orig_consec_num in orig_consecutives.values():

                  for debug_orig_y in range( orig_consec_num['top'] , orig_consec_num['bottom'] + 1 ):
                     temp = {}
                     temp['original_x'] = x
                     temp['original_y'] = debug_orig_y
                     
                     debug_column_results.append(temp)
               
               for comp_consec_num in comp_consecutives.values():
                  for debug_comp_y in range( comp_consec_num['top'] , comp_consec_num['bottom'] + 1 ):
                     temp = {}
                     temp['compare_x'] = every_x
                     temp['compare_y'] = debug_comp_y
                     
                     debug_column_results.append(temp)

               
      
         prev_bottom_y = bottom_y
         comp_prev_bottom_y = comp_bottom_y
         prev_top_y = top_y
         comp_prev_top_y = comp_top_y


   column_results = sorted( column_results , key=lambda item: item['original_x']  )
   
   pixel_shapes_functions.highlight_matches( shape_ids, filenames, debug_column_results )
   
   
   final_results = 0
   
   direct_consecutive_total = None
   far_consecutive_total = None   
   
   direct_consecutive_total, far_consecutive_total = find_direct_n_far_consecutives(column_results, "column" )
   
   if direct_consecutive_total:
      final_results += direct_consecutive_total
   if far_consecutive_total:
      final_results += far_consecutive_total

   print("virtical boundary final_results " + str(final_results) )

   return final_results







   


def process_boundaries(original_boundary_pixels, compare_boundary_pixels, shape_ids, filenames):

   def get_compare_row(compare_boundary_pixels, compare_row_counter):
   

      # pixel_ids_with_current_y contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y = [k for k in compare_boundary_pixels  if (int(compare_boundary_pixels[k]['y'])) == compare_row_counter]

      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y:
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(compare_boundary_pixels[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()      
      
      return x_values_list_in_current_y



   def get_row_consecutives(x_values_list_in_current_y):
   
      row_consecutives = {}
      prev_x_value = None
      consecutive_nums = None
      counter = 0
      for x_value in x_values_list_in_current_y:
         counter += 1
         if  prev_x_value == None:
            consecutive_nums = 1
            prev_x_value = x_value
            leftmost = x_value
         else:
            if not x_value == prev_x_value + 1:

               rightmost = prev_x_value
               temp = {'leftmost': leftmost, 'rightmost': rightmost}
               row_consecutives[consecutive_nums] = temp      
         
         
               leftmost = x_value
   
               consecutive_nums += 1
      
         prev_x_value = x_value

         if counter >= len(x_values_list_in_current_y):
            rightmost = prev_x_value
            temp = {'leftmost': leftmost, 'rightmost': rightmost}
            row_consecutives[consecutive_nums] = temp     
   
      return row_consecutives
   





   original_smallest_y = min(int(d['y']) for d in original_boundary_pixels.values())
   original_largest_y = max(int(d['y']) for d in original_boundary_pixels.values())
   
   original_shape_height = original_largest_y - original_smallest_y

   compare_smallest_y = min(int(d['y']) for d in compare_boundary_pixels.values())
   compare_largest_y = max(int(d['y']) for d in compare_boundary_pixels.values())
  
   
   compare_shape_height = compare_largest_y - compare_smallest_y
   
   # when original shape is smaller in height, every original y has to compare with at least
   # height_diff amount of compare shape from top. To be more safe, height_diff + ( original height / 5 ) would be more effective at finding matches.
   # when original shape is bigger in height, every original y has to compare with at least height_diff amount of compare shape from top.   
   height_diff = original_shape_height - compare_shape_height
   
   original_row_counter = 0
   
   prev_rightMost_x = None
   comp_prev_rightMost_x = None
   prev_leftMost_x = None
   comp_prev_leftMost_x = None

   consecutive_rows = []
   row_results = []
   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(original_smallest_y, original_largest_y + 1):
      
      original_row_counter += 1

      # pixel_ids_with_current_y contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y = [k for k in original_boundary_pixels  if (int(original_boundary_pixels[k]['y'])) == y]    
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y:
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(original_boundary_pixels[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
      
      #print("original current row number " + str(y ) )
      #print("x_values_list_in_current_y " + str(x_values_list_in_current_y) )
      
      rightMost_x = max( x_values_list_in_current_y )
      leftMost_x = min( x_values_list_in_current_y )
 
      rightMost_x_diff =  leftMost_x_diff = None
      if prev_rightMost_x != None:
         rightMost_x_diff = rightMost_x - prev_rightMost_x
         
      if prev_leftMost_x != None:
         leftMost_x_diff = leftMost_x - prev_leftMost_x


      '''
      leftmost and rightmost pixel of every consecutive pixels.
      number of every consecutive pixels to know the locations of them.
      
      75, 76, 80, 89, 90
      leftmost pixel 75, rightmost pixel 76. leftmost pixel 80. 1 pixel so no right pixel. leftmost pixel 89, rightmost pixel 90
      1:leftmost pixel 75, rigthmost pixel 76.
      
      dictionary key is number of every consecutive pixels. value are leftmost pixel and rightmost pixel.

      once we know the all pixels locations, we can get their relative locations from previous row. then we can use this relative locations
      to compare with compare shape's relative locations. Both relative locations match, the match is found.
      '''
      orig_consecutives = get_row_consecutives(x_values_list_in_current_y)


      #print("orig_consecutives " + str(orig_consecutives ) )

      # either original shape is taller or shorter than compare shape, every original y has to compare with at least the height difference amount 
      # from top of original or compare shape.
      for every_y in range( compare_smallest_y , original_row_counter + compare_smallest_y + abs(height_diff) ):
         if every_y == compare_largest_y + 1: 
            break         
            
         compare_cur_row = get_compare_row(compare_boundary_pixels, every_y)

         #print("compare current row number " + str(every_y) )
         #print("compare_cur_row " + str(compare_cur_row ) )
      
         comp_rightMost_x = max( compare_cur_row )
         comp_leftMost_x = min( compare_cur_row )
      
         comp_rightMost_x_diff = comp_leftMost_x_diff = None
         if comp_prev_rightMost_x != None:
            comp_rightMost_x_diff = comp_rightMost_x - comp_prev_rightMost_x
      
         if comp_prev_leftMost_x != None:
            comp_leftMost_x_diff = comp_leftMost_x - comp_prev_leftMost_x
         
         
         if rightMost_x_diff != None and leftMost_x_diff != None and comp_rightMost_x_diff != None and comp_leftMost_x_diff != None:
            if abs( rightMost_x_diff - comp_rightMost_x_diff ) < 2 and abs( leftMost_x_diff - comp_leftMost_x_diff ) < 2:
               consecutive_rows.append(y - 1)
               consecutive_rows.append(y)
      
      
      
         comp_consecutives = get_row_consecutives(compare_cur_row)


         #print("comp_consecutives " + str(comp_consecutives ) )
      
         row_match = 0
         total_pixels = 0

         # comparing orig_consecutives and comp_consecutives
         # example. {1: {'leftmost': 0, 'rightmost': 5}}
         # first, number of consecutives must match. if matched, pixel counts for each consecutives must be within the threshold
         orig_consecutives= dict(sorted(orig_consecutives.items(), key=lambda item: item[0]))       
         comp_consecutives= dict(sorted(comp_consecutives.items(), key=lambda item: item[0]))         
      
         orig_prev_rightmost = None
         comp_prev_rightmost = None


         if len( orig_consecutives.keys()) == len( comp_consecutives.keys() ):
            for orig_location in orig_consecutives:
               for comp_location in comp_consecutives:

                  if orig_location == comp_location:
                     if orig_prev_rightmost == None and comp_prev_rightmost == None:

                        orig_prev_rightmost = orig_consecutives[orig_location]['rightmost']
                        comp_prev_rightmost = comp_consecutives[comp_location]['rightmost']
                              
                        orig_pixels = orig_consecutives[orig_location]['rightmost'] - orig_consecutives[orig_location]['leftmost']
                        comp_pixels = comp_consecutives[comp_location]['rightmost'] - comp_consecutives[comp_location]['leftmost']

                        if abs( orig_pixels - comp_pixels ) < 3:
                           row_match += 1
                           
                     else:
                        orig_gap = orig_consecutives[orig_location]['leftmost'] - orig_prev_rightmost
                        comp_gap = comp_consecutives[comp_location]['leftmost'] - comp_prev_rightmost
                        
                        if abs( orig_gap - comp_gap ) < 3:
                           row_match += 1
                              
                        orig_pixels = orig_consecutives[orig_location]['rightmost'] - orig_consecutives[orig_location]['leftmost']
                        comp_pixels = comp_consecutives[comp_location]['rightmost'] - comp_consecutives[comp_location]['leftmost']

                        if abs( orig_pixels - comp_pixels ) < 3:
                           row_match += 1                           

                        orig_prev_rightmost = orig_consecutives[orig_location]['rightmost']
                        comp_prev_rightmost = comp_consecutives[comp_location]['rightmost']
                        
                        
                  
         if row_match >= ( len( orig_consecutives.keys()) * 2 ) - 1:
            match = True
            for row_result in row_results:
               if row_result['compare_y'] == every_y or row_result['original_y'] == y:
                  match = False
            if match:
               temp = {}
               temp['original_y'] = y
               temp['result'] = len( orig_consecutives.keys())
               temp['compare_y'] = every_y
               
               #print("row matched")
               #print(temp)

               row_results.append( temp )
      
         prev_rightMost_x = rightMost_x
         comp_prev_rightMost_x = comp_rightMost_x
         prev_leftMost_x = leftMost_x
         comp_prev_leftMost_x = comp_leftMost_x


   row_results = sorted( row_results , key=lambda item: item['original_y']  )
   #print("row_results")
   #print(row_results)
   
   
   direct_consecutive_total = None
   far_consecutive_total = None
   
   direct_consecutive_total, far_consecutive_total = find_direct_n_far_consecutives(row_results, "row" )
   
   
   final_results = 0
   
   if direct_consecutive_total:
      final_results += direct_consecutive_total
   if far_consecutive_total:
      final_results += far_consecutive_total
   
                  
      
   
   print("horizontal boundary final_results " + str(final_results) )
   
   virtical_resuls = process_boundaries_vertically(original_boundary_pixels, compare_boundary_pixels, shape_ids, filenames)

   return final_results + virtical_resuls



def evaluate_1_orig_matches(one_orig_matches, row_or_column, empty_flag):


   if row_or_column == "row":
      orig_x_or_y_label = 'original_y'
      x_or_y_label = 'matched_y'
      x_or_y_dis_label = 'y_distance'
      matched_orig_num_label = 'matched_original_num'
      pixel_count_label = 'matched_pixel_count'
      if empty_flag:
         x_or_y_label = 'empty_matched_y'
   else:
      orig_x_or_y_label = 'original_x'
      x_or_y_label = 'matched_x'
      x_or_y_dis_label = 'x_distance'
      matched_orig_num_label = 'matched_original_num'
      pixel_count_label = 'matched_pixel_count'
      if empty_flag:
         x_or_y_label = 'empty_matched_x'
         
   if empty_flag:
      matched_orig_num_label = 'empty_matched_original_num'
      pixel_count_label = 'empty_pixel_count'        


   same_xy_dis = []
   
   # stores already added ids for x/y distances
   added_ids_4_xy_dis = []
   # stores already added ids for same direction
   added_ids_4_same_dir = []
   
   # match pairs that only have same direction
   same_dir_list = []
   
   for one_orig_match in one_orig_matches:
      original_xy = one_orig_match[orig_x_or_y_label]
      compare_xy = one_orig_match[x_or_y_label]
      id_num = one_orig_match['id_num']
      original_num = one_orig_match[matched_orig_num_label]
      
      # all compare consecutive pixels x distances
      cur_xy_distance = []

      
      for another_orig_match in one_orig_matches:
         if original_num != another_orig_match[matched_orig_num_label]:
            # same original consecutive pixels have to be matched
            continue
   
         same_direction = False
         if original_xy - another_orig_match[orig_x_or_y_label] > 0:
            if compare_xy - another_orig_match[x_or_y_label] > 0:
               # original and compare are both positive increase
               same_direction = True
         else:
            if compare_xy - another_orig_match[x_or_y_label] < 0:
               # original and compare are both negative decrease
               same_direction = True
               
         if not same_direction:
            # either positive increase or decrease. so it also excludes itself
            continue

         # at this point, compare consecutive pixels have same original consecutive pixels matched and direction is the same.
         
         # make sure it is not already added
         if another_orig_match['id_num'] in added_ids_4_xy_dis:
            continue
         
         
         xy_distance = another_orig_match[orig_x_or_y_label] - original_xy
         compare_xy_distance = another_orig_match[x_or_y_label] - compare_xy
         
         if xy_distance - compare_xy_distance == 0:
            temp = {}
            temp['id_num'] = id_num
            temp['id_num2'] = another_orig_match['id_num']
            
            # same amount increase or decrease
            temp[x_or_y_dis_label] = xy_distance
         
            cur_xy_distance.append(temp)
            
            added_ids_4_xy_dis.append(another_orig_match['id_num'])
            added_ids_4_xy_dis.append(id_num)
      
         elif not id_num in added_ids_4_same_dir and not another_orig_match['id_num'] in added_ids_4_same_dir:
            # adding ones that matched same direction only.
            temp = {}
            temp['id_num'] = id_num
            temp['id_num2'] = another_orig_match['id_num']
            
            same_dir_list.append(temp)
            
            added_ids_4_same_dir.append(id_num)
            added_ids_4_same_dir.append(another_orig_match['id_num'])

      
      # add to same_xy_dis only if same distance pair is found
      if cur_xy_distance:
         same_xy_dis.append(cur_xy_distance)

   
   same_dir_totals = 0
   for same_dir in same_dir_list:
      for pixel_count in one_orig_matches: 
         if same_dir['id_num'] == pixel_count['id_num']:
            same_dir_totals += pixel_count[pixel_count_label]
         
         if same_dir['id_num2'] == pixel_count['id_num']:
            same_dir_totals += pixel_count[pixel_count_label]

   same_dir_totals *= 0.1
   
   same_xy_list_total = 0
   for same_xy_dis_list in same_xy_dis:
      one_list_total = 0
      for one_consec in same_xy_dis_list:
         for pixel_count in one_orig_matches:
            if one_consec['id_num'] == pixel_count['id_num']:
               one_list_total += pixel_count[pixel_count_label]
   
            if one_consec['id_num2'] == pixel_count['id_num']:
               one_list_total += pixel_count[pixel_count_label]
      
      one_list_total *= 0.3
      # multiply by number of consecutives in each list
      one_list_total *= ( len(same_xy_dis_list) * 0.3 )
      
      same_xy_list_total += one_list_total
      
   return same_dir_totals, same_xy_list_total




def process_real_p_rows_matches(matched_rows, empty_flag):


   if empty_flag:
      x_label = 'empty_matched_x'
      y_label = 'empty_matched_y'
      pixel_count_label = 'empty_pixel_count'
      original_total_label = 'empty_original_totals'
      matched_orig_num_label = 'empty_matched_original_num'
   else:
      x_label = 'matched_x'
      y_label = 'matched_y'
      pixel_count_label = 'matched_pixel_count'
      original_total_label = 'matched_original_totals'
      matched_orig_num_label = 'matched_original_num'      



   def calculate_x_distances(multiple_consec_comp_in_row, comp_consec_pix):

      temp = {}
      temp['id_num'] = comp_consec_pix['id_num']
      temp['id_num2'] = multiple_consec_comp_in_row['id_num']
                  
               
      # checking direction of matched original x
      if multiple_consec_comp_in_row[matched_orig_num_label] < comp_consec_pix[matched_orig_num_label]:
                     
         if comp_consec_pix[x_label] - multiple_consec_comp_in_row[x_label] > 0:
            temp['x_direction'] = True
                        
            comp_x_distance = abs( comp_consec_pix[x_label] - multiple_consec_comp_in_row[x_label] )
            orig_x_distance = comp_consec_pix['original_x'] - multiple_consec_comp_in_row['original_x']
            x_distance_diff = abs( comp_x_distance - orig_x_distance )
                        
            temp['x_distance_diff'] = x_distance_diff
            temp[pixel_count_label + str(comp_consec_pix['id_num'])] = comp_consec_pix[pixel_count_label]
            temp[pixel_count_label + str(multiple_consec_comp_in_row['id_num']) ] = multiple_consec_comp_in_row[pixel_count_label]
         
         else:
            temp['x_direction'] = False
         
      else:
                     
         if multiple_consec_comp_in_row[x_label] - comp_consec_pix[x_label] > 0:
            temp['x_direction'] = True
                        
            comp_x_distance = abs( multiple_consec_comp_in_row[x_label] - comp_consec_pix[x_label] )
            orig_x_distance = multiple_consec_comp_in_row['original_x'] - comp_consec_pix['original_x']
            x_distance_diff = abs( comp_x_distance - orig_x_distance )
                   
            temp['x_distance_diff'] = x_distance_diff                   
            temp[pixel_count_label + str(comp_consec_pix['id_num'])] = comp_consec_pix[pixel_count_label]
            temp[pixel_count_label + str(multiple_consec_comp_in_row['id_num'])] = multiple_consec_comp_in_row[pixel_count_label]                        
                        
         else:
            temp['x_direction'] = False     

      if temp['x_direction'] != False:
          
         comp_count = ( temp[pixel_count_label + str(comp_consec_pix['id_num'])] + temp[pixel_count_label + str(multiple_consec_comp_in_row['id_num'])] ) * 4
         x_distance = comp_count - ( temp['x_distance_diff'] * 2 )
         
         print("x_distance")
         print( " id_num " + str(temp['id_num']) + " id_num2 " + str(temp['id_num2']) + " id_num pixel count " + str(temp[pixel_count_label + str(comp_consec_pix['id_num'])] ) + " id_num2 pixel count " + str(temp[pixel_count_label + str(multiple_consec_comp_in_row['id_num'])] ) + " x_distance_diff " + str(temp['x_distance_diff']) + " result " + str(x_distance) )
         return x_distance


      else:
         return 0
         
         
         
   def put_into_one_orig(cur_row, one_orig_matches, compare_row_nums ):    
      temp = {}
      biggest_pixel_count = 0
      original_num = 0
      for orig_pair in cur_row:
         for consec_pixels in orig_pair:
            if 'original_y' in consec_pixels:
               cur_original_y = consec_pixels['original_y']
               cur_original_x = consec_pixels['original_x']
               original_num += 1
                  
            if pixel_count_label in consec_pixels:
            
               if original_num != consec_pixels[matched_orig_num_label]:
                  continue
                     
               if consec_pixels[pixel_count_label] > biggest_pixel_count:
                  present = False
                        
                  # putting into empty one_orig_matches
                  if not one_orig_matches:
                     comp_present = None
                     for comp_matched in compare_row_nums:
                        if consec_pixels[y_label] == comp_matched[y_label] and consec_pixels[x_label] == comp_matched[x_label]:
                           comp_present = True
                     if not comp_present:
                        biggest_pixel_count = consec_pixels[pixel_count_label]
                        temp = {}
                        temp['original_y'] = cur_original_y
                        temp['original_x'] = cur_original_x
                        temp['id_num'] = consec_pixels['id_num']
                        temp[pixel_count_label] = biggest_pixel_count     
                        temp[ matched_orig_num_label] = consec_pixels[ matched_orig_num_label]
                        temp[x_label] = consec_pixels[x_label]
                        temp[y_label] = consec_pixels[y_label]
                        
                  else:

                     for comp_row in one_orig_matches:
                        if consec_pixels['id_num'] == comp_row['id_num']:
                           present = True
                                 
                     comp_present = None
                     for comp_matched in compare_row_nums:
                        if consec_pixels[y_label] == comp_matched[y_label] and consec_pixels[x_label] == comp_matched[x_label]:
                           comp_present = True
                        
                     # this compare consecutive pixels have not already added in one_orig_matches or compare_row_nums
                     if present == False and not comp_present:
                        
                        biggest_pixel_count = consec_pixels[pixel_count_label]
                        temp = {}
                        temp['original_y'] = cur_original_y
                        temp['original_x'] = cur_original_x
                        temp['id_num'] = consec_pixels['id_num']
                        temp[pixel_count_label] = biggest_pixel_count
                        temp[ matched_orig_num_label] = consec_pixels[ matched_orig_num_label]
                        temp[x_label] = consec_pixels[x_label]
                        temp[y_label] = consec_pixels[y_label]
                        
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
            
            
         one_orig_matches.append(temp)           
         return True
         
         
         
         
         
         
         
         

   final_results = 0
   one_orig_matches = []
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
   comp_id_num = 0
   
   for matched_row in matched_rows:
      row_counts += 1
      # this will contain all original consecutive pixels with their pairing compare consecutive pixels
      cur_row = []
    
      original_num = 0
      
                 
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
                  if comp_one_consec_pixels[matched_orig_num_label] == original_num:
                  
                     pixel_count_threshold = comp_one_consec_pixels[pixel_count_label] + 1.5 + round( comp_one_consec_pixels[pixel_count_label] * 0.1 )
                     minus_pixel_count_threshold = comp_one_consec_pixels[pixel_count_label] - 1.5 - round( comp_one_consec_pixels[pixel_count_label] * 0.1 )
   
                     if one_consec_pixels['original_count'] <= pixel_count_threshold and one_consec_pixels['original_count'] >= minus_pixel_count_threshold:
                        comp_id_num += 1
                        temp = {}
                        temp['id_num'] = comp_id_num
                        temp[y_label] = comp_one_consec_pixels[y_label]
                        temp[x_label] = comp_one_consec_pixels[x_label]
                        temp[pixel_count_label] = comp_one_consec_pixels[pixel_count_label]
                        temp[matched_orig_num_label] = comp_one_consec_pixels[matched_orig_num_label]
                        temp[original_total_label] = comp_one_consec_pixels[original_total_label]
                     
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
                  
                     

      # at this point, either current row contains big enough pixel count or there are multiple pairs of small pixel count consecutive pixels
      # now comes the "2. matching by x distance direction."
      
      # x direction is only needed if current row has multiple matching pairs of the same row. this means that there are two or more same matched_y pairs
      
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
         
         comp_y_list = []
      
         for one_pair in cur_row:
            for one_consec_pixels in one_pair:
               if 'original_x' in one_consec_pixels:
                  continue
                  
               if y_label in one_consec_pixels:
                  duplicate = 0

                  duplicate_comp_consec = {}
                  duplicate_comp_consec[x_label] = one_consec_pixels[x_label]
                  duplicate_comp_consec[y_label] = one_consec_pixels[y_label]
               
               for another_consec_pixels in one_pair:
                  if y_label in one_consec_pixels:
                     if duplicate_comp_consec[y_label] == one_consec_pixels[y_label] and duplicate_comp_consec[x_label] == one_consec_pixels[x_label]:
                        duplicate += 1
                        
               if len(cur_row) > duplicate:
                  
                  # from every original pair, we need to get y value of compare consecutive pixels so that we know which compare has the multiple consecutive pixels 
                  # on the same y value
                  comp_y_list.append(one_consec_pixels[y_label])
     
                     
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
                     temp[pixel_count_label] = one_consec_pixels[pixel_count_label]
                     temp['original_x'] = x
                     temp['original_pixel_count'] = count
                     temp[matched_orig_num_label] = one_consec_pixels[matched_orig_num_label]
                     temp[original_total_label] = one_consec_pixels[original_total_label]
                     
                     multiple_comp_consec_pix.append(temp)
                     

         if not multiple_comp_consec_pix:
            # current row has multiple original consecutive pixels but there are no multiple compare consecutive pixels with same y value.
            # because there are no multiple compare consecutive pixels with the same row, each one of the compare consecutive pixels
            # matching only one original consecutive pixels. so evaluation will be only one pixel count.
            
            success = put_into_one_orig(cur_row, one_orig_matches, compare_row_nums )
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
                  temp[pixel_count_label] = another_same_y[pixel_count_label]
                  temp[matched_orig_num_label] = another_same_y[matched_orig_num_label]
                  
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
                     
                     if multiple_consec_comp_in_row[y_label] == comp_consec_pix[y_label] and multiple_consec_comp_in_row[x_label] == comp_consec_pix[x_label]:
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
         success = put_into_one_orig(cur_row, one_orig_matches, compare_row_nums )
         if success:
            matched_row_counts += 1
            

   one_orig_matches = sorted( one_orig_matches, key=lambda item: item['original_y'] )   

   same_direction_total = None
   same_row_total = None
   
   if empty_flag:
      same_direction_total, same_row_total = evaluate_1_orig_matches(one_orig_matches, "row", True)
   else:
      same_direction_total, same_row_total = evaluate_1_orig_matches(one_orig_matches, "row", False)
   
   final_results = 0
   
   if same_direction_total:
      final_results += same_direction_total
   if same_row_total:
      final_results += same_row_total

   print("same_direction_total " + str(same_direction_total) + " same_row_total " + str(same_row_total) )
   

   # removing duplicates
   original_row_nums = list( dict.fromkeys(original_row_nums) )

   
   #print(" x_distance " + str(x_distance) )

   unmatched_row_counts = row_counts - matched_row_counts
   final_results += (matched_row_counts * 1.5) - (unmatched_row_counts * 1.5)
   final_results += x_distance   
   
   print(" matched and unmatched rows results " + str( (matched_row_counts * 1.5) - (unmatched_row_counts * 1.5) ) )
   
   print(" real pixel horizontal final results " + str(final_results) )
   
   return final_results






def process_real_p_rows( comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids ):

   comparison_result = sorted( comparison_result , key=lambda item: ( item[0]['original_y'],item[0]['original_x'] )  )


   if original_shape_height >= compare_shape_height:
      rows_needed = math.floor( compare_shape_height / 3)
   else:
      rows_needed = math.floor( original_shape_height / 3)

   if rows_needed < 3:
      return None


   p_real_p_result = process_real_p_rows_matches(comparison_result, False)
   p_empty_p_result = process_real_p_rows_matches(empty_comparison_result, True)
   
   final_results = 0
   if p_real_p_result:
      final_results += p_real_p_result
   if p_empty_p_result:
      final_results += p_empty_p_result
      
   return final_results
   






def process_real_p_virtical_matches(matched_columns, empty_flag):


   if empty_flag:
      x_label = 'empty_matched_x'
      y_label = 'empty_matched_y'
      pixel_count_label = 'empty_pixel_count'
      original_total_label = 'empty_original_totals'
      matched_orig_num_label = 'empty_matched_original_num'
   else:
      x_label = 'matched_x'
      y_label = 'matched_y'
      pixel_count_label = 'matched_pixel_count'
      original_total_label = 'matched_original_totals'
      matched_orig_num_label = 'matched_original_num'      



   def calculate_y_distances(multiple_consec_comp_in_column, comp_consec_pix):

      temp = {}
      temp['id_num'] = comp_consec_pix['id_num']
      temp['id_num2'] = multiple_consec_comp_in_column['id_num']
                  
               
      # checking direction of matched original y
      if multiple_consec_comp_in_column[matched_orig_num_label] < comp_consec_pix[matched_orig_num_label]:
                     
         if comp_consec_pix[y_label] - multiple_consec_comp_in_column[y_label] > 0:
            temp['y_direction'] = True
                        
            comp_y_distance = abs( comp_consec_pix[y_label] - multiple_consec_comp_in_column[y_label] )
            orig_y_distance = comp_consec_pix['original_y'] - multiple_consec_comp_in_column['original_y']
            y_distance_diff = abs( comp_y_distance - orig_y_distance )
                        
            temp['y_distance_diff'] = y_distance_diff
            temp[pixel_count_label + str(comp_consec_pix['id_num'])] = comp_consec_pix[pixel_count_label]
            temp[pixel_count_label + str(multiple_consec_comp_in_column['id_num']) ] = multiple_consec_comp_in_column[pixel_count_label]
         
         else:
            temp['y_direction'] = False
         
      else:
                     
         if multiple_consec_comp_in_column[y_label] - comp_consec_pix[y_label] > 0:
            temp['y_direction'] = True
                        
            comp_y_distance = abs( multiple_consec_comp_in_column[y_label] - comp_consec_pix[y_label] )
            orig_y_distance = multiple_consec_comp_in_column['original_y'] - comp_consec_pix['original_y']
            y_distance_diff = abs( comp_y_distance - orig_y_distance )
                   
            temp['y_distance_diff'] = y_distance_diff                   
            temp[pixel_count_label + str(comp_consec_pix['id_num'])] = comp_consec_pix[pixel_count_label]
            temp[pixel_count_label + str(multiple_consec_comp_in_column['id_num'])] = multiple_consec_comp_in_column[pixel_count_label]                        
                        
         else:
            temp['y_direction'] = False     

      if temp['y_direction'] != False:
          
         comp_count = ( temp[pixel_count_label + str(comp_consec_pix['id_num'])] + temp[pixel_count_label + str(multiple_consec_comp_in_column['id_num'])] ) * 4
         y_distance = comp_count - ( temp['y_distance_diff'] * 2 )
         
         print("y_distance")
         print( " id_num " + str(temp['id_num']) + " id_num2 " + str(temp['id_num2']) + " id_num pixel count " + str(temp[pixel_count_label + str(comp_consec_pix['id_num'])] ) + " id_num2 pixel count " + str(temp[pixel_count_label + str(multiple_consec_comp_in_column['id_num'])] ) + " y_distance_diff " + str(temp['y_distance_diff']) + " result " + str(y_distance) )
         return y_distance


      else:
         return 0
         
         
         
   def put_into_one_orig(cur_column, one_orig_matches, compare_column_nums ):    
      temp = {}
      biggest_pixel_count = 0
      original_num = 0
      for orig_pair in cur_column:
         for consec_pixels in orig_pair:
            if 'original_x' in consec_pixels:
               cur_original_x = consec_pixels['original_x']
               cur_original_y = consec_pixels['original_y']
               original_num += 1
                  
            if pixel_count_label in consec_pixels:
            
               if original_num != consec_pixels[matched_orig_num_label]:
                  continue
                     
               if consec_pixels[pixel_count_label] > biggest_pixel_count:
                  present = False
                        
                  # putting into empty one_orig_matches
                  if not one_orig_matches:
                     comp_present = None
                     for comp_matched in compare_column_nums:
                        if consec_pixels[x_label] == comp_matched[x_label] and consec_pixels[y_label] == comp_matched[y_label]:
                           comp_present = True
                     if not comp_present:
                        biggest_pixel_count = consec_pixels[pixel_count_label]
                        temp = {}
                        temp['original_x'] = cur_original_x
                        temp['original_y'] = cur_original_y
                        temp['id_num'] = consec_pixels['id_num']
                        temp[pixel_count_label] = biggest_pixel_count
                        temp[ matched_orig_num_label ] = consec_pixels[matched_orig_num_label]
                        temp[x_label] = consec_pixels[x_label]
                         
                  else:

                     for comp_column in one_orig_matches:
                        if consec_pixels['id_num'] == comp_column['id_num']:
                           present = True
                                 
                     comp_present = None
                     for comp_matched in compare_column_nums:

                        if consec_pixels[x_label] == comp_matched[x_label] and consec_pixels[y_label] == comp_matched[y_label]:
                           comp_present = True
                        
                     # this compare consecutive pixels have not already added in one_orig_matches or compare_column_nums
                     if present == False and not comp_present:
                        
                        biggest_pixel_count = consec_pixels[pixel_count_label]
                        temp = {}
                        temp['original_y'] = cur_original_y
                        temp['original_x'] = cur_original_x
                        temp['id_num'] = consec_pixels['id_num']
                        temp[pixel_count_label] = biggest_pixel_count
                        temp[ matched_orig_num_label ] = consec_pixels[matched_orig_num_label]
                        temp[x_label] = consec_pixels[x_label]
         
      if temp:
         
         for one_pair in cur_column:
            inner_temp = {}  
            for one_consec_pixels in one_pair:

               if 'original_x' in one_consec_pixels:
             
                  original_column_nums.append( one_consec_pixels['original_x'])
                  inner_temp['original_x'] = one_consec_pixels['original_x']

               if 'id_num' in one_consec_pixels:
                  if temp['id_num'] == one_consec_pixels['id_num']:

                     inner_temp[y_label] = one_consec_pixels[y_label]
                     inner_temp[x_label] = one_consec_pixels[x_label]
                                                      
                     compare_column_nums.append( inner_temp )
            
            
         one_orig_matches.append(temp)           
         return True
         
         
   # ---------------------------                  end of put_into_one_orig                  ---------------------------        
         
               
         

   final_results = 0
   one_orig_matches = []
   y_distance = 0
   matched_column_counts = 0
   column_counts = 0
   
   # this stores all matched original column numbers
   original_column_nums = []
   
   # this stores all matched compare column numbers. Once matched, it can not match another original column.
   compare_column_nums = []

   # this is used for checking consecutiveness of of original and matched compare columns. if original column 150 matched with compare 160.
   # for this to be consecutive, original column needs to be 151 and its matched compare 171. Any other column that is not next to it does not make it a consecutive match.
   consecutive_column_matches = []
   
   comp_id_num = 0
   for matched_column in matched_columns:
      column_counts += 1
      # this will contain all original consecutive pixels with their pairing compare consecutive pixels
      cur_column = []
    
      original_num = 0
      
                 
      # first need to match with every original and compare consecutive pixels based on pixel count threshold
      for one_consec_pixels in matched_column:

         if 'original_x' in one_consec_pixels:
         
            cur_original = []
            original_num += 1
            
            temp = {}
            temp['original_y'] = one_consec_pixels['original_y']
            temp['original_x'] = one_consec_pixels['original_x']
            temp['original_count'] = one_consec_pixels['original_count']
            
            cur_original.append(temp)
            
            
            
   
            # this is for getting compare consecutive pixels for comparing with current original consecutive pixels
            for comp_one_consec_pixels in matched_column:
               
               # make sure to add only matched compare consecutive pixels to its original
               if x_label in comp_one_consec_pixels:
                  if comp_one_consec_pixels[matched_orig_num_label] == original_num:
                  
                     pixel_count_threshold = comp_one_consec_pixels[pixel_count_label] + 1.5 + round( comp_one_consec_pixels[pixel_count_label] * 0.1 )
                     minus_pixel_count_threshold = comp_one_consec_pixels[pixel_count_label] - 1.5 - round( comp_one_consec_pixels[pixel_count_label] * 0.1 )
   
                     if one_consec_pixels['original_count'] <= pixel_count_threshold and one_consec_pixels['original_count'] >= minus_pixel_count_threshold:
                        comp_id_num += 1
                        temp = {}
                        temp['id_num'] = comp_id_num
                        temp[y_label] = comp_one_consec_pixels[y_label]
                        temp[x_label] = comp_one_consec_pixels[x_label]
                        temp[pixel_count_label] = comp_one_consec_pixels[pixel_count_label]
                        temp[matched_orig_num_label] = comp_one_consec_pixels[matched_orig_num_label]
                        temp[original_total_label] = comp_one_consec_pixels[original_total_label]
                     
                        cur_original.append(temp)
                  
            # one original consecutive pixels of current column has finished putting all its matching compare consecutive pixels into cur_original
            cur_column.append(cur_original)
            
      #print("cur_column")
      #print(cur_column)
      # now cur_column contains all original consecutive pixels with their matching compare consecutive pixels
      # 1. matching by pixel count threshold is done at this point.
      
      # check if there is big enough pixel counts in every matching pairs in current column
      p_c_big_enough_threshold = 4
      pixel_count_big_enough = False
      for one_pair in cur_column:
         for one_consec_pixels in one_pair:
         
            if 'original_count' in one_consec_pixels:
            
               if one_consec_pixels['original_count'] >= p_c_big_enough_threshold:
                  pixel_count_big_enough = True
                  

                     

      # at this point, either current column contains big enough pixel count.
      # now comes the "2. matching by y distance direction."
      
      # y direction is only needed if current column has multiple matching pairs of the same column. this means that there are two or more same matched_x pairs
      
      check_pair = 0
      # check if current column matches contain more than 1 original consecutive pixels and their pairs.
      if len(cur_column) > 1:
         for one_pair in cur_column:
            for one_consec_pixels in one_pair:
              
              # check if current pair contains its pairing compare consecutive pixels
              if x_label in one_consec_pixels:
                 check_pair += 1
                 
                 # current pair contains its pairing compare consecutive pixels. break to move to check next pair
                 break
      
      
      if check_pair > 1:
      
         # for storing all x values of non duplicate compare consecutive pixels matching more than 1 original consecutive pixels on the same column.
         # for example. compare x 81, y 80. matching original x 60, y 61. compare x 81, y 80 matching original x 60 y 71. total original number is 2. skip.
         # compare x 70, y 65 matching original x 50 y 100. compare x 70, y 69 matching original x 50 y 110. total original number is 2. add.
         # compare x 70, y 64 matching original x 50 y 100. compare x 71, y 64 matching original x 50 y 110. total original number is 2. add compare x70 and x71
         # but they won't be included in multiple_comp_consec_pix because there is only one compare consecutive on the same column.
         comp_x_list = []
      
         
         for one_pair in cur_column:
            for one_consec_pixels in one_pair:
               if 'original_x' in one_consec_pixels:
                  continue
                  
               if x_label in one_consec_pixels:
                  duplicate = 0
                  # same compare consecutive pixels matching all of original consecutive pixels on the same column. 
                  duplicate_comp_consec = {}
                  duplicate_comp_consec[x_label] = one_consec_pixels[x_label]
                  duplicate_comp_consec[y_label] = one_consec_pixels[y_label]          
             
               for another_consec_pixels in one_pair:
                  
                  if x_label in one_consec_pixels:
                     if duplicate_comp_consec[x_label] == one_consec_pixels[x_label] and duplicate_comp_consec[y_label] == one_consec_pixels[y_label]:
                        duplicate += 1

               # one is itself. duplicate is less than the number of original consecutive pixels. 
               # if there are two original consecutive pixels, and duplicate is two, then skip.
               # if there are three original consecutive pixels, and duplicate is two, then add it as multiple consecutive pixels match.
               if len(cur_column) > duplicate:
                  comp_x_list.append(one_consec_pixels[x_label])
    
                     
         # at this point comp_x_list contains all x values of the current original column. now we need to get multiple x values only.
         temp = []
         multiple_comp = []
         for i in comp_x_list:
            if i not in temp:
               temp.append(i)
            else:
               # adding duplicate x values
               multiple_comp.append(i)
            
         
         # multiple_comp contains multiple compare consecutive pixels.
         # now we need to fill their data
         multiple_comp_consec_pix = []
         for one_pair in cur_column:
            for one_consec_pixels in one_pair:
            
               if 'original_y' in one_consec_pixels:
                  y = one_consec_pixels['original_y']
                  count = one_consec_pixels['original_count']
            
               if x_label in one_consec_pixels:
                  if  one_consec_pixels[x_label] in multiple_comp:
                     # current compare consecutive pixels contain multiple consecutive pixels on the same x value
                     
                     temp = {}
                     temp['id_num'] = one_consec_pixels['id_num']
                     temp[y_label] = one_consec_pixels[y_label]
                     temp[x_label] = one_consec_pixels[x_label]
                     temp[pixel_count_label] = one_consec_pixels[pixel_count_label]
                     temp['original_y'] = y
                     temp['original_pixel_count'] = count
                     temp[matched_orig_num_label] = one_consec_pixels[matched_orig_num_label]
                     temp[original_total_label] = one_consec_pixels[original_total_label]
                     
                     multiple_comp_consec_pix.append(temp)
                     

         if not multiple_comp_consec_pix:
            # current column has multiple original consecutive pixels but there are no multiple compare consecutive pixels with same x value.
            # because there are no multiple compare consecutive pixels with the same column, each one of the compare consecutive pixels
            # matching only one original consecutive pixels. evalution of this then will be one compare consecutive pixels with one original 
            # consecutive pixels
            success = put_into_one_orig(cur_column, one_orig_matches, compare_column_nums )
            if success:
               matched_column_counts += 1
         
         
         x_done = []
         for same_x in multiple_comp_consec_pix:
            
            # make sure y_distance is cotained in only one compare consecutive pixels for each column.
            if same_x[x_label] in x_done:
               continue
            
            compare_y_distace = []
            # if there is one in the multiple_comp, there are two in the multiple_comp_consec_pix but one is itself.
            cur_same_x_count = multiple_comp.count( same_x[x_label] ) 
            
            for another_same_x in multiple_comp_consec_pix:
               # make sure it is not itself and comparing with other compare consecutive pixels
               if same_x != another_same_x and same_x[x_label] == another_same_x[x_label]:
                  cur_same_x_count -= 1
                  
                  temp = {}
                  temp['id_num'] = another_same_x['id_num']
                  temp[y_label] = another_same_x[y_label]
                  temp[x_label] = another_same_x[x_label]
                  temp['original_y'] = another_same_x['original_y']
                  temp['original_pixel_count'] = another_same_x['original_pixel_count']
                  temp[pixel_count_label] = another_same_x[pixel_count_label]
                  temp[matched_orig_num_label] = another_same_x[matched_orig_num_label]
                  
                  compare_y_distace.append(temp)
                  
                  if cur_same_x_count == 0:
                     
                     temp = {'y_distance': compare_y_distace }
                     same_x.update( temp )
                     
                     x_done.append( same_x[x_label] )


         #print("multiple_comp_consec_pix")
         #print(multiple_comp_consec_pix)
         
         temp = 0
         temp_compare_consec_pix = {}
         for multiple_consec_comp_in_column in multiple_comp_consec_pix:
            if 'y_distance' in multiple_consec_comp_in_column:
               # all compare consecutive pixels of each column are contained in the same dictionary as the one with 'y_distance'

               
               for comp_consec_pix in multiple_consec_comp_in_column['y_distance']:
                  comp_present = None
                  for comp_matched in compare_column_nums:
                     if multiple_consec_comp_in_column[x_label] == comp_matched[x_label] and multiple_consec_comp_in_column[y_label] == comp_matched[y_label]:
                        comp_present = True
                  
                     if comp_consec_pix[x_label] == comp_matched[x_label] and comp_consec_pix[y_label] == comp_matched[y_label]:
                        comp_present = True
                        
                     if multiple_consec_comp_in_column[x_label] == comp_consec_pix[x_label] and multiple_consec_comp_in_column[y_label] == comp_consec_pix[y_label]:
                        # make sure it is not comparing with itself
                        comp_present = True
                     
                  if not comp_present:
                     # both of the current multiple_consec_comp_in_column and comp_consec_pix have not matched yet.
                     cur_temp = calculate_y_distances(multiple_consec_comp_in_column, comp_consec_pix)
                  
                     if cur_temp > temp:
                        temp_compare_consec_pix[y_label] = multiple_consec_comp_in_column[y_label]
                        temp_compare_consec_pix[x_label] = multiple_consec_comp_in_column[x_label]
                        temp_compare_consec_pix['another_y'] = comp_consec_pix[y_label]
                        temp = cur_temp
                  
                  # now for comparing compare consecutive pixels with each other inside y_distance list
                  for another_comp_consec_pix in multiple_consec_comp_in_column['y_distance']:                   
                  
                     comp_present = None
                     for comp_matched in compare_column_nums:
                        if comp_consec_pix[x_label] == comp_matched[x_label] and comp_consec_pix[y_label] == comp_matched[y_label]:
                           comp_present = True
                  
                        if another_comp_consec_pix[x_label] == comp_matched[x_label] and another_comp_consec_pix[y_label] == comp_matched[y_label]:
                           comp_present = True
                           
                           
                     if not comp_present:
                           
                        cur_temp = calculate_y_distances(comp_consec_pix, another_comp_consec_pix)
                     
                        if cur_temp > temp:
                           temp_compare_consec_pix[y_label] = comp_consec_pix[y_label]
                           temp_compare_consec_pix[x_label] = comp_consec_pix[x_label]
                           temp_compare_consec_pix['another_y'] = another_comp_consec_pix[y_label]
                           temp = cur_temp                  

         if temp:
            matched_column_counts += 1
            original_x = None
            for one_pair in cur_column:
               for one_consec_pixels in one_pair:
                  if 'original_x' in one_consec_pixels:
                     original_column_nums.append( one_consec_pixels['original_x'])
                     original_x = one_consec_pixels['original_x']

            inner_temp = {}
            inner_temp[y_label] = temp_compare_consec_pix[y_label]
            inner_temp[x_label] = temp_compare_consec_pix[x_label]
            inner_temp['original_x'] = original_x
                                                      
            compare_column_nums.append( inner_temp )
            
            inner_temp = {}
            inner_temp[x_label] = temp_compare_consec_pix[x_label]
            inner_temp[y_label] = temp_compare_consec_pix['another_y']
            inner_temp['original_x'] = original_x
                                                      
            compare_column_nums.append( inner_temp )            

            y_distance += temp
      else:
         # current column has only one filled pair. either current column has multile pairs but only one pair has its matching compare consecutive pixels or 
         # there is only one pair and it is filled.
         # because there is only one matching pair, evaluation of this will be the same as when multiple_comp_consec_pix was empty above.

         success = put_into_one_orig(cur_column, one_orig_matches, compare_column_nums )
         if success:
            matched_column_counts += 1


         
   
   one_orig_matches = sorted( one_orig_matches , key=lambda item: item['original_x'] )
   

   same_direction_total = None
   same_column_total = None
   
   if empty_flag:
      same_direction_total, same_column_total = evaluate_1_orig_matches(one_orig_matches, "column", True)
   else:
      same_direction_total , same_column_total = evaluate_1_orig_matches(one_orig_matches, "column", False)

   final_results = 0
   if same_direction_total:
      final_results += same_direction_total
   if same_column_total:
      final_results += same_column_total

   # removing duplicates
   original_column_nums = list( dict.fromkeys(original_column_nums) )

   unmatched_column_counts = column_counts - matched_column_counts
   
   final_results += (matched_column_counts * 1.5) - (unmatched_column_counts * 1.5)
   final_results += y_distance    
   print("virtical real pixel final_results " + str(final_results) )
   
   return final_results






def process_real_p_virtically(comparison_result, empty_comparison_result, original_shape_width, compare_shape_width, shape_ids):

   comparison_result = sorted( comparison_result , key=lambda item: ( item[0]['original_x'],item[0]['original_y'] )  )


   if original_shape_width >= compare_shape_width:
      columns_needed = math.floor( compare_shape_width / 3)
   else:
      columns_needed = math.floor( original_shape_width / 3)

   if columns_needed < 3:
      return None


   p_real_p_result = process_real_p_virtical_matches(comparison_result, False)
   p_empty_p_result = process_real_p_virtical_matches(empty_comparison_result, True)
   
   final_results = 0
   
   if p_real_p_result:
      final_results += p_real_p_result
   if p_empty_p_result:
      final_results += p_empty_p_result

   return final_results
   







def process_virtically(original_pixels_dict, compare_pixels_dict, shape_ids ):


   def compare_orig_comp_row(cur_original_column, cur_compare_column, matched_columns, empty_flag):

      if empty_flag:
         x_label = 'empty_matched_x'
         y_label = 'empty_matched_y'
         pixel_count_label = 'empty_pixel_count'
         original_total_label = 'empty_original_totals'
         matched_orig_num_label = 'empty_matched_original_num'
      else:
         x_label = 'matched_x'
         y_label = 'matched_y'
         pixel_count_label = 'matched_pixel_count'
         original_total_label = 'matched_original_totals'
         matched_orig_num_label = 'matched_original_num'      

              
      for i_compare in range(len(cur_compare_column)):
                        
         for i_original in range( len(cur_original_column) ):
          
            # here, each one of consecutive pixels of compare shape compares with every one of consecutive pixels of original one.
                        
            pixel_count_threshold = cur_compare_column[i_compare].get('count') + 1.5 + round( cur_compare_column[i_compare].get('count') * 0.1 )
            minus_pixel_count_threshold = cur_compare_column[i_compare].get('count') - 1.5 - round( cur_compare_column[i_compare].get('count') * 0.1 )
                          
            if cur_original_column[i_original].get('original_count') <= pixel_count_threshold and cur_original_column[i_original].get('original_count') >= minus_pixel_count_threshold:
                              
               temp = {}
               temp[x_label] = cur_compare_column[i_compare].get('start_x')
               temp[y_label] = cur_compare_column[i_compare].get('start_y')                           
               temp[pixel_count_label] = cur_compare_column[i_compare].get('count')
               temp[original_total_label] = len(cur_original_column)
               # which original consecutive pixels matched. not how many original consecutive pixels matched but which position of it.
               temp[matched_orig_num_label] = i_original + 1
                                 
               matched_columns.append(temp)
            
   #-----------------------------                  end of compare_orig_comp_row              ----------------------------------


   def compare_w_shape(compare_pixels_dict, search_until, original_count_from_left, original_pixels_in_current_x, original_empty_pixels_in_current_x, shape_ids):

      compare_smallest_x = min(int(d['x']) for d in compare_pixels_dict.values())
      compare_largest_x = max(int(d['x']) for d in compare_pixels_dict.values())

   
      comparison_result = []
      comparison_empty_result = []
      
   
      search_until += original_count_from_left


      #  for y in range(start, stop) stop value is excluded
      for x in range(compare_smallest_x, compare_largest_x + 1):
   

         if search_until == 0:

            return comparison_result, comparison_empty_result
         
    
         # pixel_ids_with_current_x contains all xy coordinate pairs that have the current running y value.
         pixel_ids_with_current_x = [k for k in compare_pixels_dict  if (int(compare_pixels_dict[k]['x'])) == x]
      
      
         # we first obtain all x values for the current running y value
         y_values_list_in_current_x = []
      
      
         # key is the coordinate pair id.  
         for key in pixel_ids_with_current_x:
            # putting all x values for all xy coordinates that have current running y vaule
            y_values_list_in_current_x.append(compare_pixels_dict[key]['y'])

      
         # we need to sort x values so that we can work with neighbor x values
         y_values_list_in_current_x.sort()   
      
      
         pixels_in_current_x = []
         empty_pixels_in_current_x = []
         
         
      
         # this is for getting the largest x value in current running y. largest x value is the last one in current running y because
         # x values are sorted from smallest to largest
         y_counter_in_current_running_x = 1
      
         consecutive_y_counter = 0
      
         y_numbers_in_current_running_x = len(y_values_list_in_current_x)

         first = True

         
         for y_value in y_values_list_in_current_x:
      
            # is this the first x value?
            if first != False:
               consecutive_y_counter +=1

               temp = {}
               temp['start_y'] = y_value
               temp['start_x'] = x


               prev_y_value = y_value 
               first = False     
               # for this row(y), there is only one pixel?
               if y_counter_in_current_running_x == y_numbers_in_current_running_x:

                  temp['count'] =  consecutive_y_counter
                  pixels_in_current_x.append( temp )

                  compare_orig_comp_row(original_pixels_in_current_x, pixels_in_current_x, comparison_result, False)

                  break

               y_counter_in_current_running_x += 1            
               continue
  
            # checking to see if y value is the last one in current running x
            if y_counter_in_current_running_x == y_numbers_in_current_running_x:


               # if current y value is next to the previous y value, y_value - 1 should equal prev_y_value. if there is any
               # empty pixels, y_value - 1 will be greater than prev_y_value
               if y_value - 1 > prev_y_value:
               
                  # this is for previous pixels
                  temp['count'] =  consecutive_y_counter
                  pixels_in_current_x.append( temp )

                  # now this is for the current pixel
                  temp = {}
                  temp['start_y'] = y_value
                  temp['start_x'] = x
                  temp['count'] = 1
                  pixels_in_current_x.append( temp )
               

                  empty_temp = {}
                  empty_temp['start_y'] = prev_y_value + 1
                  empty_temp['start_x'] = x
                  empty_temp['count'] = y_value  - ( prev_y_value + 1) 
                  empty_pixels_in_current_x.append( empty_temp )

               else:
                  # current pixel is consecutive pixel with previous pixels
                  # + 1 from "consecutive_y_counter + 1" is for the current pixel
                  temp['count'] = consecutive_y_counter + 1
                  pixels_in_current_x.append( temp )


               # check if there is empty pixels in either one of shapes
               if len(original_empty_pixels_in_current_x) > 0:
                  # column (x) in original shape contains empty pixels
               

                  if len(empty_pixels_in_current_x ) > 0:
                     # column (x) in compare shape also contains empty pixels
                  
                  
                     if len(original_empty_pixels_in_current_x) == 1 and len(empty_pixels_in_current_x) == 1:
                        # both shapes contain only one consecutive emtpy pixels
                      
                        # when there is only one consecutive empty pixels in  current columns (x) of both shapes, there will be exactly two consecutive pixels in both shapes
                        compare_orig_comp_row(original_pixels_in_current_x, pixels_in_current_x, comparison_result, False)
                  
                        compare_orig_comp_row(original_empty_pixels_in_current_x, empty_pixels_in_current_x, comparison_empty_result, True)


                        # comparing current column from original shape and compare shape has finished. go to next compare shape column and compare it with current original column if still left.
                        break

                     if len(original_empty_pixels_in_current_x) > 1 or len(empty_pixels_in_current_x) > 1:
                        # either one of shapes contain more than 1 empty pixels
                     
                        compare_orig_comp_row(original_pixels_in_current_x, pixels_in_current_x, comparison_result, False)
   
                        compare_orig_comp_row(original_empty_pixels_in_current_x, empty_pixels_in_current_x, comparison_empty_result, True)
                            
                                                         
                        break
                        
                  
                  else:
                     # compare shape has no empty pixels
                  
                  
                     if len(original_empty_pixels_in_current_x) == 1:
                        # column (x) in original shape contains only one consecutive empty pixels

                        compare_orig_comp_row(original_pixels_in_current_x, pixels_in_current_x, comparison_result, False)

                        # because compare shape has no empty pixels for comparing, the current original column is automatically unmatched.
                     
               else:
                  # current original column does not have empty pixels

                  if len(empty_pixels_in_current_x ) > 0:
                     # column (x) in compare shape contains empty pixels

                     if len(empty_pixels_in_current_x) == 1:
                        # column (x) in compare shape contains only one consecutive empty pixels
                     
                        compare_orig_comp_row(original_pixels_in_current_x, pixels_in_current_x, comparison_result, False)


                  else:
                     # compare shape has no empty pixels
                     # both shapes have no empty pixels. so there is only one consecutive pixels
                  
                     compare_orig_comp_row(original_pixels_in_current_x, pixels_in_current_x, comparison_result, False)
                                 

               # go to next compare shape row
               break
            
            else:
         
               # if two consecutive pixels are right next to each other, the difference of them should produce 1
               if abs( y_value - prev_y_value ) > 1:
                  # boundary is found

                  if y_value - prev_y_value < 0:
                   
                     print("this should never be printed")
                   
                

                  else:

                     # empty pixel found. empty pixel starts from previous_y_value + 1 and ends at y_value - 1.
                   
                     # consecutive shape pixels ended at previous_y_value.

                     temp['count'] =  consecutive_y_counter
                     pixels_in_current_x.append( temp )  
                  

                     empty_temp = {}
                     empty_temp['start_y'] = prev_y_value + 1
                     empty_temp['start_x'] = x
                     empty_temp['count'] = y_value  - ( prev_y_value + 1) 
                     empty_pixels_in_current_x.append( empty_temp )

                     # after boundary is found, consecutive shape pixel starts at current x_value. Also this pixel is not the last pixel, so don't call compare_w_shape
                     consecutive_y_counter = 1
                  
                     temp = {}
                     temp['start_y'] = y_value
                     temp['start_x'] = x


               else:
                  # current x value is right next to previous pixel and also it is not the last pixel in the current column (x)
                  consecutive_y_counter +=1
                
  
            prev_y_value = y_value               

            y_counter_in_current_running_x += 1
         
         
         # after looping through all comparing shape's y values in current column (x)
         search_until -= 1

         if x == compare_largest_x:

            return comparison_result, comparison_empty_result

   #--------------------------------------                       end of compare_w_shape                       ----------------------------------------



   original_smallest_x = min(int(d['x']) for d in original_pixels_dict.values())
   original_largest_x = max(int(d['x']) for d in original_pixels_dict.values())

   original_shape_width = original_largest_x - original_smallest_x
   
   compare_smallest_x = min(int(d['x']) for d in compare_pixels_dict.values())
   compare_largest_x = max(int(d['x']) for d in compare_pixels_dict.values())
   
   compare_shape_width = compare_largest_x - compare_smallest_x

   # same as row processing
   search_until = abs( original_shape_width - compare_shape_width ) + 1

   
   # this list will have matched rows from both shapes. matched rows will be pairs. Pair consists of one row from original shape and another row from compare shape
   comparison_result = []
   empty_comparison_result = []


   #  for x in range(start, stop) stop value is excluded
   for x in range(original_smallest_x, original_largest_x + 1):
   
   
      # pixel_ids_with_current_x contains all xy coordinate pairs that have the current running x value.
      pixel_ids_with_current_x = [k for k in original_pixels_dict  if (int(original_pixels_dict[k]['x'])) == x]
      
      
      # we first obtain all y values for the current running x value
      y_values_list_in_current_x = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_x:
         # putting all y values for all xy coordinates that have current running x vaule
         y_values_list_in_current_x.append(original_pixels_dict[key]['y'])

      
      # we need to sort y values so that we can work with neighbor y values
      y_values_list_in_current_x.sort()
      
      
      pixels_in_current_x = []
      empty_pixels_in_current_x = []
         
         
      
      # this is for getting the largest y value in current running x. largest y value is the last one in current running x because
      # y values are sorted from smallest to largest
      y_counter_in_current_running_x = 1
      
      consecutive_y_counter = 0
      
      y_numbers_in_current_running_x = len(y_values_list_in_current_x)

      first = True
      
         
      for y_value in y_values_list_in_current_x:
      
         matched_x_in_compare_shape = {}

         # is this the first x value?
         if first != False:
            consecutive_y_counter +=1

            temp = {}
            temp['original_y'] = y_value
            temp['original_x'] = x


            prev_y_value = y_value 
            first = False     
            # for this column(x), there is only one pixel?
            if y_counter_in_current_running_x == y_numbers_in_current_running_x:

               temp['original_count'] =  consecutive_y_counter
               pixels_in_current_x.append( temp )


               matched_x_in_compare_shape, empty_matched_x_in_compare_shape = compare_w_shape(compare_pixels_dict, search_until, x - original_smallest_x, pixels_in_current_x, empty_pixels_in_current_x, shape_ids )
               
               # return result of one pixel row, so this will not contain empty pixels
          
               # add current rows of original shape and compare shape only when match is found
               if matched_x_in_compare_shape:

                  # merging row from original and compare shapes
                  original_compare_pixels = pixels_in_current_x + matched_x_in_compare_shape

            
                  comparison_result.append(original_compare_pixels)


               break

            y_counter_in_current_running_x += 1            
            continue
  
         # checking to see if y value is the last one in current running x
         if y_counter_in_current_running_x == y_numbers_in_current_running_x:


            if y_value - 1 > prev_y_value:
               
               # this is for the previous pixels
               temp['original_count'] =  consecutive_y_counter
               pixels_in_current_x.append( temp )
               
               # now this is for the current pixel
               temp = {}
               temp['original_y'] = y_value
               temp['original_x'] = x
               temp['original_count'] = 1
               pixels_in_current_x.append(temp)

               empty_temp = {}
               empty_temp['original_y'] = prev_y_value + 1
               empty_temp['original_x'] = x
               empty_temp['original_count'] = y_value  - ( prev_y_value + 1) 
               empty_pixels_in_current_x.append( empty_temp )

            else:
               # current pixel is consecutive pixel with previous pixels
               # + 1 from "consecutive_y_counter + 1" is for the current pixel
               temp['original_count'] =  consecutive_y_counter + 1
               pixels_in_current_x.append( temp )

            
            matched_x_in_compare_shape, empty_matched_x_in_compare_shape = compare_w_shape(compare_pixels_dict, search_until, x - original_smallest_x, pixels_in_current_x, empty_pixels_in_current_x, shape_ids)

            # add current rows of original shape and compare shape only when match is found
            if matched_x_in_compare_shape:

               # merging row from original and compare shapes
               original_compare_pixels = pixels_in_current_x + matched_x_in_compare_shape

            
               comparison_result.append(original_compare_pixels)
            
            # add current rows of original shape and compare shape only when match is found
            if empty_matched_x_in_compare_shape:
               # merging row from original and compare shapes            
               empty_original_compare_pixels = empty_pixels_in_current_x + empty_matched_x_in_compare_shape

               empty_comparison_result.append(empty_original_compare_pixels)
               
            
            break
            
         else:
         
            # if two consecutive pixels are right next to each other, the difference of them should produce 1
            if abs( y_value - prev_y_value ) > 1:
               # boundary is found

               if y_value - prev_y_value < 0:
                   
                  print("this should never be printed")
                   
                

               else:

                  # empty pixel found. empty pixel starts from previous_y_value + 1 and ends at y_value - 1.
                   
                  # consecutive shape pixels ended at previous_x_value.

                  # this count is for previous pixels
                  temp['original_count'] =  consecutive_y_counter
                  pixels_in_current_x.append( temp )  
                  

                  empty_temp = {}
                  empty_temp['original_y'] = prev_y_value + 1
                  empty_temp['original_x'] = x
                  empty_temp['original_count'] = y_value  - ( prev_y_value + 1) 
                  empty_pixels_in_current_x.append( empty_temp )

                  # after boundary is found, consecutive shape pixel starts at current x_value. Also this pixel is not the last pixel, so don't call compare_w_shape
                  consecutive_y_counter = 1
                  
                  temp = {}
                  temp['original_y'] = y_value
                  temp['original_x'] = x


            else:
               # current x value is right next to previous pixel and also it is not the last pixel in the current row (y)
               consecutive_y_counter +=1
                
  
         prev_y_value = y_value               

         y_counter_in_current_running_x += 1
         
         
      # after looping through all original x values in current row (y)


      # updating for each row (y) of compare shape
         
         
      #updating for each row (y) of original shape

      
   # check if both shapes are same shapes in different frames of video


   result = process_real_p_virtically(comparison_result, empty_comparison_result, original_shape_width, compare_shape_width, shape_ids)

   return result




# this method compares two shapes from different frames of video and tries to determine if they are both the same 
# same in different frames of video.

#  two parameters in, Both are a dictionary with following form.
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
    
def find_shapes_in_diff_frames(original_pixels_dict, compare_pixels_dict, algorithm, shape_ids):


   def compare_orig_comp_row(cur_original_row, cur_compare_row, matched_rows, empty_flag):

      if empty_flag:
         x_label = 'empty_matched_x'
         y_label = 'empty_matched_y'
         pixel_count_label = 'empty_pixel_count'
         original_total_label = 'empty_original_totals'
         matched_orig_num_label = 'empty_matched_original_num'
      else:
         x_label = 'matched_x'
         y_label = 'matched_y'
         pixel_count_label = 'matched_pixel_count'
         original_total_label = 'matched_original_totals'
         matched_orig_num_label = 'matched_original_num'      

              
      for i_compare in range(len(cur_compare_row)):
                        
         for i_original in range( len(cur_original_row) ):
          
            # here, each one of consecutive pixels of compare shape compares with every one of consecutive pixels of original one.
                        
            pixel_count_threshold = cur_compare_row[i_compare].get('count') + 1.5 + round( cur_compare_row[i_compare].get('count') * 0.1 )
            minus_pixel_count_threshold = cur_compare_row[i_compare].get('count') - 1.5 - round( cur_compare_row[i_compare].get('count') * 0.1 )
                          
            if cur_original_row[i_original].get('original_count') <= pixel_count_threshold and cur_original_row[i_original].get('original_count') >= minus_pixel_count_threshold:
                              
               temp = {}
               temp[x_label] = cur_compare_row[i_compare].get('start_x')
               temp[y_label] = cur_compare_row[i_compare].get('start_y')                           
               temp[pixel_count_label] = cur_compare_row[i_compare].get('count')
               temp[original_total_label] = len(cur_original_row)
               # which original consecutive pixels matched. not how many original consecutive pixels matched but which position of it.
               temp[matched_orig_num_label] = i_original + 1
                                 
               matched_rows.append(temp)
            
   #-----------------------------                  end of compare_orig_comp_row              ----------------------------------


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
         
    
         # pixel_ids_with_current_y contains all xy coordinate pairs that have the current running y value.
         pixel_ids_with_current_y = [k for k in compare_pixels_dict  if (int(compare_pixels_dict[k]['y'])) == y]
      
      
         # we first obtain all x values for the current running y value
         x_values_list_in_current_y = []
      
      
         # key is the coordinate pair id.  
         for key in pixel_ids_with_current_y:
            # putting all x values for all xy coordinates that have current running y vaule
            x_values_list_in_current_y.append(compare_pixels_dict[key]['x'])

      
         # we need to sort x values so that we can work with neighbor x values
         x_values_list_in_current_y.sort()   
      
      
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

         if y == compare_largest_y:

            return comparison_result, comparison_empty_result

   #--------------------------------------                       end of compare_w_shape                       ----------------------------------------




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
   
   
      # pixel_ids_with_current_y contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y = [k for k in original_pixels_dict  if (int(original_pixels_dict[k]['y'])) == y]
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y:
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(original_pixels_dict[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
      
      
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


   if algorithm == "consecutive_count":
      result = process_real_p_rows(comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids)

      # row processing has done, now process virtically
      virtical_resuls = process_virtically(original_pixels_dict, compare_pixels_dict, shape_ids )
      
      final_results = 0
      if result:
         final_results += result
      if virtical_resuls:
         final_results += virtical_resuls

      return final_results
         
         
      
      




















































































































































