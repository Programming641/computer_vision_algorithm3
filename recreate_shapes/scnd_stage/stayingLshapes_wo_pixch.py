
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions
from libraries.cv_globals import top_shapes_dir, styLshapes_wo_pixch, scnd_stg_all_files
import pickle, shutil

import sys, os

im1file = "14"
im2file = "15"
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


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


styLshapes_wo_pixch_dir = top_shapes_dir + directory + scnd_stg_all_files + "/styLshapes_wo_pixch/"
if os.path.exists(styLshapes_wo_pixch_dir ) == False:
   os.makedirs(styLshapes_wo_pixch_dir )

staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/"


for each_files in all_matches_so_far:
   print( each_files )
   
   im1file = each_files.split(".")[0]
   im2file = each_files.split(".")[1]

   styLshapes_wo_pixch_imdir = styLshapes_wo_pixch_dir + im1file + "." + im2file + "/"

   # delete and create folder
   if os.path.exists(styLshapes_wo_pixch_imdir) == True:
      files_len = len( os.listdir(styLshapes_wo_pixch_imdir) )
      print( str( files_len ) + " files before")
      
      shutil.rmtree(styLshapes_wo_pixch_imdir)
   os.makedirs(styLshapes_wo_pixch_imdir)


   staying_Lshapes_wo_pixch_dfile = staying_Lshapes_Ddir + "data/" + im1file + "." + im2file + ".data"
   with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
      # [['79999', '79936', ['67590', '67196']]]
      # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
      sty_Lshapes_wo_pixch = pickle.load(fp)
   fp.close()



   for each_shapes in sty_Lshapes_wo_pixch:
      if ( each_shapes[0], each_shapes[1] ) not in all_matches_so_far[ each_files ]:
      
         save_im1fpath = styLshapes_wo_pixch_imdir + each_shapes[0] + "." + each_shapes[1] + "im1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, [each_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255,0,0) )

         save_im2fpath = styLshapes_wo_pixch_imdir + each_shapes[0] + "." + each_shapes[1] + "im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, [each_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0,0,255) )
      











 




















