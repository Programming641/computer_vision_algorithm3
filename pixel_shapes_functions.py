import re
from PIL import Image

# returns all pixel shape ids with indexes
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




