
from libraries import image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, pixch_sty_dir
import pickle
import sys
import math
from PIL import Image


filename = "12"
filename2 = "13"
directory = "videos/street3/resized/min"

shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_sty_shapes_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
pixch_sty_shapes_file = pixch_sty_shapes_dir + "data/" +  filename + "." + filename2 + "." + filename + ".data"
with open (pixch_sty_shapes_file, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   pixch_sty_shapes1 = pickle.load(fp)
fp.close()

pixch_sty_shapes_file2 = pixch_sty_shapes_dir + "data/" +  filename + "." + filename2 + "." + filename2 + ".data"
with open (pixch_sty_shapes_file2, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   pixch_sty_shapes2 = pickle.load(fp)
fp.close()


im1file_shapes = [ shapes[0] for shapes in pixch_sty_shapes1 ]
im2file_shapes = [ shapes[1] for shapes in pixch_sty_shapes1 ]

im1file_shapes.extend( [ shapes[0] for shapes in pixch_sty_shapes2 ] )
im2file_shapes.extend( [ shapes[1] for shapes in pixch_sty_shapes2 ] )


image_functions.cr_im_from_shapeslist2( filename, directory, im1file_shapes, save_filepath=None , shapes_rgb=(255,0,0) )
image_functions.cr_im_from_shapeslist2( filename2, directory, im2file_shapes, save_filepath=None , shapes_rgb=(0,0,255) )


















