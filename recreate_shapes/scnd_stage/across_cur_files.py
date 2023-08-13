
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
im1file = "14"
im2file = "15"
# if target directory is shape_nbrs_matches, make target_dir emtpy, 
# if it's for only_nfnd_pixch_sty. write "/only_nfnd_pixch_sty/" in target_dir
target_dir = "/only_nfnd_pixch_sty2/"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
across_all_files_dfile = across_all_files_ddir + im1file + "." + im2file + ".data"
with open (across_all_files_dfile, 'rb') as fp:
   # { ('1270', '2072'), ('2062', '2062'), ... }
   # { ( image1 shapeid, image2 shapeid ), ... }
   acrs_cur_files_shapes = pickle.load(fp)
fp.close()


across_all_files_imdir = top_shapes_dir + directory + scnd_stg_all_files + "/" + im1file + "." + im2file + "/"
# delete and create folder
if os.path.exists(across_all_files_imdir) == True:
   shutil.rmtree(across_all_files_imdir)
os.makedirs(across_all_files_imdir)


for each_shapes in acrs_cur_files_shapes:
   # each_shapes -> ('30115', '27323')

   save_im1fpath = across_all_files_imdir + each_shapes[0] + "." + each_shapes[1] + "im1.png"
   image_functions.cr_im_from_shapeslist2( im1file, directory, [each_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
   
   save_im2fpath = across_all_files_imdir + each_shapes[0] + "." + each_shapes[1] + "im2.png"

   image_functions.cr_im_from_shapeslist2( im2file, directory, [each_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )  






















