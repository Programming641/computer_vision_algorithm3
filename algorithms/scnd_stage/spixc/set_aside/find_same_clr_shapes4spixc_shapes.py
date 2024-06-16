# find same color shapes for smal pixel count shapes.
from libraries import pixel_functions, image_functions

from PIL import Image
import math
import os, sys
import pickle

from collections import OrderedDict
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
from libraries import pixel_shapes_functions
from libraries import pixel_functions


image_filename = '25'

directory = "videos/giraffe/min"

recreate_images = False

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_same_clr_shapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'


same_colors_dir = top_shapes_dir + directory + "s_pixc_shapes/same_clr_shapes/"
same_colors_file = same_colors_dir + image_filename + ".data"


if os.path.exists(same_colors_dir ) == False:
   os.makedirs(same_colors_dir)


# getting small pixel count shapes
pix_counts_w_shapes = image_functions.get_image_stats( image_filename, directory )

small_pixc_shapes = []
for pixel_count in pix_counts_w_shapes:

   if pixel_count <= 13:
      small_pixc_shapes.extend( pix_counts_w_shapes[ pixel_count ] )




orig_image = Image.open(top_images_dir + directory + image_filename + ".png" )
orig_pixels = orig_image.getdata()
im_width, im_height = orig_image.size

# shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }
shapes_colors = pixel_shapes_functions.get_all_shapes_colors( image_filename, directory )

# same_clr_shapes[shapeid] = { "shapeids": [ shapeid1, shapeid2,... ], "rgb": ( r, g, b ) }
same_clr_shapes = {}


# to store shapes that are already put into some shape
already_putinto_shapes = []
for shapeid in small_pixc_shapes:
   if shapeid in already_putinto_shapes:
      continue
   
   same_clr_shapes[shapeid] = { "shapeids": [], "rgb": ( shapes_colors[shapeid]["r"], shapes_colors[shapeid]["g"], shapes_colors[shapeid]["b"] ) }
   same_clr_shapes[shapeid]["shapeids"].append( shapeid )
   
   already_putinto_shapes.append( shapeid )
   
   for ano_shapeid in small_pixc_shapes:
      if ano_shapeid in already_putinto_shapes:
         continue
      
      clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(shapes_colors[shapeid] ,
                                                 shapes_colors[ano_shapeid], 30 )


      # color did not change and brightness is within threshold
      if not clrch and brit_thres :
         same_clr_shapes[shapeid]["shapeids"].append( ano_shapeid )

         already_putinto_shapes.append( ano_shapeid )


with open(same_colors_file, 'wb') as fp:
   pickle.dump(same_clr_shapes, fp)
fp.close()







































