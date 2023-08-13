
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
across_all_files_dfile = across_all_files_ddir + "all_files.data"
with open (across_all_files_dfile, 'rb') as fp:
   # {'10.11_11.12': [['56275', '57073', '57073', '57074'], ['61175', '40399', '', ''], ... }
   # { prev filename_cur filename: [ [ prev image1 shapeid, prev image2 shapeid, cur image1 shapeid, cur image2 shapeid ], ... ], ... }
   acrs_all_files_shapes = pickle.load(fp)
fp.close()


across_all_files_imdir = top_shapes_dir + directory + scnd_stg_all_files + "/all_files/" 
# delete and create folder
if os.path.exists(across_all_files_imdir) == True:
   shutil.rmtree(across_all_files_imdir)
os.makedirs(across_all_files_imdir)



for filename in acrs_all_files_shapes:
   prev_cur_files = filename.split("_")
   prev_im1file = prev_cur_files[0].split(".")[0]
   prev_im2file = prev_cur_files[0].split(".")[1]
   cur_im1file = prev_cur_files[1].split(".")[0]
   cur_im2file = prev_cur_files[1].split(".")[1]
   
   for each_file_shapes in acrs_all_files_shapes[filename]:
      # each_file_shapes -> ['56275', '57073', '57073', '57074']
      # if all prev and cur shapes are found, above is correct. if not, not found shapes are empty 
      # ['', '57073', '', ''] or ['', '', '5555', '11111']
      result_name = each_file_shapes[0] + "." + each_file_shapes[1] + "." + each_file_shapes[2] + "." + each_file_shapes[3]
      
      if each_file_shapes[0] != "":
         save_im1fpath = across_all_files_imdir + result_name + "." + prev_im1file + ".png"
         image_functions.cr_im_from_shapeslist2( prev_im1file, directory, [each_file_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
      if each_file_shapes[1] != "":
         save_im2fpath = across_all_files_imdir + result_name + "." + prev_im2file + ".png"
         image_functions.cr_im_from_shapeslist2( prev_im2file, directory, [each_file_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )  
      
      if each_file_shapes[2] != "":
         save_im1fpath = across_all_files_imdir + result_name + "." + cur_im1file + ".png"
         image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [each_file_shapes[2]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )      
      if each_file_shapes[3] != "":
         save_im2fpath = across_all_files_imdir + result_name + "." + cur_im2file + ".png"
         image_functions.cr_im_from_shapeslist2( cur_im2file, directory, [each_file_shapes[3]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )  





















