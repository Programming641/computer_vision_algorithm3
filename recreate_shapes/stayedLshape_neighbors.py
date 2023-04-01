import pathlib
import os, sys
import shutil
import pickle
import tkinter
from PIL import ImageTk, Image

from libraries.cv_globals import proj_dir, top_shapes_dir, styLshapes_w_nbrs
from libraries import image_functions

shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"

image1_file = "12"
image2_file = "13"
directory = "videos/street3/resized/min"
# choices are
# normal, intnl_spixcShp
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

styLshapes_w_neighbors_dir = top_shapes_dir + directory + styLshapes_w_nbrs + "/" + shapes_type + "/"
styLshapes_w_neighbors_ddir = styLshapes_w_neighbors_dir + "data/"
styLshapes_w_neighbors_im1dir = styLshapes_w_neighbors_dir + image1_file + "/"
styLshapes_w_neighbors_im2dir = styLshapes_w_neighbors_dir + image2_file + "/"

# loop all "btwn_frames" files
data_dir = pathlib.Path(styLshapes_w_neighbors_ddir)

btwn_frames_files = []
for data_file in data_dir.iterdir():
   data_filename = os.path.basename(data_file)
   data_filename = os.path.splitext(data_filename)[0]
   
   if "." in data_filename:
      # current file is "btwn_frames" file
      btwn_frames_files.append( data_filename )

for btwn_frames_file in btwn_frames_files:
   first_num_lastindex = btwn_frames_file.find(".")
   first_filenum = btwn_frames_file[0: first_num_lastindex]
   second_filenum = btwn_frames_file[first_num_lastindex + 1: len( btwn_frames_file )] 
   # delete and create folder
   if os.path.exists(styLshapes_w_neighbors_dir + first_filenum + "." + second_filenum) == True:
      shutil.rmtree(styLshapes_w_neighbors_dir + first_filenum + "." + second_filenum)
   os.makedirs( styLshapes_w_neighbors_dir + first_filenum + "." + second_filenum )



# { "file1.file2": [ [ ['2072', '2874'], ['53280', '57316'], ... ], ... ], ... }
all_btwn_frames_files = {}
for btwn_frames_file in btwn_frames_files:

   styLshapes_w_neighbors_dfile = styLshapes_w_neighbors_ddir + btwn_frames_file + ".data"
   with open (styLshapes_w_neighbors_dfile, 'rb') as fp:
      # {'2072.1': [['2072', '2874'], ['53280', '57316']], ... }
      # { image1 shapeid.count of this shapeid: [ [ image1shapeid, image2 shapeid ], ... ], ... }
      # { image1 shapeid.count of this shapeid: [ all neighbors for current image1 shapeid.count ] }
      styLshapes_w_neighbors = pickle.load(fp)
   fp.close()


   first_num_lastindex = btwn_frames_file.find(".")
   first_filenum = btwn_frames_file[0: first_num_lastindex]
   second_filenum = btwn_frames_file[first_num_lastindex + 1: len( btwn_frames_file )]  

   all_btwn_frames_files[ first_filenum + "." + second_filenum ] = styLshapes_w_neighbors



for file1_2names in all_btwn_frames_files:
   first_num_lastindex = file1_2names.find(".")
   first_filenum = file1_2names[0: first_num_lastindex]
   second_filenum = file1_2names[first_num_lastindex + 1: len( file1_2names )]

   for im1_n2_nbrs_shapeid in all_btwn_frames_files[ file1_2names ]:
      # im1_n2_nbrs_shapeid -> 2072.1
      # all_btwn_frames_files[ file1_2names ][ im1_n2_nbrs_shapeid ]  -> [['2072', '2874'], ['53280', '57316']]
      
      im1shapes_file = styLshapes_w_neighbors_dir + first_filenum + "." + second_filenum + "/" + "im1." + im1_n2_nbrs_shapeid + ".png" 
      im2shapes_file = styLshapes_w_neighbors_dir + first_filenum + "." + second_filenum + "/" + "im2." + im1_n2_nbrs_shapeid + ".png" 
      
      im1shapes = []
      im2shapes = []
      
      for im1_2_shapeids in all_btwn_frames_files[ file1_2names ][ im1_n2_nbrs_shapeid ]:
         im1shapes.append( im1_2_shapeids[0] )
         im2shapes.append( im1_2_shapeids[1] )
         

         
      image_functions.cr_im_from_shapeslist2( first_filenum, directory, im1shapes, save_filepath=im1shapes_file , shapes_rgb=( 0, 0, 255 ) )   
      image_functions.cr_im_from_shapeslist2( second_filenum, directory, im2shapes, save_filepath=im2shapes_file , shapes_rgb=( 0, 0, 255 ) )  







