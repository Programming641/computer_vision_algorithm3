from PIL import Image
import os
import pixel_shapes_functions
import read_files_functions

image_filename = "office outside color group"
image_directory = ""

shapes_colors_foldername = image_filename + " same color shapes"

# if the folder does not exists, create it
if os.path.exists("shapes/objectshape/" + shapes_colors_foldername) == False:
   os.mkdir("shapes/objectshape/" + shapes_colors_foldername)

shapes_colors_path = "shapes/objectshape/" + shapes_colors_foldername + "/" + image_filename

# shapes_colors holds one RGB color for every shape of the image
# form is shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }
shapes_colors = pixel_shapes_functions.get_shapes_colors(image_filename, image_directory)

# this is for storing all shapes of the image sorted by same colors
# the form is...
# same_color_shapes[same_color_shape_id] = {'RGB': {'r': 100, 'g':200, 'b': 50}, 'shape_ids': [same_color_shape_id, shape_id1, shape_id2, ......] }
# same_color_shape_id is the first shape that is encountered in the processing of finding the same color shapes
same_color_shapes = {}


# now that we have every shape's colors, we will recreate the image based on the same color

# we will look for the shapes that have the color with each one of the shapes
# We will accomplish that by putting current running shape in the outer loop and compare it
# with every shape of the image.
for current_running_shape_id in shapes_colors:
   same_color_shape_contains = False
   remove_current_shape = False

   same_color_shapes[current_running_shape_id] = {}
   same_color_shapes[current_running_shape_id]['RGB'] = {'r': shapes_colors[current_running_shape_id]['r'], 'g': shapes_colors[current_running_shape_id]['g'], \
                                                        'b': shapes_colors[current_running_shape_id]['b']}
   same_color_shapes[current_running_shape_id]['shape_ids'] = []

   # first, make sure that current running shape is not already in the same_color_shapes
   # if it is already in some same_color_shapes then, delete current shape and skip this shape and move onto next shape
   for shape_id in same_color_shapes:
      if  current_running_shape_id in same_color_shapes[shape_id]['shape_ids']:
         same_color_shape_contains = True
         remove_current_shape = True
         
   if remove_current_shape == True:
      same_color_shapes.pop(current_running_shape_id)

   if same_color_shape_contains == True:
      continue


   current_running_shape_rgb = [ shapes_colors[current_running_shape_id]['r'] ]
   current_running_shape_rgb.append(shapes_colors[current_running_shape_id]['g'])
   current_running_shape_rgb.append(shapes_colors[current_running_shape_id]['b'])
   
   for compare_shape_id in shapes_colors:
   
      # getting comparing shape's rgb values in the python list for performing comparison with current running shape
      compare_shape_rgb = [ shapes_colors[compare_shape_id]['r'] ]
      compare_shape_rgb.append(shapes_colors[compare_shape_id]['g'])
      compare_shape_rgb.append(shapes_colors[compare_shape_id]['b'])

      # now we compare two shapes to see if they have the same colors
      if current_running_shape_rgb == compare_shape_rgb:
         # current running shape and comparing shape have the exact same color.
         # now, we need to put both shapes in the same list
         same_color_shapes[current_running_shape_id]['shape_ids'].append(compare_shape_id)
        
print(" read shapes file ")
# we need to get every pixel of the shapes
shapes_pixels = read_files_functions.read_shapes_file(image_filename, image_directory)
print(" shapes file read")


original_image = Image.open("images/" + str(image_directory) + image_filename + ".png")

image_width, image_height = original_image.size

shapes_colors_file_counter = 1

shapes_id_test = []
pixel_counter_test = 0



for same_color_shapes_id in same_color_shapes:
   # outer loop is to loop through every same color shapes

   # create new image for the same color shapes that contain every shape that has the same color
   new_image = Image.new('RGBA', (image_width, image_height) )

   # this loop is to loop through every shapes that have the same color as the current running same_color_shapes_id
   for same_color_shape_ids in same_color_shapes[same_color_shapes_id]['shape_ids']:
      r = same_color_shapes[same_color_shapes_id]['RGB']['r']
      g = same_color_shapes[same_color_shapes_id]['RGB']['g']
      b = same_color_shapes[same_color_shapes_id]['RGB']['b']
      
      # this loop is to get every pixel of the every shape in the current running same_color_shapes_id
      for shape_id in shapes_pixels:

         if same_color_shape_ids == shape_id:
            shapes_id_test.append(same_color_shape_ids)    
            for pixel_ids in shapes_pixels[shape_id]:
               pixel_counter_test += 1
               x = shapes_pixels[shape_id][pixel_ids]['x']
               y = shapes_pixels[shape_id][pixel_ids]['y']

               
               new_image.putpixel( (x, y) , (r, g, b) )

   new_image.save(shapes_colors_path + str(shapes_colors_file_counter) + ".png")
   shapes_colors_file_counter += 1


'''
# this is a test to see if shapes_id_test contains every shape of the image
for shape_id in shapes_pixels:
   if shape_id in shapes_id_test:
      shapes_id_test.remove(shape_id)
      
# if shapes_id_test does contain every shape of the image then shapes_id_test here should be empty      
print(shapes_id_test)

# this should produce same number as the image resolution
print(pixel_counter_test)
'''

















