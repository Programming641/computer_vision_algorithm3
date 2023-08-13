
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
consecutives_dfile = across_all_files_ddir + "consecutives.data"
with open (consecutives_dfile, 'rb') as fp:
   # [{'10.11': ('56319', '57125'), '11.12': ('57125', '57529')}, ... ]
   # consecutives that include broken up shapes -> {'10.11': ['4510', ['4108', '1306', '3315']]}
   # consecutives that include combining shapes -> {'11.12': [['79968', '79999'], '79999']}
   # another kind of consecutives -> {'10.11': ['30115', ['27323', '30917']], '11.12': [['27323', '30917'], ['27324', '31319']]}
   consecutive_shapes = pickle.load(fp)
fp.close()



consecutives_dir = top_shapes_dir + directory + scnd_stg_all_files + "/consecutives/images/"
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
      
      im1not_found = None
      im2not_found = None
      if type( shapes ) is tuple:
         image_functions.cr_im_from_shapeslist2( im1file, directory, [shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
         image_functions.cr_im_from_shapeslist2( im2file, directory, [shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )    

         im1not_found = False
         im2not_found = False         

      elif type( shapes ) is list:
         
         if type( shapes[0] ) is list:
            image_functions.cr_im_from_shapeslist2( im1file, directory, shapes[0], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
            im1not_found = False
         elif type( shapes[0] ) is str:
            image_functions.cr_im_from_shapeslist2( im1file, directory, [shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
            im1not_found = False

         if type( shapes[1] ) is list:
            image_functions.cr_im_from_shapeslist2( im2file, directory, shapes[1], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )
            im2not_found = False 
         elif type( shapes[1] ) is str:
            image_functions.cr_im_from_shapeslist2( im2file, directory, [shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )
            im2not_found = False 


      if im1not_found is not False or im2not_found is not False:
         print("ERROR")

   
   each_consecutives_counter += 1












