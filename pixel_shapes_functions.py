
import re
from PIL import Image
import os
import recreate_shapes
from statistics import mean
import math

# returns all pixel shape ids and all its pixel indexes
# pixel id dictionary[ matched pixel shape id ] = [ pixel index1, pixel index2, ..... ]
def get_all_pixels_of_shapes(shape_ids, image_filename, directory_under_images=""):


    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images.find('/') == -1:
       directory_under_images +='/'

    shapes_file = open("shapes/" + image_filename + "_shapes.txt")
    shapes_file_contents = shapes_file.read()


    original_image = Image.open("images/" + str(directory_under_images) + image_filename + ".png")

    image_width, image_height = original_image.size



    # single pixel shapes
    # ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
    # space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
    # single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'

    single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
    match = re.findall(single_pixel_pattern, shapes_file_contents)


    # shapes_with_indexes[matched shape id ] = [ pixel index1, pixel index2 .... ]
    shapes_with_indexes = {}

    for matched_shape_id in shape_ids: 

        # match contains all image shapes
        for shape in match:


           shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
           match_temp = re.search(shapes_id_pattern, shape)
           shapes_id = match_temp.group().strip('(,')
           
           if str(shapes_id) != str(matched_shape_id):
              continue
              

           shapes_with_indexes[shapes_id] = [int(shapes_id)]



    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
    '''
    multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    match = re.findall(multiple_pixel_pattern, shapes_file_contents)
    
    

    for matched_shape_id in shape_ids: 

        # match contains all image shapes
        for shape in match:


           shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
           match_temp = re.search(shapes_id_pattern, shape)
           shapes_id = match_temp.group().strip('(,')
           
           if str(shapes_id) != str(matched_shape_id):
              continue
              

           pixels_list_pattern = '\[.*\]'
           pixels_index_string = re.findall(pixels_list_pattern, shape)



           #pixel_index_string contains one shape
           # pixels_index_string is a list but contains only one string
           for one_string in pixels_index_string:
          
              # one_string is a one string. removing unnecessary characters leaving only the numbers
              one_string_stripped = one_string.strip('[, ]')
              one_string_stripped = one_string_stripped.replace(' ', '')
              # split each pixel index number by ,
              one_string_list = one_string_stripped.split(',')



           shapes_with_indexes[matched_shape_id] = one_string_list


    return shapes_with_indexes














#  parameter in and out is a dictionary with following form.
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
    
def get_boundary_pixels(pixels_dict):


   pixel_boundaries = {}


   # first, we are going to get boundaries horizontally



   smallest_y = min(int(d['y']) for d in pixels_dict.values())
   largest_y = max(int(d['y']) for d in pixels_dict.values())


   pixel_counter = 1
   
   debug = False



   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(smallest_y, largest_y + 1):

      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in pixels_dict  if (int(pixels_dict[k]['y'])) == y]
      
      first = True
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      '''
      -------------------        boundary finding algorithm            ---------------------------
      
      With current running y value, boundary is where there is no consecutive x values. This means there is no more 
      neighbor x values on the right or left side.  The " boundary left side " has missing x values on the " left " ( no more smaller x values )
      The " boundary right side " has missing x values on the " right " ( missing neighbor larger x values )
      finally, the smallest and largest x values are the farthest of all pixels in the current running y value.
      '''
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y_values:
      
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(pixels_dict[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
      
      # this is for getting the largest x value in current running y. largest x value is the last one in current running y because
      # x values are sorted from smallest to largest
      x_counter_in_current_running_y = 1
      
      x_numbers_in_current_running_y = len(x_values_list_in_current_y)

      for x_value in x_values_list_in_current_y:

         # boundary is also on smallest y and largest y because very top and very bottom will be the boundaries
         # this is for the very top
         if y == smallest_y:
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y                 

    
         # boundary is also on smallest y and largest y because very top and very bottom will be the boundaries
         # this is for the bottom
         if y == largest_y:
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y                 
         
         # checking to see if x value is the last one in current running y
         if x_counter_in_current_running_y == x_numbers_in_current_running_y:
            
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y                


         # smallest x value and largest x value in the current running y value are the farthest boundary pixels
         # x values are sorted, so smallest x value in current running y is the first x value
         if first != False:
         
            pixel_boundaries[pixel_counter] = {}
            pixel_boundaries[pixel_counter]['x'] = x_value
            pixel_boundaries[pixel_counter]['y'] = y            
            
            first = False
            
         else:
         
             # if two consecutive pixels are right next to each other, the difference of them should produce 1
             if abs( x_value - previous_x_value ) > 1:
                # boundary is found

                if x_value - previous_x_value < 0:
                   # result is negative, this means current x value is smaller ( it is on the left relative to previous )
                   # then, current x value is the boundary pixel " on the left side "

                   pixel_boundaries[pixel_counter] = {}
                   pixel_boundaries[pixel_counter]['x'] = x_value
                   pixel_boundaries[pixel_counter]['y'] = y
                

                else:

                   # result is positive, this means current x value is larger than previous ( it is on the right relative 
                   # to previous ). Then, current x value is the boundary pixel " on the right side " relative to previous

                   pixel_boundaries[pixel_counter] = {}
                   pixel_boundaries[pixel_counter]['x'] = x_value
                   pixel_boundaries[pixel_counter]['y'] = y
                
                
                   # because current x value is not consecutive from previous x value, previous x value is also the boundary
                   pixel_counter += 1
                   pixel_boundaries[pixel_counter] = {}
                   pixel_boundaries[pixel_counter]['x'] = previous_x_value
                   pixel_boundaries[pixel_counter]['y'] = y
                
         previous_x_value = x_value               

         pixel_counter += 1
         x_counter_in_current_running_y += 1




   # -----------------------------          now this is for getting boundaries vertically        ----------------------------------------



   smallest_x = min(int(d['x']) for d in pixels_dict.values())
   largest_x = max(int(d['x']) for d in pixels_dict.values())


   # for loop for going from smallest x value to largest x value
   # here, we will look at each one of the columns of pixels from smallest x value to the largest x_counter_in_current_running_y
   # for example, we will look at all pixels that lie in ( 0, all y values ), ( 1, all y values ) ..... 
   #  for x in range(start, stop) stop value is excluded
   for x in range(smallest_x, largest_x + 1):

      # pixel_ids_with_current_x_values contains all xy coordinate pairs that have the current running x value.
      pixel_ids_with_current_x_values = [k for k in pixels_dict  if (int(pixels_dict[k]['x'])) == x]
      
      first = True
      y_counter_in_current_running_x = 1
      
      # we first obtain all y values for the current running x value
      y_values_list_in_current_x = []
      
      
      '''
      -------------------        boundary finding algorithm            ---------------------------
      
      With current running x value, boundary is where there is no consecutive y values. This means there is no more 
      neighbor y values on the top or bottom.  The " boundary top side " has missing y values on the " top " ( no more smaller y values )
      The " boundary bottom side " has missing y values on the " bottom " ( missing neighbor larger y values) 
      '''
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_x_values:
      
         # putting all y values for all xy coordinates that have current running x vaule
         y_values_list_in_current_x.append(pixels_dict[key]['y'])

      
      # we need to sort x values so that we can work with neighbor x values
      y_values_list_in_current_x.sort()
        

      for y_value in y_values_list_in_current_x:
 
         # check if current y value is the last one in the current running x
         if y_counter_in_current_running_x == len(y_values_list_in_current_x):
         

         
            pixel_boundaries[pixel_counter] = {}

            pixel_boundaries[pixel_counter]['x'] = x
            pixel_boundaries[pixel_counter]['y'] = y_value

         
         # for the current running x value (all pixels vertically ), first y is the very top pixel which should be boundary
         if first == True:
         
            pixel_boundaries[pixel_counter] = {}

            pixel_boundaries[pixel_counter]['x'] = x
            pixel_boundaries[pixel_counter]['y'] = y_value 
 
            previous_y_value = y_value
            first = False
         else:          

            # if two consecutive pixels are right next to each other, the difference of them should produce 1
            if abs( y_value - previous_y_value ) > 1:
               # boundary is found
                

               pixel_boundaries[pixel_counter] = {}

               pixel_boundaries[pixel_counter]['x'] = x
               pixel_boundaries[pixel_counter]['y'] = y_value


               # because current y value is not consecutive from previous y value, previous y value is also the boundary
               pixel_counter += 1
               pixel_boundaries[pixel_counter] = {}
               pixel_boundaries[pixel_counter]['x'] = x
               pixel_boundaries[pixel_counter]['y'] = previous_y_value
   
                
         previous_y_value = y_value    

         pixel_counter += 1
         y_counter_in_current_running_x += 1




   return pixel_boundaries








#  parameter in, pixels_dict is a dictionary with following form.
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
    
def create_shapes_stats(pixels_dict, filename, pixel_ids_list):

   '''
   this is to get shape's statistics
   
   statistics are:
   
   all xy values in the below form
   start_x: x, start_y: y, count: count value
   all consecutive pixels excluding empty pixels
   
   empty pixels in the same form as xy values
   start_x:x, start_y:y, count: count value
   
   boundary pixels in the below form
   x:x y:y. x:x y:y. x:x y:y.

   central pixel
   x:x y:y

   central pixel is needed to convert image coordinate xy values to shape's coordinate values. Shape's coordinate values are 
   needed for comparing and finding same shape in different frames of images.   
   
   '''


   if os.path.exists("shapes/shapes_stats/" + filename) == False:
      os.mkdir("shapes/shapes_stats/" + filename)
      

   stats_file = open("shapes/shapes_stats/" + filename + "/" + pixel_ids_list[0] + "_stats.txt", "w" )

   # writin shapes ids.
   stats_file.write("#" + str(pixel_ids_list) )
   stats_file.write("\n\n")


   smallest_y = min(int(d['y']) for d in pixels_dict.values())
   largest_y = max(int(d['y']) for d in pixels_dict.values())

   smallest_x = min(int(d['x']) for d in pixels_dict.values())
   largest_x = max(int(d['x']) for d in pixels_dict.values())
   
   
   stats_file.write("total pixels:" + str( len(pixels_dict) ) + "\n\n")
   stats_file.write("shape origin pixel:\n" + "x:" + str( smallest_x ) + " y:" + str( smallest_y ) + "\n\n")


   
   debug = False



   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(smallest_y, largest_y + 1):
   
      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in pixels_dict  if (int(pixels_dict[k]['y'])) == y]
      
      first = True
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y_values:
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(pixels_dict[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()
      
      # this is for getting the largest x value in current running y. largest x value is the last one in current running y because
      # x values are sorted from smallest to largest
      x_counter_in_current_running_y = 1
      
      consecutive_x_counter = 0
      
      x_numbers_in_current_running_y = len(x_values_list_in_current_y)


      for x_value in x_values_list_in_current_y:
      


         # is this the first x value?
         if first != False:
            consecutive_x_counter +=1
            stats_file.write("shape xy values:\n")
            stats_file.write("start_x:" + str(x_value) + " start_y:" + str(y) )

            previous_x_value = x_value 
            first = False     
            # for this row(y), there is only pixel?
            if x_counter_in_current_running_y == x_numbers_in_current_running_y:
               stats_file.write(" count:" + str(consecutive_x_counter) + "\n" )

               break

            x_counter_in_current_running_y += 1            
            continue
  
         # checking to see if x value is the last one in current running y
         if x_counter_in_current_running_y == x_numbers_in_current_running_y:

            stats_file.write(" count:" + str(consecutive_x_counter + 1) + "\n" )
            
            break
            
         else:
         
             # if two consecutive pixels are right next to each other, the difference of them should produce 1
             if abs( x_value - previous_x_value ) > 1:
                # boundary is found

                if x_value - previous_x_value < 0:
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
                   stats_file.write(" count:" + str(consecutive_x_counter) + "\n" )
                   
                   
                   # writing empty pixels into stats_file
                   stats_file.write("empty pixels:\n" )
                   stats_file.write("start_x:" + str(previous_x_value + 1) + " start_y:" + str(y) + " count:" + str(x_value  - ( previous_x_value + 1) ) + "\n" )
                   
                   
                   # consecutive shape pixel starts at current x_value.
                   consecutive_x_counter = 1
                   stats_file.write("shape xy values:\n")
                   stats_file.write("start_x:" + str(x_value) + " start_y:" + str(y) )


             else:
                # current x value is right next to previous pixel and also it is not the last pixel in the current row (y)
                consecutive_x_counter +=1
                
  
         previous_x_value = x_value               

         x_counter_in_current_running_y += 1
         
      debug=False
      
   stats_file.write("\n")
   stats_file.close()





# called from find_shapes_in_diff_frames
# this method is for comparing and finding same shape in different frames of video.

# I copied code from find_shapes_in_diff_frames for getting pixels in current row (y) so it is horrible
# but I stick with it for now. fix it later when I get time or feel the need.

# return is the result of comparison. return is dictionary with following form
# search_ended, single_pixel_count_match, matched_x, matched_y, matched_pixel_count, empty_matched_x, empty_matched_y
# search_ended is boolean. single_pixel_count_match's value is boolean. matched_x, y, count are values where original pixels matched.

def compare_w_shape(compare_pixels_dict, search_until, original_count_from_top, original_pixels_in_current_y, original_empty_pixels_in_current_y):


   #print("original_pixels_in_current_y")
   #print(original_pixels_in_current_y)

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
            
            
            # check there is empty pixels in either one of shapes
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
                                    
                  
                  if len(original_empty_pixels_in_current_y) > 1 and len(empty_pixels_in_current_y) > 1:
                     # both shapes contain more than 1 consecutive empty pixels
                     

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
                     minus_pixel_count_threshold = pixels_in_current_y[0]['count'] - 2 - round( pixels_in_current_y[0]['count'] * 0.1 )
   
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
   else:
      rows_needed = math.floor( original_shape_height / 3)

   if rows_needed < 3:
      print("can not determine with pixel consecutive row match algorithm")
      return
      
   
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
            

   if row_match_result > rows_needed:
      return row_match_result

















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
   search_until = abs( original_shape_height - compare_shape_height )

   
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


   if algorithm == "boundary":
      return find_boundary_matches(comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids)
   elif algorithm == "consecutive_count":
      return find_consecutive_matches(comparison_result, empty_comparison_result, original_shape_height, compare_shape_height, shape_ids)







'''
def are_boundaries_same_shape( original_boundaries, compare_boundaries ):


   # first sort boudaries values from smallest y to the biggest y.
   original_boundaries = sorted( original_boundaries.items(), key=lambda item: item[1]['y'] )
   compare_boundaries = sorted( compare_boundaries.items(), key=lambda item: item[1]['y'] )


   # removing duplicate xy coordinates
   temp = {}

   for key, value in original_boundaries.items():
      if value not in temp.values():
         temp[key] = value
      
   original_boundaries = temp

   temp = {}

   for key, value in compare_boundaries.items():
      if value not in temp.values():
         temp[key] = value
      

   compare_boundaries = temp


   #matching algorithm

   #start comparing at both of top rows. it could be that one shape has top row number of 15, compare shape can have different number of top row number, like 10 or 5.

   #matching the same row.
   #count every consecutive pixels. starting from leftmost consecutive pixels.

'''



































































# return is boundary_shapes
# boundary_shapes contains boundary shape number, pixel number, xy values
# form is shown below
# boundary shapes[ boundary shape number ][ pixel number ]['x']
# boundary shapes[ boundary shape number ][ pixel number ]['y']

# input parameter -> boundary_pixels. this is the one returned by get_boundary_pixels function
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
def get_boundary_shapes(boundary_pixels):


   def put_neighbor_pixel_in_boundary_shape(comparing_pixel):
   

      nonlocal shape_number   
      nonlocal boundary_shape_counter
      nonlocal boundary_shapes
      nonlocal boundary_pixels



      # current running pixel is not in existing boundary shapes
      if shape_number == None:
     
            boundary_shapes[boundary_shape_counter][comparing_pixel] = { 'x': boundary_pixels[comparing_pixel]['x'] , 'y': boundary_pixels[comparing_pixel]['y'] }

        
      else:
         # current running pixel is found in existing boundary shapes

            boundary_shapes[shape_number][comparing_pixel] = { 'x': boundary_pixels[comparing_pixel]['x'] , 'y': boundary_pixels[comparing_pixel]['y'] }
      


   def process_neighbors(pixel_numbers):
   

      nonlocal boundary_shape_counter
      nonlocal boundary_shapes
      nonlocal boundary_pixels
      nonlocal shape_number


      current_running_pixels_list = []
      
      return_flag = False


      shape_number = None
      
      
      print("current running pixel number is " + str(pixel_numbers) )
      
      


      if not len(pixel_numbers)==0:
          pixel_number = pixel_numbers.pop()
          
      elif not len(boundary_pixels)==0:
          pixel_number = list(boundary_pixels.keys())[0]
          
      else:
          return boundary_shapes



      # finding where in boundary shapes number current pixel resides
      for shape_num, pixels in boundary_shapes.items():

         if pixel_number in pixels.keys():

            shape_number = shape_num         
            print("shape number " + str(shape_number))
            print(" current pixel " + str(pixel_number))

      
      if shape_number == None:

         boundary_shape_counter += 1
         boundary_shapes[boundary_shape_counter] = { pixel_number: {'x': boundary_pixels[pixel_number]['x'], 'y': boundary_pixels[pixel_number]['y'] } }         
         print("boundary shapes ")
         print(boundary_shapes)
      

      # getting current pixel's neighbors
      # left, right neighbor pixes have same y value as the current pixel's y value
      # above pixels , top left, top , top right pixes have y value , " current y value - 1 "
      # below pixels, bottom left, bottom, bottom right pixels have y value, " current y value + 1 "
      all_pixels_left_or_right = [k for k in boundary_pixels  if (int(boundary_pixels[k]['y'])) == boundary_pixels[pixel_number]['y'] ]
       
      # removing current pixel from all_pixels_left_or_right because this should contain comparing pixels and not comparing with itself
      all_pixels_left_or_right.remove(pixel_number)
      
       
      all_above_pixels = [k for k in boundary_pixels  if (int(boundary_pixels[k]['y'])) == boundary_pixels[pixel_number]['y'] - 1 ]
      all_below_pixels = [k for k in boundary_pixels  if (int(boundary_pixels[k]['y'])) == boundary_pixels[pixel_number]['y'] + 1 ]
       
      print("all above pixels " + str(all_above_pixels))
      print("all pixels left or right " + str(all_pixels_left_or_right))
      print("all below pixels " + str(all_below_pixels))   


      found_above_neighbors = []      
      found_left_or_right_neighbors = []
      found_below_neighbors =[]

      # all above pixels contains all pixels that are right above current pixel. We now need to find " above neighbor pixels "
      for pixel in all_above_pixels:
      
         
       
         # top neighbor has  ( current pixel x value , current pixel y value - 1 )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x']:
            # top neighbor found
     
            found_above_neighbors.append(pixel)
               
               

        
         # top left neighbor has  ( current pixel x value - 1 , current pixel y value - 1 )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x'] - 1:

            found_above_neighbors.append(pixel)        
                
       
         # top right neighbor has  ( current pixel x value + 1 , current pixel y value - 1 )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x'] + 1:


            found_above_neighbors.append(pixel) 
       
       
      # all left or right pixels contains all pixels that are on the same y value as current runnning pixel. We now need to find " left or right neighbor pixels "
      for pixel in all_pixels_left_or_right:
        
        
         # left neighbor has  ( current pixel x value - 1 , current pixel y value )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x'] - 1:
         
            found_left_or_right_neighbors.append(pixel)           
        
        
         # right neighbor has  ( current pixel x value + 1 , current pixel y value )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x'] + 1:
            found_left_or_right_neighbors.append(pixel)        
        
        
        
        
      # all below pixels contains all pixels that are right below current pixel. We now need to find " below neighbor pixels "
      for pixel in all_below_pixels:
            
        
         # bottom neighbor has  ( current pixel x value , current pixel y value + 1 )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x']:
            # bottom neighbor found
          
          
            found_below_neighbors.append(pixel)   
        
        
         # bottom left neighbor has  ( current pixel x value - 1 , current pixel y value + 1 )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x'] - 1:
            # bottom left neighbor found
            
        
            found_below_neighbors.append(pixel)               
            
         # bottom right neighbor has  ( current pixel x value - 1 , current pixel y value + 1 )
         if boundary_pixels[pixel]['x'] == boundary_pixels[pixel_number]['x'] + 1:
            # bottom right neighbor found
            
        
            found_below_neighbors.append(pixel)   
       
      
      
      print(" found above neighbors " + str(found_above_neighbors) )
      print(" found left or right neighbors " + str(found_left_or_right_neighbors))
      print(" found below neighbors " + str(found_below_neighbors) )

  
      if not len(found_above_neighbors) == 0:
         for found_above_neighbor in found_above_neighbors:
 
            print(" I am pixel number " + str(pixel_number))
            print(" I am putting this neighbor " + str(found_above_neighbor))
              
            # put all found neighbors in the same boundary shape as current running pixel
            put_neighbor_pixel_in_boundary_shape(found_above_neighbor )


      if not len(found_left_or_right_neighbors) == 0:
         for found_left_or_right_neighbor in found_left_or_right_neighbors:

            print(" I am pixel number " + str(pixel_number))
            print(" I am putting this neighbor " + str(found_left_or_right_neighbor))
     
            put_neighbor_pixel_in_boundary_shape(found_left_or_right_neighbor )     


      if not len(found_below_neighbors) == 0:
         for found_below_neighbor in found_below_neighbors:
         
            print(" I am pixel number " + str(pixel_number))
            print(" I am putting this neighbor " + str(found_below_neighbor))
     
            put_neighbor_pixel_in_boundary_shape(found_below_neighbor )    


      # after putting all found direct neighbors in the same shape as current running pixel, put current running pixel
      # in already process list because current runnin pixel won't have any more neighbors. So putting it in the already process list
      # and deleting it from boundary shapes won't have negative impact on other pixels

      already_processed_pixels.append(pixel_number)    

      # deleting current running pixel from boundary_pixels
      for processed_key in already_processed_pixels:
         if processed_key in boundary_pixels.keys():
            boundary_pixels.pop(processed_key)


      print(" boundary pixel shape counter " + str(boundary_shape_counter))
      print("")
      
      print(" here comes boundary shapes " )
      print(boundary_shapes)

           

      # current running pixel has put its neighbors in boundary shapes. Now pick next pixel to start putting neighbors again
      if not len(boundary_pixels)==0:
          pixel_number = list(boundary_pixels.keys())[0]
          current_running_pixels_list = [pixel_number]
          return process_neighbors(current_running_pixels_list)
      else:
          print(" boundary_pixels should now be empty ")
          return_flag = True
          return boundary_shapes





   # ---------------------------       get_boundary_shapes        ---------------------------------



   # boundary_shapes contains boundary shape number, pixel number, xy values
   # form is shown below
   # boundary shapes[choundary shape number ][ pixel number ]['x']
   # boundary shapes[choundary shape number ][ pixel number ]['y']
   boundary_shapes = {}
   boundary_shape_counter = 0
   already_processed_pixels = []
   
   shape_number = None
   multiple_neighbor = False


   # first, get arbitrary pixel
   arbitrary_starting_pixel_key = list(boundary_pixels.keys())[0]
   
   print(arbitrary_starting_pixel_key)


   # putting first arbitrary pixel into boundary shapes 
   boundary_shape_counter += 1
   boundary_shapes[boundary_shape_counter] = { arbitrary_starting_pixel_key: {'x': boundary_pixels[arbitrary_starting_pixel_key]['x'], 'y': boundary_pixels[arbitrary_starting_pixel_key]['y'] } }


   pixel_list = []
   pixel_list.append(arbitrary_starting_pixel_key)

   return process_neighbors(pixel_list)





# IN parameters
# pixel: pixel to find its direct neighbors
# pixel form is
# { 'x': 100, 'y': 200 }
# pixels: pixels to look for pixel's direct neighbors
# pixels parameter form is....
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
#
# {1: {'x': 97, 'y': 52}, 2: {'x': 106, 'y': 52}......}
#
# returns
# all found direct neighbors in the same form as IN pixels parameter

def find_direct_neighbors(pixel, pixels):

   # all found direct neighbors
   found_neighbors = {}
   
   for neighbor_search_pixel_id in pixels:
  
      # looking for top direct neighbor
      # direct top neighbor is: ( current x, y )  then direct top neighbor is ( top x, y - 1)
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] and pixel['y'] == pixels[neighbor_search_pixel_id]['y'] - 1:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         
      # looking for top right direct neighbor
      # direct top right neighbor is: ( current x, y ) then direct top right neighbor is ( top right x + 1, y - 1 )
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] + 1 and pixel['y'] == pixels[neighbor_search_pixel_id]['y'] - 1:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         
      # looking for direct right neighbor
      # direct right neighbor is: ( current x, y )  then direct right neighbor is ( right x + 1, y )
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] + 1 and pixel['y'] == pixels[neighbor_search_pixel_id]['y']:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         
      # looking for direct bottom right neighbor
      # direct bottom right neighbor is: ( current x, y )  then direct bottom right neighbor is ( bottom right x + 1, y + 1 )
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] + 1 and pixel['y'] == pixels[neighbor_search_pixel_id]['y'] + 1:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         
      # looking for direct bottom neighbor
      # direct bottom neighbor is: ( current x, y )  then direct bottom neighbor is ( bottom x, y + 1 )
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] and pixel['y'] == pixels[neighbor_search_pixel_id]['y'] + 1:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         
      # looking for direct bottom left neighbor
      # direct bottom left neighbor is: ( current x, y )  then direct bottom left neighbor is ( bottom x - 1, y + 1 )
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] - 1 and pixel['y'] == pixels[neighbor_search_pixel_id]['y'] + 1:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         
      # looking for direct left neighbor
      # direct left neighbor is: ( current x, y )  then direct left neighbor is ( bottom x - 1, y )
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] - 1 and pixel['y'] == pixels[neighbor_search_pixel_id]['y']:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         
      # looking for direct top left neighbor
      # direct top left neighbor is: ( current x, y )  then direct top left neighbor is ( bottom x - 1, y - 1 )
      if pixel['x'] == pixels[neighbor_search_pixel_id]['x'] - 1 and pixel['y'] == pixels[neighbor_search_pixel_id]['y'] - 1:
         found_neighbors[neighbor_search_pixel_id] = pixels[neighbor_search_pixel_id]
         

   return found_neighbors






# IN parameters
# pixels: pixels to look for pixel's direct neighbors
# pixels parameter form is....
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
#
# {1: {'x': 97, 'y': 52}, 2: {'x': 106, 'y': 52}......}
#
# returns
# all found direct neighbors in the same form as IN pixels parameter

def get_direct_neighbors(pixels):

   # all found direct neighbors
   found_neighbors = {}
   

   
   for pixel_id in pixels:
   
      pixel_counter = 1
  
      # getting top direct neighbor
      # direct top neighbor is: ( current x, y )  then direct top neighbor is ( top x, y - 1)
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'], 'y': pixels[pixel_id]['y'] - 1 }
      pixel_counter += 1
         
      # getting top right direct neighbor
      # direct top right neighbor is: ( current x, y ) then direct top right neighbor is ( top right x + 1, y - 1 )
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'] + 1, 'y': pixels[pixel_id]['y'] - 1 }
      pixel_counter += 1
       
      # getting direct right neighbor
      # direct right neighbor is: ( current x, y )  then direct right neighbor is ( right x + 1, y )
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'] + 1, 'y': pixels[pixel_id]['y']}
      pixel_counter += 1
         
      # getting direct bottom right neighbor
      # direct bottom right neighbor is: ( current x, y )  then direct bottom right neighbor is ( bottom right x + 1, y + 1 )
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'] + 1, 'y': pixels[pixel_id]['y'] + 1 }
      pixel_counter += 1
         
      # getting direct bottom neighbor
      # direct bottom neighbor is: ( current x, y )  then direct bottom neighbor is ( bottom x, y + 1 )
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'], 'y': pixels[pixel_id]['y'] + 1 }
      pixel_counter += 1
       
      # getting direct bottom left neighbor
      # direct bottom left neighbor is: ( current x, y )  then direct bottom left neighbor is ( bottom x - 1, y + 1 )
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'] - 1, 'y': pixels[pixel_id]['y'] + 1 }
      pixel_counter += 1

      # getting direct left neighbor
      # direct left neighbor is: ( current x, y )  then direct left neighbor is ( bottom x - 1, y )
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'] - 1, 'y': pixels[pixel_id]['y'] }
      pixel_counter += 1         
         
      # getting direct top left neighbor
      # direct top left neighbor is: ( current x, y )  then direct top left neighbor is ( bottom x - 1, y - 1 )
      found_neighbors[str(pixel_id) + '_neighbor' + str(pixel_counter)] = { 'x': pixels[pixel_id]['x'] - 1, 'y': pixels[pixel_id]['y'] - 1 }       

   return found_neighbors





def find_direct_shape_neighbors(image_filename, directory_under_images):

    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images.find('/') == -1:
       directory_under_images +='/'

    if os.path.exists("shapes") == False:
       os.mkdir("shapes")


    shapes_neighbors_filename = "shapes/" + image_filename + " shapes_neighbors.txt"

    image_original = 'images/' + directory_under_images + image_filename + '.png'

    read_original_image = Image.open(image_original)

    original_width, original_height = read_original_image.size

    # for storing shape's neighbor shapes
    # { shape id: [ neighboor shape id1 , neighbor shape id2, ..... ] }
    shape_neighbors = {}

    already_processed_shapes = []


    whole_image_shapes = recreate_shapes.get_whole_image_shape(True, image_filename, directory_under_images)  

    for pixel_shape_id , pixel_xy_values in whole_image_shapes.items():  
       # outer loop is for current running shape which looks for direct shape neighbors
       
       print(pixel_shape_id)
       # every shape has its neighbors
       shape_neighbors[pixel_shape_id] = []
       
       boundary_pixels = get_boundary_pixels(pixel_xy_values)
       
       boundary_direct_neigbors = get_direct_neighbors(boundary_pixels)
       
       # for storing boundary pixels' neighbor pixel indexes. if candidate neighbor shape contains any of the 
       # index numbers in it, then this candidate is neighbor shape
       pixel_indexes = []
       
       for shape_id, xy_values in boundary_direct_neigbors.items():
       
          pixel_index = xy_values['y'] * original_width + xy_values['x']
          pixel_indexes.append(pixel_index)
          
       for neighbor_shape_id , neighbor_pixel_xy_values in whole_image_shapes.items():         
          # inner loop is for finding neighbors for current running shape
          
          neighbor_pixel_indexes = []
          
          for key in neighbor_pixel_xy_values:
       
             neighbor_pixel_index = neighbor_pixel_xy_values[key]['y'] * original_width + neighbor_pixel_xy_values[key]['x']
             neighbor_pixel_indexes.append(neighbor_pixel_index)
          
             
          if not pixel_shape_id == neighbor_shape_id:  
             for pixel_index in pixel_indexes:
                if pixel_index in neighbor_pixel_indexes:

                   shape_neighbors[pixel_shape_id].append(neighbor_shape_id)
                   break
                
          elif pixel_shape_id == neighbor_shape_id or neighbor_shape_id in already_processed_shapes:
             break        
             
        
       if len(shape_neighbors[pixel_shape_id]) == 0:
          shape_neighbors.pop(pixel_shape_id)
             
       already_processed_shapes.append(pixel_shape_id)


    f = open(shapes_neighbors_filename, 'w')
    f.write(str(shape_neighbors))
    f.close()





    return shape_neighbors




def get_shapes_colors(filename, directory):

    # directory is specified but does not contain /
    if directory != "" and directory.find('/') == -1:
       directory +='/'

    shapes_color_filename = "shapes/" + filename + " shapes_colors.txt"

    image_original = 'images/' + directory + filename + '.png'

    read_original_image = Image.open(image_original)

    image_width, image_height = read_original_image.size

    image_pixels = read_original_image.getdata()

    shapes_colors = {}

    whole_image_shapes = recreate_shapes.get_whole_image_shape(True, filename, directory)

    for shape_id , pixel_xy_values in whole_image_shapes.items():
       print(shape_id)
    
       shapes_colors[shape_id] = {}
    
       # for storing RGB values for each shape. Initializing for each shape
       Red = []
       Green = []
       Blue = []
    
       for pixel_id in pixel_xy_values:

          image_index = pixel_xy_values[pixel_id]['y'] * image_width + pixel_xy_values[pixel_id]['x']

          r, g, b, a = image_pixels[ image_index ]
          Red.append(r)
          Green.append(g)
          Blue.append(b)


          r = round(mean(Red))
          g = round(mean(Green))
          b = round(mean(Blue))
       
          shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }


    f = open(shapes_color_filename, 'w')
    f.write(str(shapes_colors))
    f.close()

    return shapes_colors











































































































