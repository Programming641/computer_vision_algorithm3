
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, shapes_results_functions, pixel_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir, styLshapes_wo_pixch, spixc_shapes, internal
import pickle
import sys, os

im1file = "14"
im2file = "15"
directory = "videos/street3/resized/min"

shapes_type = "intnl_spixcShp"

if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"

   print("execute script algorithms/styLshapes/verify_styLshp_wo_pixch.py file1 " + im1file + " file2 " + im2file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"
staying_Lshapes_wo_pixch_dfile = staying_Lshapes_Ddir + im1file + "." + im2file + ".data"
with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
   # [ ['3380', '3790', ['2989', '2988', ... ] ], ... ]
   # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
   styLshapes_wo_pixch = pickle.load(fp)
fp.close()


original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size

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


verified_shapes = shapes_results_functions.verify_matches( styLshapes_wo_pixch, [ im1shapes, im2shapes ], [ im1shapes_colors, im2shapes_colors ],
                  [ im1shapes_neighbors, im2shapes_neighbors ], original_image.size, min_colors )


with open(staying_Lshapes_Ddir + im1file + "." + im2file + "verified.data", 'wb') as fp:
   pickle.dump(verified_shapes, fp)
fp.close()
























