
import math
from PIL import Image
import pixel_shapes_functions

filename = "easy image to analyze for practice4"

directory = ""

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'






image_file = open('shapes/objectshape/' + filename + ' matched shape ids.txt')
image_file_contents = image_file.read()



# removing single quote, brackets and space
pixel_indexest_string = image_file_contents.replace('\'', '') 
pixel_indexest_string = pixel_indexest_string.strip('[]')
pixel_indexest_string = pixel_indexest_string.replace(' ', "")

# list with all matched shape ids
pixel_indexes = pixel_indexest_string.split(',')

shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(pixel_indexes, filename, directory)
   
print(shapeIDs_with_all_indexes)


image_original = 'images/' + directory + filename + '.png'

read_original_image = Image.open(image_original)

original_pixel = read_original_image.getdata()

image_width, image_height = read_original_image.size

new_image = Image.new('RGB', (image_width, image_height) )


for shape_id in shapeIDs_with_all_indexes:
    for pixel_index in shapeIDs_with_all_indexes[shape_id]: 
    
       pixel_index = int(pixel_index)
       pixel_index_R, pixel_index_G, pixel_index_B, alpha = original_pixel[ pixel_index ]

       y = math.floor(pixel_index / image_width)

       x  = pixel_index % image_width




       new_image.putpixel( (x, y) , (pixel_index_R, pixel_index_G, pixel_index_B) )


new_image.save("shapes/objectshape/" + filename + ' shape.png')

