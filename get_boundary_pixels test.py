from PIL import Image
from libraries import pixel_shapes_functions
import math

filename = "hanger001_color_group"

directory = ""

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


original_image = Image.open("images/" + directory + filename + ".png")

image_width, image_height = original_image.size











pixel_ids_list = [20085]









shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(pixel_ids_list, filename, directory)


pixels = {}
pixel_counter = 1

for shape_id in shapeIDs_with_all_indexes:



    for pixel_index in shapeIDs_with_all_indexes[shape_id]: 
    
    
       pixel_index = int(pixel_index)
       
       y = math.floor(pixel_index / image_width)

       x  = pixel_index % image_width


       pixels[pixel_counter] = {}
       pixels[pixel_counter] ['x'] = x
       pixels[pixel_counter] ['y'] = y

       pixel_counter += 1

# returned_val has the following form
# {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, 16679: {'x': 178, 'y': 229}}
# containing coordinates of boundary pixels
returned_val = pixel_shapes_functions.get_boundary_pixels(pixels)

print(returned_val)

# for boundary testing
b_filename = "20085"
b_directory = "boundary_test"


# b_directory is specified but does not contain /
if b_directory != "" and b_directory.find('/') == -1:
   b_directory +='/'


image_original = 'images/' + b_directory + b_filename + '.png'


read_original_image = Image.open(image_original)


for key in returned_val:

   read_original_image.putpixel( (returned_val[key]['x'], returned_val[key]['y']) , (255, 0, 0) )

read_original_image.save("images/" + b_directory + b_filename + "_boundary.png")













