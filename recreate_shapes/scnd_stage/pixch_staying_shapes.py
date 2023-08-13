
from libraries import image_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, pixch_sty_dir, scnd_stg_all_files
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


pixch_sty_shapes_dir = top_shapes_dir + directory + scnd_stg_all_files + "/pixch_sty_shapes/"
if os.path.exists(pixch_sty_shapes_dir ) == False:
   os.makedirs(pixch_sty_shapes_dir )

sty_shapes_dir = top_shapes_dir + directory + pixch_sty_dir + "/"


for each_files in all_matches_so_far:
   print( each_files )
   
   im1file = each_files.split(".")[0]
   im2file = each_files.split(".")[1]

   sty_shapes_imdir = pixch_sty_shapes_dir + im1file + "." + im2file + "/"

   # delete and create folder
   if os.path.exists(sty_shapes_imdir) == True:
      files_len = len( os.listdir(sty_shapes_imdir) )
      print( str( files_len ) + " files before")
      
      shutil.rmtree(sty_shapes_imdir)
   os.makedirs(sty_shapes_imdir)


   sty_shapes_file1 = sty_shapes_dir + "data/" + im1file + "." + im2file + "." + im1file + ".data"
   with open (sty_shapes_file1, 'rb') as fp:
      # [('1270', '2072'), ('2062', '2062'), ... ]
      # [ ( image1 shapeid, image2 shapeid ), ... ]
      sty_shapes1 = pickle.load(fp)
   fp.close()

   sty_shapes_file2 = sty_shapes_dir + "data/" + im1file + "." + im2file + "." + im2file + ".data"
   with open (sty_shapes_file2, 'rb') as fp:
      # [('1270', '2072'), ('2062', '2062'), ... ]
      # [ ( image1 shapeid, image2 shapeid ), ... ]
      sty_shapes2 = pickle.load(fp)
   fp.close()

   
   all_sty_shapes = [ temp_shapes for temp_shapes in sty_shapes1 if temp_shapes not in sty_shapes2 ]
   all_sty_shapes.extend( sty_shapes2 )

   for each_sty_shapes in all_sty_shapes:
      if each_sty_shapes not in all_matches_so_far[ each_files ]:
   
         save_im1fpath = sty_shapes_imdir + each_sty_shapes[0] + "." + each_sty_shapes[1] + "im1.png"
         image_functions.cr_im_from_shapeslist2( im1file, directory, [each_sty_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255,0,0) )

         save_im2fpath = sty_shapes_imdir + each_sty_shapes[0] + "." + each_sty_shapes[1] + "im2.png"
         image_functions.cr_im_from_shapeslist2( im2file, directory, [each_sty_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0,0,255) )


















