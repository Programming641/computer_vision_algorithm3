# find small pixel count shapes neighbors
from libraries import pixel_functions, image_functions, read_files_functions

from PIL import Image
import os, sys
import pickle
import copy

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir

image_filename = '12'
directory = "videos/street3/resized/min"

shapes_type = "intnl_spixcShp"

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_spixcShp_Dnbr_sharing_Lshapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'


spixcShp_w_same_Lshapes_dir = top_shapes_dir + directory + "spixc_shapes/same_Lshapes/" + shapes_type + "/"
spixcShp_w_same_Lshapes_dfile = spixcShp_w_same_Lshapes_dir + "data/" + image_filename + ".data"

spixcShp_w_same_Lshapes_imdir = spixcShp_w_same_Lshapes_dir + image_filename + "/"

if os.path.exists(spixcShp_w_same_Lshapes_imdir ) == False:
   os.makedirs(spixcShp_w_same_Lshapes_imdir)


with open (spixcShp_w_same_Lshapes_dfile, 'rb') as fp:
   # { '45414': [['45829',...], {'55023', ...}], ... }
   # { 'spixc_shapeid': [ [ list of spixc_shapes that share the same Lshapes ], { shared large shapes } ], ... }
   spixcShp_w_same_Lshapes = pickle.load(fp)
fp.close()


for spixcShpid in spixcShp_w_same_Lshapes:

   cur_shapes = [ spixcShpid ]
   
   cur_shapes.extend( spixcShp_w_same_Lshapes[ spixcShpid ][0] )
   
   for Lshape in spixcShp_w_same_Lshapes[spixcShpid][1]:
      cur_shapes.append( Lshape )
   
   save_filepath = spixcShp_w_same_Lshapes_imdir + spixcShpid + ".png"
   
   image_functions.cr_im_from_shapeslist2( image_filename, directory, cur_shapes, save_filepath=save_filepath , shapes_rgb=( 0, 0, 255 ) )






















