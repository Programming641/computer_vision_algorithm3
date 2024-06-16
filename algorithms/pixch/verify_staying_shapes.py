
from libraries import pixel_functions, pixel_shapes_functions, shapes_results_functions, btwn_amng_files_functions

from PIL import Image
import math
import os, sys
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal

im1file = '14'
im2file = "15"

directory = "videos/street3/resized/min"

if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]

   print("execute script algorithms/pixch/verify_staying_shapes.py. file1 " + im1file + " file2 " + im2file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

pixch_dir = top_shapes_dir + directory + "pixch/"
pixch_sty_shapes_dir = pixch_dir + "sty_shapes/"
sty_shapes_ddir = pixch_sty_shapes_dir + "data/"

sty_shapes1_dfile = sty_shapes_ddir + im1file + "." + im2file + "." + im1file + ".data"
sty_shapes2_dfile = sty_shapes_ddir + im1file + "." + im2file + "." + im2file + ".data"

with open (sty_shapes1_dfile, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   sty_shapes1 = pickle.load(fp)
fp.close()

with open (sty_shapes2_dfile, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   sty_shapes2 = pickle.load(fp)
fp.close()

all_staying_shapes = set()
for sty_shape in sty_shapes1:
   all_staying_shapes.add( sty_shape )
for sty_shape in sty_shapes2:
   all_staying_shapes.add( sty_shape )

print( len( all_staying_shapes ) )

shapes_dir = top_shapes_dir + directory + "shapes/"
shapes_dfile = shapes_dir + im1file + "shapes.data"
im2shapes_dfile = shapes_dir + im2file + "shapes.data"

with open (shapes_dfile, 'rb') as fp:
   # { '79999': ['79999', ... ], ... }
   # { 'shapeid': [ pixel indexes ], ... }
   im1shapes = pickle.load(fp)
fp.close()   

with open (im2shapes_dfile, 'rb') as fp:
   # { '79999': ['79999', ... ], ... }
   # { 'shapeid': [ pixel indexes ], ... }
   im2shapes = pickle.load(fp)
fp.close()


shape_neighbors_file = shapes_dir + "shape_nbrs/" + im1file + "_shape_nbrs.data"
im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + im2file + "_shape_nbrs.data"

with open (shape_neighbors_file, 'rb') as fp:
   im1shapes_neighbors = pickle.load(fp)
fp.close()

with open (im2shape_neighbors_file, 'rb') as fp:
   im2shapes_neighbors = pickle.load(fp)
fp.close()

if "min" in directory:
   min_colors = True
else:
   min_colors = False

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, min_colors=min_colors)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, min_colors=min_colors)


verified_matches = shapes_results_functions.verify_matches( all_staying_shapes, [ im1shapes, im2shapes ], [ im1shapes_colors, im2shapes_colors ], 
                   [ im1shapes_neighbors, im2shapes_neighbors ], original_image.size, min_colors  )



print( len( verified_matches ) )


with open(sty_shapes_ddir + im1file + "." + im2file + "verified.data", 'wb') as fp:
   pickle.dump(verified_matches, fp)
fp.close()



