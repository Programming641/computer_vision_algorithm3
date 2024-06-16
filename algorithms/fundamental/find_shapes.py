#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#
from libraries import pixel_functions, pixel_shapes_functions

from PIL import Image
import math
import os, sys
import pickle

from collections import OrderedDict
from libraries.cv_globals import top_shapes_dir, top_images_dir


image_filename = '25'
directory = "videos/street3/resized/min1/"

if len(sys.argv) >= 2:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_shapes.py. filename " + image_filename + " directory " + directory )


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

dir_names = directory.split("/")
# example "videos/street6/resized/min3/". last one is empty. one forward from the last is min3
lowest_dirname = dir_names[ len( dir_names ) - 2 ]
clrgrp_type = lowest_dirname


original_image = Image.open(top_images_dir + directory + image_filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size


# shapes[shape's index value ] = [ pixel index1, pixel index2, .... ]
shapes = OrderedDict()

# [ { pixel index: shapeid }, ... ]
# already_added_pixels is divided into indexes solely for speed!
# each list index contains 1000 pixel indexes. for example, list index 0: pixel indexes up to 999. list index 1 1000 to 1999.
# list index 2 contains 2000 up to 2999. and so on.
already_added_pixels = [ ]
dividing_num = 100

# initialize already_added_pixels
total_image_pixels_len = image_size[0] * image_size[1]
index_needed_for_Alrdy_A_P = total_image_pixels_len / dividing_num
for needed_index in range( math.ceil(index_needed_for_Alrdy_A_P) ):
   already_added_pixels.append( {} )



#image_size[0] is width
for y in range(image_size[1]):
   print("\r" + "y is " + str(y), end="")

   for x in range(image_size[0]):   
   
      # converting for the getdata(). y is the row that you want to get data for. current_pixel_index is the current pixel's index number
      current_pixel_index = (y * image_size[0])+ x    

      # initializing current pixel' shape number
      current_shape_id = None
      
      # this is needed for checking if pixel has same color with every pixels in the confirmed shapes
      cur_shape_containing_confirmed_shapes = None
      
      cur_pixel_neighbors = pixel_functions.get_nbr_pixels(current_pixel_index, image_size)      

      # check if current pixel is in other pixel's shapes.
      already_added_pix_index = math.floor( current_pixel_index / dividing_num ) 
      if already_added_pixels[already_added_pix_index].get( current_pixel_index ):
         # current pixel is found in existing shape. current shape will be this found shape
         current_shape_id = already_added_pixels[already_added_pix_index][ current_pixel_index ]
               
         cur_shape_containing_confirmed_shapes = shapes[ current_shape_id ]


      # current pixel was not found in all shapes so create its own shape
      if current_shape_id == None:     
         # create shape with current pixel's number as shape's id
         current_shape_id = current_pixel_index
         # make sure to put current pixel in current pixel shape
         
         shapes[current_shape_id] = [current_shape_id]
         
         already_added_pixels[already_added_pix_index][ current_shape_id ] = current_shape_id


      cur_shape_pixel_RGB = original_pixel[current_shape_id]



      # iterating each one of current pixel's neighbors
      for neighbor in cur_pixel_neighbors:
      
         neighbor_shape_index = None  
         
         cur_nbr_containing_shapes = []
         # check if this neighbor is already in the shape
         already_added_pix_index = math.floor( neighbor / dividing_num ) 
         if already_added_pixels[already_added_pix_index].get(neighbor):
                  
            # check if neighbor is already in the same shape as current_pixel_index
            neighbor_shape_index = already_added_pixels[already_added_pix_index][ neighbor ]
            if neighbor_shape_index == current_shape_id:
               break
                  
            cur_nbr_containing_shapes = shapes[ neighbor_shape_index ]            
                              


         if len(cur_nbr_containing_shapes) >= 1:
            # neighbor is found in neighbor_shape_index
            # check if all pixels in the  neighbor_shape_index have same same as current_shape_id
            # merge two shapes only if they all have the same color
            # merging all pixels in neighbor shape into current shape

            all_pixels_same_clr = None
            for cur_nbr_containing_pixel in cur_nbr_containing_shapes:
               for cur_shape_pixel in shapes[current_shape_id]:
                  if "min" not in clrgrp_type:
                     appear_diff = pixel_functions.compute_appearance_difference(original_pixel[cur_nbr_containing_pixel] ,
                                                 original_pixel[cur_shape_pixel], 30 )
                  
                  else:
                     if original_pixel[cur_nbr_containing_pixel] != original_pixel[cur_shape_pixel]:
                        appear_diff = True
                     else:
                        appear_diff = False
                     
                  
                  if appear_diff is True:
                     # appearance changed
                     all_pixels_same_clr = False
                     break

               if all_pixels_same_clr == False:
                  break
                  
            if all_pixels_same_clr != False:

               # moving neighbor_shape_index and all its pixels to current_shape_id in already_added_pixels
               already_added_pixels[already_added_pix_index][ neighbor_shape_index ] = current_shape_id
               for pixel in shapes[ neighbor_shape_index ]:
                  already_added_pix_index = math.floor( pixel / dividing_num ) 
                  already_added_pixels[already_added_pix_index][ pixel ] = current_shape_id

               shapes[current_shape_id].extend(shapes[neighbor_shape_index])
               
               shapes.pop(neighbor_shape_index)



         if cur_shape_containing_confirmed_shapes:
            neighbor_pixel_RGB = original_pixel[neighbor]

            # make sure all pixels have same color as neighbor, then you can put neighbor in current_shape_id shape
            all_pixels_same_clr = None
            for pixel in cur_shape_containing_confirmed_shapes:
               if "min" not in clrgrp_type:
                  appear_diff = pixel_functions.compute_appearance_difference(original_pixel[pixel], neighbor_pixel_RGB, 30 )
               else:
                  if original_pixel[pixel] != neighbor_pixel_RGB:
                     # appearance changed
                     appear_diff = True
                  else:
                     appear_diff = False
                  
               if appear_diff is True:
                  # appearance changed
                  all_pixels_same_clr = False
                  break
               
            if all_pixels_same_clr != False:
                  
               # neighbor pixel will be added to current shape
               shapes[current_shape_id].append(neighbor)    

               already_added_pix_index = math.floor( neighbor / dividing_num ) 
               already_added_pixels[already_added_pix_index][ neighbor ] = current_shape_id                  
            


target_im_shapes_dir = top_shapes_dir + directory + "shapes/"
if os.path.exists(target_im_shapes_dir ) == False:
   os.makedirs(target_im_shapes_dir)

with open(target_im_shapes_dir + image_filename + "shapes.data", 'wb') as fp:
   pickle.dump(shapes, fp)
fp.close()


pixel_shapes_functions.create_shapeids_by_pindex( image_filename, directory, image_size )












