import re
from PIL import Image
import os
import recreate_shapes
from statistics import mean

# returns all pixel shape ids and all its pixel indexes
# pixel id dictionary[ matched pixel shape id ] = [ pixel index1, pixel index2, ..... ]
def get_all_pixels_of_shapes(shape_ids, image_filename, directory_under_images=""):


    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images.find('/') == -1:
       directory_under_images +='/'

    shapes_file = open("shapes/" + image_filename + " shapes.txt")
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
                
                
         previous_x_value = x_value               

         pixel_counter += 1
         x_counter_in_current_running_y += 1











   # -----------------------------          now this is for getting boundaries vertically        ----------------------------------------



   smallest_x = min(int(d['x']) for d in pixels_dict.values())
   largest_x = max(int(d['x']) for d in pixels_dict.values())


   pixel_counter = 1

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
 
         # check if current y value is the last one in the current running y
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
                
         previous_y_value = y_value    

         pixel_counter += 1
         y_counter_in_current_running_x += 1




   return pixel_boundaries





















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





def compute_appearance_difference(current_pix, compare_pixel):

   original_red, original_green, original_blue, alpha = current_pix

   compare_red, compare_green, compare_blue, alpha = compare_pixel
    
   red_difference = abs(original_red - compare_red)
   green_difference = abs(original_green - compare_green)
   blue_difference = abs(original_blue - compare_blue)
    
   total_difference = red_difference + green_difference + blue_difference

   average = total_difference / 3

   # exclude 0 or negatie values because 0 or negative values mean that difference is smaller than average.
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







