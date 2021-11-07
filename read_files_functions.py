import re
import math
from PIL import Image
import time
import ast

def read_shapes_file(image_filename, directory_under_images):

    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images.find('/') == -1:
           directory_under_images +='/'


    original_image = Image.open("images/" + directory_under_images + image_filename + ".png")

    image_width, image_height = original_image.size

    original_image_data = original_image.getdata()

    image_file = open('shapes/' + image_filename + '_shapes.txt')
    image_file_contents = image_file.read()
    
    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
    space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
    single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    '''
    single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
    match = re.findall(single_pixel_pattern, image_file_contents)
    
    shapes = {}


    # match contains all shapes
    for shape in match:


       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       shapes_id = match_temp.group().strip('(,')
 
       shapes[shapes_id] = {}

       # for single pixel shapes, shape_id is the same as pixel index number
       pixel_index = int(shapes_id)
       
       y = math.floor(pixel_index / image_width)
       x  = pixel_index % image_width          
                      
       shapes[shapes_id][shapes_id] = {}
       shapes[shapes_id][shapes_id]['x'] = x
       shapes[shapes_id][shapes_id]['y'] = y


    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
    '''
    multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    match = re.findall(multiple_pixel_pattern, image_file_contents)

    # match contains all shapes
    for shape in match:

       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       shapes_id = match_temp.group().strip('(,')

       pixels_list_pattern = '\[.*\]'
       pixels_index_string = re.findall(pixels_list_pattern, shape)

       shapes[shapes_id] = {}

       #pixel_index_string contains one shape
       # pixels_index_string is a list but contains only one string
       for one_string in pixels_index_string:
      
          # one_string is a one string. removing unnecessary characters leaving only the numbers
          one_string_stripped = one_string.strip('[, ]')
          # split each number by ,
          one_string_list = one_string_stripped.split(',')

          # now iterate over all pixel index numbers
          for pixel_index in one_string_list:
             pixel_index = int(pixel_index)
         
             original_image_red, original_image_green, original_image_blue = original_image_data[pixel_index ]
             y = math.floor(pixel_index / image_width)
             x  = pixel_index % image_width          
             
             shapes[shapes_id][pixel_index] = {}
             shapes[shapes_id][pixel_index]['x'] = x
             shapes[shapes_id][pixel_index]['y'] = y
             
             
    image_file.close()
    return shapes



# data inside the file has the form below
# {'6389': ['6735', '6389'], '12308': ['12654']....}
def read_dict_key_value_list(image_filename, directory_under_images, filepath):

    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images.find('/') == -1:
           directory_under_images +='/'


    original_image = Image.open("images/" + directory_under_images + image_filename + ".png")

    image_width, image_height = original_image.size


    image_file = open(filepath)
    image_file_contents = image_file.read()

    key_is_single_quoted = True

    # shapes_neighbors file has key value surrounded by single quotes but repeating pattern shapes file 
    # does not have keys surrounded by single quotes
    key_single_quoted_pattern = "\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\': "
    match = re.findall(key_single_quoted_pattern, image_file_contents)

    if len(match) == 0:
       key_is_single_quoted = False

    if key_is_single_quoted == True:    
       # this is for getting single neighbors
       # pattern is...
       # ' then comes numbers 1-image size digits then comes ' then comes : then comes space then comes [ then comes single quote
       # then comes 1-image size digits then comes single quote then comes ]
       single_pattern = "\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\': \[\'[0-9]{1," + str(len(str(image_width * image_height))) + \
                              "}\'\]"
                           
       match = re.findall(single_pattern, image_file_contents)


    if key_is_single_quoted == False:
       single_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}: \[\'[0-9]{1," + str(len(str(image_width * image_height))) + \
                              "}\'\]"
                           
       match = re.findall(single_pattern, image_file_contents)

    dictionary = {}
    
    for m in match:
    
       if key_is_single_quoted == True:
          # getting keys from single shape neighbors
          single_key_pattern = "\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\':"
          single_key = re.search(single_key_pattern, m).group()
       
       # for key values not surrounded by single quotes
       if key_is_single_quoted == False:
          single_key_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}:"
          single_key = re.search(single_key_pattern, m).group()
       
       # removing single quote and colon
       single_key_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}"
       single_key = re.search(single_key_pattern, single_key).group()
       
       dictionary[single_key] = ""
       
       # this time is for single neighbors of single neighbor shapes
       single_value_pattern = "\[\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\'\]"
       single_value = re.search(single_value_pattern, m).group()
       
       # getting only numbers
       single_value_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}"
       single_value = re.search(single_value_pattern, single_value ).group()
       
       dictionary[single_key] = [single_value]
       
    if key_is_single_quoted == True:   
       # multiple neighbor shapes
       # "\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\':"     this is for getting shape id 
       multiple_pattern = "\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\':" + " \[" + \
                                "(?:\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\',\s{1})+\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\'\]"
                                
       match = re.findall(multiple_pattern, image_file_contents)
 
    # for key values not surrounded by single quotes
    if key_is_single_quoted == False:
       multiple_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}:" + " \[" + \
                                "(?:\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\',\s{1})+\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\'\]"
                                
       match = re.findall(multiple_pattern, image_file_contents)



    for m in match:

       if key_is_single_quoted == True: 
          # getting keys from multiple shape neighbors
          multiple_key_pattern = "\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\':"
          multiple_key = re.search(multiple_key_pattern, m).group()
 
       # for key values not surrounded by single quotes
       if key_is_single_quoted == False:
          multiple_key_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}:"
          multiple_key = re.search(multiple_key_pattern, m).group() 
       
 
       # removing single quote and colon
       multiple_key_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}"
       multiple_key = re.search(multiple_key_pattern, multiple_key).group()
             
       dictionary[multiple_key] = ""
             
       multiple_values_pattern = "(?:\'[0-9]{1," + str(len(str(image_width * image_height))) + "}\',\s{1})+\'[0-9]{1," + \
                                          str(len(str(image_width * image_height))) + "}\'\]"
       
       multiple_values = re.search(multiple_values_pattern, m ).group()
      
       # getting only numbers
       multiple_values_pattern = "[0-9]{1," + str(len(str(image_width * image_height))) + "}"
       multiple_values_list = re.findall(multiple_values_pattern, multiple_values )    
       
       dictionary[multiple_key] = multiple_values_list
       
    return dictionary
       
       














