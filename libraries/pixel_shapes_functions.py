
import re
from PIL import Image
import os, sys
from statistics import mean
import math

from libraries import read_files_functions, image_functions
from libraries.cv_globals import proj_dir, top_images_dir, top_shapes_dir


# shape_ids is list containing shape ids
# [20085]
# returns all pixel shape ids and all its pixel indexes
# pixel id dictionary[ matched pixel shape id ] = [ pixel index1, pixel index2, ..... ]
def get_all_pixels_of_shapes(shape_ids, image_filename, directory_under_images=""):


    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images[-1] != "/":
       directory_under_images +='/'

    shapes_file = open(top_shapes_dir + directory_under_images + "shapes/" + image_filename + "_shapes.txt")
    shapes_file_contents = shapes_file.read()


    original_image = Image.open(top_images_dir + str(directory_under_images) + image_filename + ".png")

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
              

           shapes_with_indexes[shapes_id] = [shapes_id]



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



# pixel is pixel index number
def get_shapeid_frompix(pixel, image_filename, directory_under_images=""):


    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images[-1] != "/":
       directory_under_images +='/'

    shapes_file = open(top_shapes_dir + directory_under_images + "shapes/" + image_filename + "_shapes.txt")
    shapes_file_contents = shapes_file.read()


    original_image = Image.open(top_images_dir + str(directory_under_images) + image_filename + ".png")

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

    # match contains all image shapes
    for shape in match:


       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       shapes_id = match_temp.group().strip('(,')
           
       if str(shapes_id) == str(pixel):
          shapes_with_indexes[shapes_id] = [shapes_id]
          
          return shapes_with_indexes
              

       



    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
    '''
    multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    match = re.findall(multiple_pixel_pattern, shapes_file_contents)
    

    # match contains all image shapes
    for shape in match:


       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       shapes_id = match_temp.group().strip('(,')
       
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


       if pixel in one_string_list:
          shapes_with_indexes[shapes_id] = one_string_list
          
          return shapes_with_indexes

       


    return None





# get all shapeids for the given parameter pixel index numbers
# input parameter "pixels" is list containing pixel index numbers
def get_shapeids_frompixels( pixels, imfile, imdir ):


    # directory is passed in parameter but does not contain /
    if imdir != "" and imdir[-1] != ('/'):
       imdir +='/'

    shapes_file = open(top_shapes_dir + imdir + "shapes/" + imfile + "_shapes.txt")
    shapes_file_contents = shapes_file.read()


    img = Image.open(top_images_dir + str(imdir) + imfile + ".png")

    image_width, image_height = img.size



    # single pixel shapes
    # ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
    # space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
    # single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'

    single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
    match = re.findall(single_pixel_pattern, shapes_file_contents)


    # shapes_with_indexes[matched shape id ] = [ pixel index1, pixel index2 .... ]
    shapepix = {}

    # match contains all image shapes
    for shape in match:


       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       shapeid = match_temp.group().strip('(,')
           
       if shapeid in pixels:
          shapepix[shapeid] = [ shapeid ]




    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
    '''
    multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    match = re.findall(multiple_pixel_pattern, shapes_file_contents)


    # match contains all image shapes
    for shape in match:

       # getting shapeid
       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       # removing "(,"
       shapeid = match_temp.group().strip('(,')
       
       # get list of all pixels of a shape
       # start_pixel_list
       start_pix_l = shape.find("[")
       end_pix_l = shape.find("]")
       
       allpix = shape[ start_pix_l : end_pix_l + 1]
       allpix = allpix.strip('][').split(', ')
       
       
       
       # check if image pixel is containd in input pixels
       for pix in allpix:
          if pix in pixels:
             shapepix[shapeid] = allpix



    return shapepix

















#  parameter in and out is a dictionary with following form.
#    pixels_dict = {1: { "x": x, "y": y }, 2: { "x": x, "y": y }, ... }
#  keys are not pixel index number. they are just incremental values starting from 1
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


   # duplicate xy coordinates created if pixels are found both virtically and horizontally. so remove them
   temp = {}

   for key, value in pixel_boundaries.items():
      if value not in temp.values():
         temp[key] = value
      
   pixel_boundaries = temp
   pixel_boundaries = {k: v for k, v in sorted(pixel_boundaries.items(), key=lambda item: (item[1]['y'], item[1]['x']))}

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






# orig_pixels, comp_pixels parameter form is....
#    pixels[pixel_counter] = {}
#    pixels[pixel_counter] ['x'] = x
#    pixels[pixel_counter] ['y'] = y
#
# {1: {'x': 97, 'y': 52}, 2: {'x': 106, 'y': 52}......}
#
# returns False or None if any pixel of orig_pixels is not neighbor with any pixel of comp_pixels
# returns matched orig and comp index numbers
# returns { orig1: orig index, comp1: comp index, orig2: orig index, comp2: comp index..... }

def find_direct_neighbors(orig_pixels, comp_pixels):


   original_smallest_y = min(int(d['y']) for d in orig_pixels.values())
   original_largest_y = max(int(d['y']) for d in orig_pixels.values())
   original_smallest_x = min(int(d['x']) for d in orig_pixels.values())
   original_largest_x = max(int(d['x']) for d in orig_pixels.values())   
   
   
   
   # original shape's neighbor will be somewhere between original_smallest_y - 1 and original_largest_y + 1
   orig_neighbor_top = original_smallest_y - 1
   orig_neighbor_bottom = original_largest_y + 1
   orig_neighbor_left = original_smallest_x - 1
   orig_neighbor_right = original_largest_x + 1
   
   comp_smallest_y = min(int(d['y']) for d in comp_pixels.values())
   comp_largest_y = max(int(d['y']) for d in comp_pixels.values())
   comp_smallest_x = min(int(d['x']) for d in comp_pixels.values())
   comp_largest_x = max(int(d['x']) for d in comp_pixels.values()) 
   
   maybe_neighbors_y = False
   maybe_neighbors_x = False

   # when compare shape is above original shape, compare shape's bottom has to be at the same place or below original top.
   if comp_smallest_y <= orig_neighbor_top and comp_largest_y >= orig_neighbor_top:
      maybe_neighbors_y = True
   
   # when compare shape is below original shape then compare shape's top has to be at the same place or above original shape's 
   # bottom
   elif comp_smallest_y > orig_neighbor_top and comp_smallest_y <= orig_neighbor_bottom:
      maybe_neighbors_y = True
      
   # when comapre shape is at the same place or further left than original shape, compare shape's right has to be at the same 
   # place or further right than original shape's left 
   if comp_smallest_x <= orig_neighbor_left and comp_largest_x >= orig_neighbor_left:
      maybe_neighbors_x = True
      
   # when compare shape is at the same place or further right than original shape, compare shape's left has to be at the same 
   # place or further left than the original shape's right
   elif comp_smallest_x > orig_neighbor_left and comp_smallest_x <= orig_neighbor_right:
      maybe_neighbors_x = True
   
   if (not maybe_neighbors_y) or (not maybe_neighbors_x):
      return False

   # all found direct neighbors
   found_neighbors = {}
   nbr_counter = 1
   found_neighbor_flag = False
   
   for orig_pixel in orig_pixels.values():
      for comp_pixel in comp_pixels.values():
  
         # looking for top direct neighbor
         # if current pixel is ( current x, y )  then direct top neighbor is ( top x, y - 1)
         if comp_pixel['x'] == orig_pixel['x'] and comp_pixel['y'] == orig_pixel['y'] - 1:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
         # looking for top right direct neighbor
         # if current pixel is  ( current x, y ) then direct top right neighbor is ( top right x + 1, y - 1 )
         if comp_pixel['x'] == orig_pixel['x'] + 1 and comp_pixel['y'] == orig_pixel['y'] - 1:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
         # looking for direct right neighbor
         # if current pixel is ( current x, y )  then direct right neighbor is ( right x + 1, y )
         if comp_pixel['x'] == orig_pixel['x'] + 1 and comp_pixel['y'] == orig_pixel['y']:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
         # looking for direct bottom right neighbor
         # if current pixel is  ( current x, y )  then direct bottom right neighbor is ( bottom right x + 1, y + 1 )
         if comp_pixel['x'] == orig_pixel['x'] + 1 and comp_pixel['y'] == orig_pixel['y'] + 1:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
         # looking for direct bottom neighbor
         # if current pixel is ( current x, y )  then direct bottom neighbor is ( bottom x, y + 1 )
         if comp_pixel['x'] == orig_pixel['x'] and comp_pixel['y'] == orig_pixel['y'] + 1:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
         # looking for direct bottom left neighbor
         # if current pixel is ( current x, y )  then direct bottom left neighbor is ( bottom x - 1, y + 1 )
         if comp_pixel['x'] == orig_pixel['x'] - 1 and comp_pixel['y'] == orig_pixel['y'] + 1:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
         # looking for direct left neighbor
         # if current pixel is ( current x, y )  then direct left neighbor is ( bottom x - 1, y )
         if comp_pixel['x'] == orig_pixel['x'] - 1 and comp_pixel['y'] == orig_pixel['y']:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
         # looking for direct top left neighbor
         # if current pixel is ( current x, y )  then direct top left neighbor is ( bottom x - 1, y - 1 )
         if comp_pixel['x'] == orig_pixel['x'] - 1 and comp_pixel['y'] == orig_pixel['y'] - 1:
            found_neighbors['orig' + str(nbr_counter)] = orig_pixel
            found_neighbors['comp' + str(nbr_counter)] = comp_pixel
            found_neighbor_flag = True
            nbr_counter += 1
         
   if found_neighbor_flag: 
      return found_neighbors
   else:
      return



def get_all_shapes_colors(filename, directory):

    # directory is specified but does not contain /
    if directory != "" and directory[-1] != ('/'):
       directory +='/'

    image_file = top_images_dir + directory + filename + '.png'

    read_image = Image.open(image_file)

    image_width, image_height = read_image.size

    image_pixels = read_image.getdata()

    shapes_colors = {}

    whole_image_shapes = read_files_functions.rd_shapes_file(filename, directory)

    for shape_id , pixel_xy_values in whole_image_shapes.items():
    
       shapes_colors[shape_id] = {}
    
       # for storing RGB values for each shape. Initializing for each shape
       Reds = []
       Greens = []
       Blues = []
    
       pixels_color_counter = 0
       for pixel_id in pixel_xy_values:

          image_index = pixel_xy_values[pixel_id]['y'] * image_width + pixel_xy_values[pixel_id]['x']

          if len(image_pixels[ image_index ]) == 3:
             r, g, b = image_pixels[ image_index ]
          else:
             r, g, b, a = image_pixels[ image_index ]

          Reds.append(r)
          Greens.append(g)
          Blues.append(b)

          # maximum sample counts of each shape is 100
          if pixels_color_counter > 100:
             break

          pixels_color_counter += 1
          
       r = round(mean(Reds))
       g = round(mean(Greens))
       b = round(mean(Blues))
       

       
       shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }

    return shapes_colors



# returns
# { "shapeid number": [ image_area number, image_area number ... ] }
def localize_shape( shape_coordinates , image_areas , shapeid ):


   def get_shape_locations( shape_coordinates ):

      shape_locations = []

      shape_smallest_y = min(int(d['y']) for d in shape_coordinates.values())
      shape_largest_y = max(int(d['y']) for d in shape_coordinates.values())

      y_interval = round( ( shape_largest_y - shape_smallest_y ) / 5 )
      
      if y_interval < 1:
         y_interval = 1

      for y in range ( shape_smallest_y , shape_largest_y + 1 , y_interval ):


         # pixel_ids_at_top contains all xy coordinate pairs that have the current running y value.
         pixel_ids = [k for k in shape_coordinates  if (int(shape_coordinates[k]['y'])) == y]

      
      
         # we first obtain all x values for the current running y value
         x_es = []
      
         # key is the coordinate pair id.  
         for key in pixel_ids:
            # putting all x values for all xy coordinates that have current running y vaule
            x_es.append(shape_coordinates[key]['x'])

      
         # we need to sort x values so that we can work with neighbor x values
         x_es.sort()

         leftmost_x = min( x_es )
         rightmost_x = max( x_es )
         
         x_interval = round( ( rightmost_x - leftmost_x ) / 5 )
         
         if x_interval < 1:
            x_interval = 1

         for x in range( leftmost_x , rightmost_x + 1, x_interval  ):
            temp = {}
            temp['x'] = x
            temp['y'] = y
            
            shape_locations.append( temp )
        
        
      return shape_locations


      #   ----------------------------------     End of get_shape_locations      ------------------------------------------


   shape_locations = shape_coordinates.values()

   shape_in_image_areas = []
   
   location_threshold = 3  
   
   location_labels = [ { 'top_middle': {'y_threshold': ( - location_threshold ), 'x_threshold': ( location_threshold, - location_threshold ) }, \
                      'right': { 'y_threshold': ( location_threshold, - location_threshold ), 'x_threshold': ( location_threshold ) }, \
                      'bottom_middle': { 'y_threshold': ( location_threshold ), 'x_threshold': ( location_threshold, - location_threshold ) }, \
                      'left': { 'y_threshold': ( location_threshold, - location_threshold ), 'x_threshold': ( - location_threshold ) } } ]

   
   for shape_location in shape_locations:
      
      for image_area in image_areas:
         for area_num, image_loc in image_area.items():
            
            cur_area_present = False
            if shape_in_image_areas:
               for shape_in_image_area in shape_in_image_areas:
                  if shape_in_image_area['image_area'] == area_num:
                     cur_area_present = True
                     
                     break
            
            if cur_area_present:
               continue
               
            image_shape_loc_match = False
            
            for location_label in location_labels:
               if image_shape_loc_match:
                  break
               for loc_label, thresholds in location_label.items():
                  if image_shape_loc_match:
                     break               

                  if shape_location['x'] >= image_loc['left'] and shape_location['x'] <= image_loc['right']:
                     if shape_location['y'] >= image_loc['top'] and shape_location['y'] <= image_loc['bottom']:
                        image_shape_loc_match = True
                     
                        temp = {}
                        temp['shapeid'] = shapeid
                        temp['image_area'] = area_num
                     
                        shape_in_image_areas.append( temp )
                    
                        break
               
                  # if there is only one threshold, it becomes int value only. if there is two, it would be tuple
                  if type(thresholds['x_threshold']) != int:
                     for x_threshold in thresholds['x_threshold']:                
               
                        if not image_shape_loc_match:
                           # check with the threshold
                           if shape_location['x'] + x_threshold >= image_loc['left'] and shape_location['x'] + x_threshold <= image_loc['right']:
                              if shape_location['y'] >= image_loc['top'] and shape_location['y'] <= image_loc['bottom']:
                                 image_shape_loc_match = True
                     
                                 temp = {}
                                 temp['shapeid'] = shapeid
                                 temp['image_area'] = area_num
                     
                                 shape_in_image_areas.append( temp )
                        
                                 break

                  if type( thresholds['y_threshold'] ) != int :
                     for y_threshold in thresholds['y_threshold']:
   
                        if not image_shape_loc_match:
                           # check with the threshold
                           if shape_location['x']  >= image_loc['left'] and shape_location['x'] <= image_loc['right']:
                              if shape_location['y'] + y_threshold >= image_loc['top'] and shape_location['y'] + y_threshold <= image_loc['bottom']:
                                 image_shape_loc_match = True
                    
                                 temp = {}
                                 temp['shapeid'] = shapeid
                                 temp['image_area'] = area_num
                     
                                 shape_in_image_areas.append( temp )
                        
                                 break   
   
   # currently shape_in_image_areas have following form
   # [{'shapeid': '30184', 'image_area': 5}, {'shapeid': '30184', 'image_area': 10}]
   # this should be in following form
   # { "shapeid number": [ image_area number, image_area number ... ] }
   shape_im_areas = {}
   im_a_shapeid = None
   for shape_in_image_area in shape_in_image_areas:
      for sid_or_im_a in shape_in_image_area:
         if len(shape_im_areas) == 0 and sid_or_im_a == "shapeid":
            im_a_shapeid = shape_in_image_area[sid_or_im_a]
            shape_im_areas[ im_a_shapeid ] = []
            
            
         
         elif sid_or_im_a == "image_area":
            shape_im_areas[im_a_shapeid].append( shape_in_image_area[sid_or_im_a] )
   
   return shape_im_areas




   

# orig_coords and comp_coords have the following form
# {'179': {'x': 179, 'y': 0}} single pixel
# multiple pixels
# {27273: {'x': 93, 'y': 151}, 27453: {'x': 93, 'y': 152}, 27452: {'x': 92, 'y': 152}, 27632: {'x': 92, 'y': 153}}
# shape_ids are original and compare shapeid
# shape_ids is as follows
# shape_ids = [ int('550' ), int ('179') ]
# returns locations list if they are close, if not, returns empty list
def are_shapes_near(orig_file, comp_file, directory, orig_coords, comp_coords, shape_ids ):


   # needed for creating image areas
   original_image = Image.open(top_images_dir + directory + orig_file + ".png")
   image_width, image_height = original_image.size

   compare_image = Image.open(top_images_dir + directory + comp_file + ".png")
   compare_image_width, compare_image_height = compare_image.size

   # make sure original image size(width, height) is exactly the same as compare image size(width, height)
   if not (image_width == compare_image_width and image_height == compare_image_height):
      return False

   image_areas = image_functions.get_image_areas( im_file, directory )

      
   orig_locations = localize_shape( orig_coords , image_areas , shape_ids[0] )

   orig_image_areas = []
      
   for orig_location in orig_locations:
      orig_image_areas.append( orig_location['image_area'] )

   comp_locations = localize_shape( comp_coords , image_areas , shape_ids[1] )
   
   matched_areas = []
   for comp_location in comp_locations.values():
      for orig_image_area in orig_image_areas.values():
            
         for comp_loc in comp_location:
            if comp_loc in orig_image_area:
               matched_areas.append( comp_loc )
                
         
   if matched_areas:
      temp = {}
      temp['orig_shapeid'] = shape_ids[0]
      temp['comp_shapeid'] = shape_ids[1]
      temp["m_areas"] = []

      for matched_area in matched_areas:
         temp["m_areas"].append(matched_area)

      return temp
   else:
      return None





# shape_coords have the following form
# {'179': {'x': 179, 'y': 0}} single pixel
# multiple pixels
# {27273: {'x': 93, 'y': 151}, 27453: {'x': 93, 'y': 152}, 27452: {'x': 92, 'y': 152}, 27632: {'x': 92, 'y': 153}}
# shape_coords keys can be string or int. does not matter because shape_coords values are used only and keys are not used.
# shapeid is int.
def get_shape_im_locations( im_file, directory, shape_coords, shapeid ):


   image_areas = image_functions.get_image_areas( im_file, directory )

      
   shape_locations = localize_shape( shape_coords , image_areas , shapeid )

   return shape_locations






# xy_coordinates should be a list of dictionaries containing coordinates
def highlight_matches( shape_ids, filenames, xy_coordinates, func_name ):
   
   if not xy_coordinates:
      return
   
   x_present = False
   y_present = False   
   compare_label = None

   if os.path.exists("debug") == False:
      os.mkdir("debug")

   # check labels of compare pixels. they aren't necessarily in every dictionary. so we have to see and check
   for i in range( 0 , len(xy_coordinates) ):

      if 'compare_x' in xy_coordinates[i]:
         compare_label = 'compare_'
         break
      if 'matched_x' in xy_coordinates[i]:
         compare_label = 'matched_'
         break

   original_image = Image.open("shapes/" + str(filenames[0]) + "_shapes/" + str(shape_ids[0]) + ".png")
   image_width, image_height = original_image.size

   compare_image = Image.open("shapes/" + str(filenames[1]) + "_shapes/" + str(shape_ids[1]) + ".png")
   compare_image_width, compare_image_height = compare_image.size

   for xy_coordinate in xy_coordinates:
      
      if 'original_x' in xy_coordinate:
         original_image.putpixel( (xy_coordinate['original_x'] , xy_coordinate['original_y']) , (0, 0, 0) )
          
      if compare_label + 'x' in xy_coordinate:
         compare_image.putpixel( (xy_coordinate[compare_label + 'x'] , xy_coordinate[compare_label + 'y']) , (0, 0, 0) )

         

   original_image.save( "debug/" +  func_name + " original " + str(shape_ids[0]) + " comp " + str(shape_ids[1]) + ".png")
   compare_image.save("debug/" + func_name + " orig " + str(shape_ids[0]) + " compare " + str(shape_ids[1]) + ".png")










































































