
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

move_together_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/move_together/data/"
move_together_dfile = move_together_ddir + "move_together.data"
with open (move_together_dfile, 'rb') as fp:
   move_together_shapes = pickle.load(fp)
fp.close()



for filenames in move_together_shapes:
   print( filenames )
   
   im1file = filenames.split(".")[0]
   im2file = filenames.split(".")[1]

   move_together_imdir = top_shapes_dir + directory + scnd_stg_all_files + "/move_together/" + im1file + "." + im2file + "/"
   # delete and create folder
   if os.path.exists(move_together_imdir) == True:
      files_len = len( os.listdir(move_together_imdir) )
      print( str( files_len ) + " files before")
      shutil.rmtree(move_together_imdir)
   os.makedirs(move_together_imdir)

   for each_file_shapes in move_together_shapes[filenames]:
      # each_file_shapes -> ( image1 shape, image2 shape )
      
      image_filename = each_file_shapes[0] + "." + each_file_shapes[1]
      save_im1fpath = move_together_imdir + image_filename + ".png"
      save_im2fpath = move_together_imdir + image_filename + "im2.png"
      

      image_functions.cr_im_from_shapeslist2( im1file, directory, [each_file_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255, 0, 0 ) )
      image_functions.cr_im_from_shapeslist2( im2file, directory, [each_file_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0, 0, 255 ) )  

   files_len = len( os.listdir(move_together_imdir) )
   
   print( str( files_len ) + " files now")
   print()





