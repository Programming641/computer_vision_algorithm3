from PIL import Image
import read_files_functions
import os

filename = "blue1 color group"

directory = "monochromatic light sources"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'

original_image = Image.open("images/" + str(directory) + filename + ".png")

image_width, image_height = original_image.size

original_image_data = original_image.getdata()


image_shapes = read_files_functions.read_shapes_file(filename, directory)

brightness_change_file = "shapes/" + filename + " with brightness change.txt"

if os.path.exists(brightness_change_file[:-4]) == False:
   os.mkdir(brightness_change_file[:-4])


brightness_change_shapes = read_files_functions.read_dict_key_value_list(filename, directory, brightness_change_file)

for brightness_shape_id in brightness_change_shapes:

   new_image = Image.new('RGB', (image_width, image_height) )

   # for some shape ids, shape id is not included in the list of all shapes with the brightness change, so include it as well 
   # then process all shapes in the list
   if not brightness_shape_id in brightness_change_shapes:
      brightness_change_shapes[brightness_shape_id].append(brightness_shape_id)
      
   # processing each of the shapes in the list
   for brightness_shape in brightness_change_shapes[brightness_shape_id]:
      
      for image_shape_id in image_shapes:

         if brightness_shape == image_shape_id:      
            # get all pixels of the current shape
            for pixel_id in image_shapes[image_shape_id]:
            
               r, g, b, alpha = original_image_data[int(pixel_id)]
               new_image.putpixel( (image_shapes[image_shape_id][pixel_id]['x'], image_shapes[image_shape_id][pixel_id]['y']) , (r, g, b) )

   # saving one shape
   new_image.save(brightness_change_file[:-4] + '/' + brightness_shape_id + '.png')






























