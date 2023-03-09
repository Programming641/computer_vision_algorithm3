
from libraries import pixel_functions

from PIL import Image
import math
import os, sys
import pickle

from collections import OrderedDict
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir


image_filename = '1'

directory = "videos/cat/min"

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_edges.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'


edge_dir = top_shapes_dir + directory + "edges/"
edge_data_dir = edge_dir + "data/"

if os.path.exists(edge_dir ) == False:
   os.makedirs(edge_dir )
if os.path.exists(edge_data_dir ) == False:
   os.makedirs(edge_data_dir )


original_image = Image.open(top_images_dir + directory + image_filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size

edge_image = Image.open(top_images_dir + directory + image_filename + ".png")

pixch = False
if pixch:
   pixch_edge_image = Image.open(top_shapes_dir + directory + "pixch/" + "pixdiff" + image_filename + "." + 
                      str(int(image_filename) + 1) + "result" + str(int(image_filename) + 1) + ".png")

#shape_ch_edge_image = Image.open(top_shapes_dir + "videos/monkey/" + "shapes_ch/" + "diff3.4result4_clrgrp.png")



edge_data = set()

debug = False

#image_size[0] is width
for y in range(image_size[1]):

   for x in range(image_size[0]):
   
   
      # converting for the getdata(). y is the row that you want to get data for. current_pixel_index is the current pixel's index number
      current_pixel_index = (y * image_size[0])+ x

      
      cur_pixel_neighbors = pixel_functions.get_nbr_pixels(current_pixel_index, image_size)      



      # iterating each one of current pixel's unfound neighbors
      for neighbor in cur_pixel_neighbors:
         
            
         
         neighbor_x = neighbor % image_size[0]
         neighbor_y = math.floor( neighbor / image_size[0])

         clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(original_pixel[current_pixel_index] ,
                                                 original_pixel[neighbor], 70, clr_thres=70 )
                                                 
                  
         
         if clrch or ( not brit_thres ) :
            # color changed is true or brightness is over threshold
            edge_image.putpixel( ( neighbor_x, neighbor_y ) , (0, 0, 255) )
            
            if pixch:
               pixch_edge_image.putpixel( ( neighbor_x, neighbor_y ) , (0, 0, 255) )
               #shape_ch_edge_image.putpixel( ( neighbor_x, neighbor_y ) , (0, 0, 255) )
            
            
            edge_data.add( neighbor )
            
            
               
         
         else:
         
            # this neighbor stayed but maybe this neighbor's neighbor may have rapid change
            nested_nbrs = pixel_functions.get_nbr_pixels(neighbor, image_size)
            
            
            for nested_nbr in nested_nbrs:
               if not nested_nbr in cur_pixel_neighbors or nested_nbr != current_pixel_index:
                  
                  clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(original_pixel[current_pixel_index] ,
                                                 original_pixel[nested_nbr], 70, clr_thres=70 )
                  
                                                 
                  if clrch or ( not brit_thres ):
                     # color changed is true or brightness is over threshold
                     nested_nbr_x = nested_nbr % image_size[0]
                     nested_nbr_y = math.floor( nested_nbr / image_size[0])
                  
                     edge_image.putpixel( ( nested_nbr_x, nested_nbr_y ) , (0, 0, 255) )
                     
                     if pixch:
                        pixch_edge_image.putpixel( ( neighbor_x, neighbor_y ) , (0, 0, 255) )
                        #shape_ch_edge_image.putpixel( ( neighbor_x, neighbor_y ) , (0, 0, 255) )
                     
                     edge_data.add( nested_nbr )

                  
         if debug:
            sys.exit()            
         

edge_image.save(edge_dir + image_filename + ".png" )

with open(edge_data_dir + image_filename + ".data", 'wb') as fp:
   pickle.dump(edge_data, fp)
fp.close()

if pixch:
   pixch_edge_image.save(edge_dir + "pixch" + image_filename + "." + str(int(image_filename) + 1) + ".png")
   #shape_ch_edge_image.save(edge_dir + "shapes_ch3.4.png")




