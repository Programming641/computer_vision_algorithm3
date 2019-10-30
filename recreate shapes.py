import re
import math
import os

from PIL import Image

'''
this module serves 2 purposes. One is to recreate the each shape of the image. Another purpose is to return xy coordinate values of the each 
shape to the caller. If parameter is true then, it is a request to return xy coordinates of all image shapes

2nd parameter, shape_id_in_need is a list that contains all shapes that fell in the mouse circled area.
'''
def get_whole_image_shape(parameter, shape_id_in_need=None):


    shapes_filename = "easy image to analyze for practice shapes.txt"

    # shapes file has the rule for its filename. Its filename consists of name of the image shape + shapes.txt.
    # so to extract the shapes image name only, you just remove last space + shapes.txt
    original_image_filename = shapes_filename[:-11]

    if os.path.exists("shapes/" + shapes_filename[:-4]) == False:
       os.mkdir("shapes/" + shapes_filename[:-4])

    # this is for object shapes which is mouse circled image shapes
    foldername = ""
    if shape_id_in_need != None:
       foldername = "objectshape/"
       if os.path.exists("shapes/objectshape/" + shapes_filename[:-4]) == False:
          os.mkdir("shapes/objectshape/" + shapes_filename[:-4])





    original_image = Image.open("images/" + original_image_filename + ".png")

    image_width, image_height = original_image.size

    original_image_data = original_image.getdata()



    shapes_file = open("shapes/" + shapes_filename)
    shapes_file_contents = shapes_file.read()


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

    shapes = {}

    shape_progress_counter = 0
    # match contains all shapes
    for shape in match:

       if parameter == False:
          new_image = Image.new('RGB', (image_width, image_height) )

       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       shapes_id = match_temp.group().strip('(,')
 
       # it is a request to create shapes that fell inside the mouse circled area but the current running shape is not 
       # inside the mouse circled area
       if shape_id_in_need != None and not str(shapes_id) in shape_id_in_need:
          continue
          


 
       pixels_list_pattern = '\[.*\]'
       pixels_index_string = re.findall(pixels_list_pattern, shape)




       shape_pixel_counter = 0 
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
             shape_pixel_counter += 1
             pixel_index = int(pixel_index)
         
             original_image_red, original_image_green, original_image_blue, alpha = original_image_data[pixel_index ]
             y = math.floor(pixel_index / image_width)
             x  = pixel_index % image_width          
             
             if parameter == True:

                shapes[shapes_id][shape_pixel_counter] = {}
                shapes[shapes_id][shape_pixel_counter]['x'] = x
                shapes[shapes_id][shape_pixel_counter]['y'] = y

             if parameter == False:
                new_image.putpixel( (x, y) , (original_image_red, original_image_green, original_image_blue) )


          if parameter == False:
             shape_progress_counter += 1          
             print("shape " + str(shape_progress_counter))  
             
             # saving one shape
             new_image.save("shapes/" + foldername + shapes_filename[:-4] + '/' + shapes_id + '.png')
      
    shapes_file.close() 
    
    if parameter == True:
       return shapes 




if __name__ == '__main__':
   get_whole_image_shape(False)
