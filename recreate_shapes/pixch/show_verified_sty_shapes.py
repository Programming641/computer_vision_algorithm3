
from libraries import image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, pixch_sty_dir
import pickle
import sys, os
import shutil
from PIL import Image


filename = "24"
filename2 = "25"
directory = "videos/giraffe/resized/min"

shapes_type = "intnl_spixcShp"

sty_shapes_color = ( 0, 0, 255 )

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

sty_shapes_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
sty_shapes_file = sty_shapes_dir + "data/" + filename + "." + filename2 + "verified.data"
with open (sty_shapes_file, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   sty_shapes = pickle.load(fp)
fp.close()


im1shapes = [ shapes[0] for shapes in sty_shapes ]

image_functions.cr_im_from_shapeslist2( filename, directory, im1shapes , shapes_rgb=(255,0,0) )

im2shapes = [ shapes[1] for shapes in sty_shapes ]

image_functions.cr_im_from_shapeslist2( filename2, directory, im2shapes , shapes_rgb=(0,0,255) )



















