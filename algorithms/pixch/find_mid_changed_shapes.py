# find shapes with their most pixels changed
from libraries import pixel_functions

from PIL import Image
import math
import os, sys
import winsound
import pickle

from libraries.cv_globals import top_shapes_dir, pixch_sty_dir, frth_smallest_pixc


main_filename = "15"
image_filename = '14'
image_filename2 = "15"

directory = "videos/street3/resized/min"

# pixel change image contains pixel change color and backgound color. this is needed to exclude background color
pixch_color = ( 0, 255 , 0 )

if len(sys.argv) >= 2:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_shapes.py. filename " + image_filename + " directory " + directory )


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_ddir = top_shapes_dir + directory + "pixch/data/"
pixch_dfile = pixch_ddir  + image_filename + "." + image_filename2 + ".data"
with open (pixch_dfile, 'rb') as fp:
   # {  '34933', '3241', ... }
   pixch = pickle.load(fp)
fp.close()



shapes_w_intnl_spixcShp_dfile = top_shapes_dir + directory + "shapes/intnl_spixcShp/data/" + main_filename + "shapes.data"
with open (shapes_w_intnl_spixcShp_dfile, 'rb') as fp:
   # { "shapeid": [ pixel indexes ], ... }
   image_shapes = pickle.load(fp)
fp.close()


pixch_sty_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
pixch_sty_dfile = pixch_sty_dir + "data/" + image_filename + "." + image_filename2 + "." + main_filename + ".data"
with open (pixch_sty_dfile, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   pixch_stayed_shapes = pickle.load(fp)
fp.close()

im1_2pixch_sty_shapes = [ set(), set() ]
for each_pixch_stayed_shapes in pixch_stayed_shapes:
   im1_2pixch_sty_shapes[0].add( each_pixch_stayed_shapes[0] )
   im1_2pixch_sty_shapes[1].add( each_pixch_stayed_shapes[1] )


if main_filename == image_filename:
   pixch_sty_shp_index = 0
else:
   pixch_sty_shp_index = 1



mid_pixch_shapes = []
for shapeid in image_shapes:
   if len( image_shapes[shapeid] ) < frth_smallest_pixc:
      continue
   temp_shape = set()
   temp_shape.add( shapeid )
   found_in_sty_shp = temp_shape.intersection( im1_2pixch_sty_shapes[pixch_sty_shp_index] )
   
   if len( found_in_sty_shp ) > 0:
      continue
   
   pixch_pixels = set( image_shapes[shapeid] ).intersection( pixch )
   
   if len( pixch_pixels ) > 0 and len( pixch_pixels ) / len( image_shapes[shapeid] ) < 0.53:
      mid_pixch_shapes.append( shapeid )


pixch_shapes_file = pixch_ddir + image_filename + "." + image_filename2 + "." + main_filename + "mid_ch.data"
with open(pixch_shapes_file, 'wb') as fp:
   pickle.dump(mid_pixch_shapes, fp)
fp.close()






frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)






