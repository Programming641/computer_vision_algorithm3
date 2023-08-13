
from libraries import image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, pixch_sty_dir
import pickle
import sys, os
import shutil
from PIL import Image


filename = "14"
filename2 = "15"
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

pixch_ch_shapes_dir = top_shapes_dir + directory + "pixch/ch_shapes/ch_from/"
pixch_ch_shapes_file = pixch_ch_shapes_dir + "data/" + filename + "." + filename2 + "verified.data"
with open (pixch_ch_shapes_file, 'rb') as fp:
   # [[['23933', '27137'], ['13530', '27539']], ... ]
   # [ [ [ image1 shapeids ] [ image2 shapeids ] ], ... ]
   pixch_ch_shapes = pickle.load(fp)
fp.close()

pixch_ch_shapes_imdir = pixch_ch_shapes_dir + filename + "." + filename2 + "verified/"
# delete and create folder
if os.path.exists(pixch_ch_shapes_imdir) == True:
   shutil.rmtree(pixch_ch_shapes_imdir)
os.makedirs(pixch_ch_shapes_imdir)


for each_changed_shapes in pixch_ch_shapes:
   im1save_filepath = pixch_ch_shapes_imdir + each_changed_shapes[0][0] + "im1.png"
   im2save_filepath = pixch_ch_shapes_imdir + each_changed_shapes[0][0] + "im2.png"
   image_functions.cr_im_from_shapeslist2( filename, directory, each_changed_shapes[0], save_filepath=im1save_filepath , shapes_rgb=(255,0,0) )
   image_functions.cr_im_from_shapeslist2( filename2, directory, each_changed_shapes[1], save_filepath=im2save_filepath , shapes_rgb=(0,0,255) )


















