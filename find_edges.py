#
# algorithm for determining the closest match with the color group uses how far away the RGB value is from original
#
#
from libraries import pixel_functions

from PIL import Image
import math
import os, sys

from collections import OrderedDict
from libraries.cv_globals import proj_dir

shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"

image_filename = 'bird01clrgrp'

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


if os.path.exists(shapes_dir + directory ) == False:
   os.makedirs(shapes_dir + directory )
   
   

original_image = Image.open(images_dir + directory + image_filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size

edge_image = Image.open(images_dir + directory + image_filename + ".png")

debug = False

#image_size[0] is width
for y in range(image_size[1]):
   print("y is " + str(y))


   for x in range(image_size[0]):
   
   
      # converting for the getdata(). y is the row that you want to get data for. current_pixel_index is the current pixel's index number
      current_pixel_index = (y * image_size[0])+ x

      
      cur_pixel_neighbors = pixel_functions.get_nbr_pixels(current_pixel_index, image_size)      



      # iterating each one of current pixel's unfound neighbors
      for neighbor in cur_pixel_neighbors:
         
            
         
         neighbor_x = neighbor % image_size[0]
         neighbor_y = math.floor( neighbor / image_size[0])

         clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(original_pixel[current_pixel_index] ,
                                                 original_pixel[neighbor], 50, clr_thres=50 )
                                                 
                  
         # color changed is true
         if clrch :
            edge_image.putpixel( ( neighbor_x, neighbor_y ) , (255, 0, 0) )
            
            
               
         
         else:
         
            # this neighbor stayed but maybe this neighbor's neighbor may have rapid change
            nested_nbrs = pixel_functions.get_nbr_pixels(neighbor, image_size)
            
            
            for nested_nbr in nested_nbrs:
               if not nested_nbr in cur_pixel_neighbors or nested_nbr != current_pixel_index:
                  
                  clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(original_pixel[current_pixel_index] ,
                                                 original_pixel[nested_nbr], 50, clr_thres=50 )
                  
                                                 
                  if clrch or ( not brit_thres ):
                  
                     nested_nbr_x = nested_nbr % image_size[0]
                     nested_nbr_y = math.floor( nested_nbr / image_size[0])
                  
                     edge_image.putpixel( ( nested_nbr_x, nested_nbr_y ) , (255, 0, 0) )

                  
         if debug:
            sys.exit()            


edge_image.save("test.png")








