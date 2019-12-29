import re
from PIL import Image
import os
import read_files_functions






filename = "birdcopy face color group"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'

same_color_pairs_foldername = filename + " same color pairs"



# if the folder does not exists, create it
if os.path.exists("shapes/objectshape/" + same_color_pairs_foldername) == False:
   os.mkdir("shapes/objectshape/" + same_color_pairs_foldername)

same_color_pairs_path = "shapes/objectshape/" + same_color_pairs_foldername + "/" + filename


original_image = Image.open("images/" + directory + filename + ".png")

image_width, image_height = original_image.size

original_image_data = original_image.getdata()



same_color_pairs = read_files_functions.read_same_color_pairs_file(filename, directory)

# we need to get every pixel of the shapes
# return value form is
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapes_pixels = read_files_functions.read_shapes_file(filename, directory)

file_counter = 1

for key in same_color_pairs:

   # not processing single pair shapes/
   if len(same_color_pairs[key]) <= 1:
      continue
      
   # creating new image for every same color pairs
   new_image = Image.new('RGB', (image_width, image_height) )

   # pair is each pair of multiple pairs of the same colors
   # example ['8240', '8354']
   for pair in same_color_pairs[key]:
      # getting first shape index id of pair
      shape_index1 = pair[0]
      # getting second shape index id of pair
      shape_index2 = pair[1]  


      # we now have index values of the current shape pair.
      # for recreating image with same colors, we will get all pixels of the shapes
      
      for image_shape_id in shapes_pixels:
      
         if shape_index1 == image_shape_id:
            # first getting all pixels of first shape of the pair
            for pixel_index in shapes_pixels[image_shape_id]:
         
               # getting pixel's rgb
               x = shapes_pixels[image_shape_id][pixel_index]['x']
               y = shapes_pixels[image_shape_id][pixel_index]['y']             
               
               r, g, b, a = original_image_data[int(pixel_index)]
               
               new_image.putpixel( (x, y) , (r, g, b) )

      for image_shape_id in shapes_pixels:
      
         if shape_index2 == image_shape_id:
            # first getting all pixels of first shape of the pair
            for pixel_index in shapes_pixels[image_shape_id]:
         
               # getting pixel's rgb
               x = shapes_pixels[image_shape_id][pixel_index]['x']
               y = shapes_pixels[image_shape_id][pixel_index]['y']             
               
               r, g, b, a = original_image_data[int(pixel_index)]
               
               new_image.putpixel( (x, y) , (r, g, b) )


   new_image.save(same_color_pairs_path + str(file_counter) + ".png")

   file_counter += 1










































