
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

across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
nbr_matches_dfile = across_all_files_ddir + "nbr_matches.data"
with open (nbr_matches_dfile, 'rb') as fp:
   nbr_matched_shapes = pickle.load(fp)
fp.close()


across_all_files_dir = top_shapes_dir + directory + scnd_stg_all_files + "/nbr_matches/"
for filename in nbr_matched_shapes:
   print( filename )

   im1file = filename.split(".")[0]
   im2file = filename.split(".")[1]
   
   across_all_files_imdir = across_all_files_dir + im1file + "." + im2file + "/"

   # delete and create folder
   if os.path.exists(across_all_files_imdir) == True:
      shutil.rmtree(across_all_files_imdir)
   os.makedirs(across_all_files_imdir)

   
   for each_file_shapes in nbr_matched_shapes[filename]:
      # each_file_shapes -> ('57125', '57529')

      result_name = each_file_shapes[0] + "." + each_file_shapes[1]
      

      save_im1fpath = across_all_files_imdir + result_name + ".png"
      image_functions.cr_im_from_shapeslist2( im1file, directory, [each_file_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )

      save_im2fpath = across_all_files_imdir + result_name + "im2.png"
      image_functions.cr_im_from_shapeslist2( im2file, directory, [each_file_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )  





















