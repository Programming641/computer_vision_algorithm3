# find shapes with their most pixels changed
from libraries import pixel_functions, btwn_amng_files_functions

from PIL import Image
import math
import os, sys
import pickle

from libraries.cv_globals import top_shapes_dir


main_filename = "2"
image_filename = '1'
image_filename2 = "2"

directory = "videos/street6/resized/min3"


if len(sys.argv) >= 2:
   # excluding .png extension 
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   image_filename2 = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   main_filename = sys.argv[2][0: len( sys.argv[2] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"
   
   print("execute find_pixch_shapes.py " + directory + " " + image_filename + " " + main_filename )


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_ddir = top_shapes_dir + directory + "pixch/data/"
pixch_dfile = pixch_ddir  + image_filename + "." + image_filename2 + ".data"
with open (pixch_dfile, 'rb') as fp:
   pixch = pickle.load(fp)
fp.close()

shapes_dfile = top_shapes_dir + directory + "shapes/" + main_filename + "shapes.data"
with open (shapes_dfile, 'rb') as fp:
   # { "shapeid": [ pixel indexes ], ... }
   image_shapes = pickle.load(fp)
fp.close()

# { shapeid: { pixch pindexes }, ... }
pixch_shapes = {}
most_pixch_shapes = []

for shapeid in image_shapes:
   pixch_pixels = { pixel for pixel in image_shapes[shapeid] if pixel in pixch }
   
   if len( pixch_pixels ) >= len( image_shapes[shapeid] ) * 0.8:
      # 80% or more pixels have changed
      most_pixch_shapes.append( shapeid )

   pixch_shapes[ shapeid ] = pixch_pixels


pixch_shapes_file = pixch_ddir + image_filename + "." + image_filename2 + "." + main_filename + "pixch_shapes.data"
with open(pixch_shapes_file, 'wb') as fp:
   pickle.dump(pixch_shapes, fp)
fp.close()

pixch_shapes_file = pixch_ddir + image_filename + "." + image_filename2 + "." + main_filename + "most_ch.data"
with open(pixch_shapes_file, 'wb') as fp:
   pickle.dump(most_pixch_shapes, fp)
fp.close()



