# find shapes with their most pixels changed
from libraries import pixel_functions

from PIL import Image
import math
import os, sys
import pickle

from libraries.cv_globals import top_shapes_dir


main_filename = "15"
image_filename = '14'
image_filename2 = "15"

directory = "videos/street3/resized/min"


if len(sys.argv) >= 2:
   # excluding .png extension 
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   image_filename2 = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   main_filename = sys.argv[2][0: len( sys.argv[2] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"
   
   print("execute find_mid_changed_shapes_matches.py " + directory + " " + image_filename + " " + main_filename )


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_ddir = top_shapes_dir + directory + "pixch/data/"
pixch_dfile = pixch_ddir  + image_filename + "." + image_filename2 + ".data"
with open (pixch_dfile, 'rb') as fp:
   pixch = pickle.load(fp)
fp.close()

shapes_w_intnl_spixcShp_dfile = top_shapes_dir + directory + "shapes/intnl_spixcShp/data/" + main_filename + "shapes.data"
with open (shapes_w_intnl_spixcShp_dfile, 'rb') as fp:
   # { "shapeid": [ pixel indexes ], ... }
   image_shapes = pickle.load(fp)
fp.close()

pixch_shapes = []

for shapeid in image_shapes:
   pixch_pixels = [ pixel for pixel in image_shapes[shapeid] if pixel in pixch ]
   
   if len( pixch_pixels ) > len( image_shapes[shapeid] ) * 0.8:
      pixch_shapes.append( shapeid )


pixch_shapes_file = pixch_ddir + image_filename + "." + image_filename2 + "." + main_filename + "most_ch.data"
with open(pixch_shapes_file, 'wb') as fp:
   pickle.dump(pixch_shapes, fp)
fp.close()





