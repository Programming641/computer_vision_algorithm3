import re
from PIL import Image

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






    # not taking single pixel shapes
    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
    space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
    single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'

    single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
    match = re.findall(single_pixel_pattern, shapes_file_contents)

    '''


    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
    '''
    multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    match = re.findall(multiple_pixel_pattern, shapes_file_contents)
    
    
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

   smallest_y = min(int(d['y']) for d in pixels_dict.values())
   largest_y = max(int(d['y']) for d in pixels_dict.values())

 
   first = True
   pixel_counter = 1



   # for loop for going from smallest y value to the largest y value
   # this means going from very top pixel to very bottom pixel
   #  for y in range(start, stop) stop value is excluded
   for y in range(smallest_y, largest_y + 1):

      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in pixels_dict  if (int(pixels_dict[k]['y'])) == y]
      
      missing_x_value_threshold = 5
      
      
      # we first obtain all x values for the current running y value
      x_values_list_in_current_y = []
      
      
      '''
      -------------------        boundary finding algorithm            ---------------------------
      
      With current running y value, boundary is where there is no consecutive x values. This means there is no more 
      neighbor x values for a while.  The " boundary left side " has missing x values on the " left " ( no more smaller x values )
      The " boundary right side " has missing x values on the " right " ( missing neighbor larger x values for a while )
      " for a while " should be the threshold for finding " missing x values "
      finally, the smallest and largest x values are the farthest of all pixels in the current running y value.
      '''
      
      # key is the coordinate pair id.  
      for key in pixel_ids_with_current_y_values:
      
         # putting all x values for all xy coordinates that have current running y vaule
         x_values_list_in_current_y.append(pixels_dict[key]['x'])

      
      # we need to sort x values so that we can work with neighbor x values
      x_values_list_in_current_y.sort()


      for x_value in x_values_list_in_current_y:
 


         if first != False:
            previous_x_value = x_value
            first = False
            
         else:
         
             if abs( x_value - previous_x_value ) > missing_x_value_threshold:
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
                
                
                

             pixel_counter += 1
                




   return pixel_boundaries

















