
import math
from statistics import mean
from PIL import Image
import pixel_shapes_functions

filename = "bird01 color group"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


image_original = 'images/' + directory + filename + '.png'

read_original_image = Image.open(image_original)


read_new_image = Image.open('shapes/objectshape/' + filename + ' shape.png')

image_width, image_height = read_original_image.size

image_pixels = read_original_image.getdata()

image_file = open('shapes/objectshape/' + filename + ' matched shape ids.txt')
image_file_contents = image_file.read()



# removing single quote, brackets and space
pixel_indexest_string = image_file_contents.replace('\'', '') 
pixel_indexest_string = pixel_indexest_string.strip('[]')
pixel_indexest_string = pixel_indexest_string.replace(' ', "")

# list with all matched shape ids
pixel_indexes = pixel_indexest_string.split(',')

shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(pixel_indexes, filename, directory)
   
print(str(shapeIDs_with_all_indexes) + "\n\n\n")


# this is for finding above or below neighbor pixels. 
above_below_neighbor_threshold = 5




for shape_id in shapeIDs_with_all_indexes:
    shapeIDs_with_all_indexes[shape_id].sort()
    print(shapeIDs_with_all_indexes[shape_id])
    
    # storing missing numbers. initializing for each shape
    missing_pixel_indexes = []
    
    # storing RGB values for each shape. Initializing for each shape
    Red = []
    Green = []
    Blue = []
    
    
    first = True
    for current_pixel_index in shapeIDs_with_all_indexes[shape_id]:

        current_pixel_index = int(current_pixel_index)
        
        r, g, b, a = image_pixels[ current_pixel_index ]
        Red.append(r)
        Green.append(g)
        Blue.append(b)
        
        if first == True:
           previous_pixel_index = current_pixel_index
           first = False
           continue

        '''
        numbers are sorted, so if there is no missing pixels then current number is previous pixel + 1
        all numbers here are in the same shape, so pixels can be above or below pixels. If there is no
        missing pixels but it is above or below, the current number should have jumped quite alot from
        previous number. The amout of jump depends on image width and the amount of pixels in the current
        individual shape. If current individual shape contains large amounts of pixels, the current pixel
        maybe far end of the shape.
        '''
        if current_pixel_index - previous_pixel_index != 1 and current_pixel_index - previous_pixel_index < above_below_neighbor_threshold:

           # example. current 103 previous 100
           # 103 - 100 - 1 = 2 numbers missing
           missing_number_amount = current_pixel_index - previous_pixel_index - 1
           
           # range exclude last number
           for i in range(1, missing_number_amount + 1):
              missing_pixel_indexes.append(previous_pixel_index + i)

           

        
        previous_pixel_index = current_pixel_index
        

    print("missing pixel indexes are " + str(missing_pixel_indexes))

        
    # we now have missing pixels. Next is to fill it with RGB value that most pixels in the same shape have.
    # because all pixels in the same shape have similar appearance with threshold constraint, it is probably just ok to
    # get average value for RGBs

    if not missing_pixel_indexes == "":
       # getting average RGB for all pixels in each shape
       r = round(mean(Red))
       g = round(mean(Green))
       b = round(mean(Blue))
       
       for missing_pixel_index in missing_pixel_indexes:
          
          y = math.floor(missing_pixel_index / image_width)
       
          x  = missing_pixel_index % image_width
       
          read_new_image.putpixel( (x, y) , (r, g, b) )


          read_new_image.save('shapes/objectshape/' + filename + ' shape test.png')
       


