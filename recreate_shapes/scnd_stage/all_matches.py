
import tkinter
from PIL import ImageTk, Image

from libraries import pixel_shapes_functions, read_files_functions, image_functions
from libraries.cv_globals import top_shapes_dir, scnd_stg_all_files, internal
import sys, os
import pickle
import shutil


shapes_type = "intnl_spixcShp"
directory = "videos/street6/resized/min"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

if shapes_type == "normal":
   print("ERROR. shapes_type normal is not supported")
   sys.exit()

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()



across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
across_all_files_dfile = across_all_files_ddir + "all_files.data"
with open (across_all_files_dfile, 'rb') as fp:
   acrs_all_files_shapes = pickle.load(fp)
fp.close()

all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes


all_matches_dir = top_shapes_dir + directory + scnd_stg_all_files + "/all_matches/"
if os.path.exists(all_matches_dir ) == False:
   os.makedirs(all_matches_dir )




for each_files in all_matches_so_far:
   print( each_files )
   
   im1file = each_files.split(".")[0]
   im2file = each_files.split(".")[1]
   
   all_matches_imdir = all_matches_dir + im1file + "." + im2file + "/"

   # delete and create folder
   if os.path.exists(all_matches_imdir) == True:
      files_len = len( os.listdir(all_matches_imdir) )
      print( str( files_len ) + " files before")
      
      shutil.rmtree(all_matches_imdir)
   os.makedirs(all_matches_imdir)
   
   done_im_shapes = []
   im_couner = 1
   
   for each_file_shapes in all_matches_so_far[ each_files ]:
      if each_file_shapes in done_im_shapes:
         continue
   
      im1fname = all_matches_imdir + str( im_couner ) + "im1.png"
      im2fname = all_matches_imdir + str( im_couner ) + "im2.png"

      result_im_shapes = [ temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[0] == each_file_shapes[0] ]

      done_im_shapes.extend( result_im_shapes )
      
      result_im1shapes = [ temp_shape[0] for temp_shape in result_im_shapes ]
      result_im2shapes = [ temp_shape[1] for temp_shape in result_im_shapes ]

      result_im_shapes = [ temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[1] == each_file_shapes[1] ]

      done_im_shapes.extend( result_im_shapes )
      
      result_im1shapes.extend( [ temp_shape[0] for temp_shape in result_im_shapes ] )
      result_im2shapes.extend( [ temp_shape[1] for temp_shape in result_im_shapes ] )

      image_functions.cr_im_from_shapeslist2( im1file, directory, result_im1shapes, save_filepath=im1fname, shapes_rgb=(0, 255, 0 ) )
      image_functions.cr_im_from_shapeslist2( im2file, directory, result_im2shapes, save_filepath=im2fname, shapes_rgb=(0, 0, 255 ) )

      
      im_couner += 1


   files_len = len( os.listdir(all_matches_imdir) )
   
   print( str( files_len ) + " files now")
   print()







