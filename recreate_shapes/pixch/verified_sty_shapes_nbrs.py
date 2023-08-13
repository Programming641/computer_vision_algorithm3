
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

sty_shapes_dir = top_shapes_dir + directory + pixch_sty_dir + "/"
sty_shapes_nbrs_file = sty_shapes_dir + "data/" + filename + "." + filename2 + "nbrs.data"
with open (sty_shapes_nbrs_file, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   sty_shapes_nbrs = pickle.load(fp)
fp.close()



sty_shapes_nbrs_imdir = sty_shapes_dir + filename + "." + filename2 + "nbrs/"
# delete and create folder
if os.path.exists(sty_shapes_nbrs_imdir) == True:
   shutil.rmtree(sty_shapes_nbrs_imdir)
os.makedirs(sty_shapes_nbrs_imdir)


for each_sty_shapes in sty_shapes_nbrs:
   # [ [ im1shapeid, im1neighbor ], [ im2shapeid, im2neighbor ] ]
   
   save_im1fpath = sty_shapes_nbrs_imdir + each_sty_shapes[0][0] + "." + each_sty_shapes[1][0] + "im1.png"
   image_functions.cr_im_from_shapeslist2( filename, directory, [each_sty_shapes[0][1]], save_filepath=save_im1fpath , shapes_rgb=(255,0,0) )

   save_im2fpath = sty_shapes_nbrs_imdir + each_sty_shapes[0][0] + "." + each_sty_shapes[1][0] + "im2.png"
   image_functions.cr_im_from_shapeslist2( filename2, directory, [each_sty_shapes[1][1]], save_filepath=save_im2fpath , shapes_rgb=(0,0,255) )















