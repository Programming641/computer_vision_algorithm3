
from PIL import Image
import pickle
import math
import copy, shutil
import os, sys
from libraries.cv_globals import top_temp_dir, top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import frth_smallest_pixc, Lshape_size, third_smallest_pixc
from libraries import read_files_functions, pixel_shapes_functions, image_functions, pixel_functions, same_shapes_functions
import winsound


directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


dis_n_appeared_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/dis_n_appeared_shapes/data/"
disappeared_dfile = dis_n_appeared_ddir + "disappeared.data"
with open (disappeared_dfile, 'rb') as fp:
   disappeared_shapes = pickle.load(fp)
fp.close()     

disappeared_imdir = top_shapes_dir + directory + scnd_stg_all_files + "/dis_n_appeared_shapes/disappeared/"
# delete and create folder
if os.path.exists(disappeared_imdir) == True:
   shutil.rmtree(disappeared_imdir)
os.makedirs(disappeared_imdir)

for filename in disappeared_shapes:

   im1file = filename.split(".")[0]
   im2file = filename.split(".")[1]
   
   im1shapes = set()
   for shapeid in disappeared_shapes[filename]:
      im1shapes.add( shapeid )
   
   save_im1fpath = disappeared_imdir + filename + ".png"
   image_functions.cr_im_from_shapeslist2( im1file, directory, im1shapes, save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )      












