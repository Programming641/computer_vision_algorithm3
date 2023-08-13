
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


consecutives_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutives/data/"
consecutives_dfile = consecutives_ddir + "2.data"
with open (consecutives_dfile, 'rb') as fp:
   consecutive_shapes = pickle.load(fp)
fp.close()


consecutives_dir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutives/images2/"
# delete and create folder
if os.path.exists(consecutives_dir) == True:
   shutil.rmtree(consecutives_dir)
os.makedirs(consecutives_dir)

each_consecutives_counter = 1
for each_consecutives in consecutive_shapes:
   
   for filename, shapes in each_consecutives.items():

      im1file = filename.split(".")[0]
      im2file = filename.split(".")[1]
      
      save_im1fpath = consecutives_dir + str( each_consecutives_counter ) + "_" + im1file + "." + im2file + ".png"
      save_im2fpath = consecutives_dir + str( each_consecutives_counter ) + "_" + im1file + "." + im2file + "im2.png"
   
      for each_shapes in shapes:

         image_functions.cr_im_from_shapeslist2( im1file, directory, [each_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
         image_functions.cr_im_from_shapeslist2( im2file, directory, [each_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )    


   
   each_consecutives_counter += 1












