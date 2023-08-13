
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions
from libraries.cv_globals import top_shapes_dir, styLshapes
import pickle
import shutil
import winsound
import sys, os
import pathlib


directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

staying_Lshapes_dir = top_shapes_dir + directory + styLshapes + "/" + shapes_type + "/"
staying_Lshapes_Ddir = staying_Lshapes_dir + "data/"

# loop all "btwn_frames" files
data_dir = pathlib.Path(staying_Lshapes_Ddir)

btwn_frames_files = []
for data_file in data_dir.iterdir():
   data_filename = os.path.basename(data_file)
   # filename without last comma ( which should be extension )
   data_filename = os.path.splitext(data_filename)[0]
   # check if file has the following form
   # number.number
   if data_filename.count(".") == 1:
      first_num_lastindex = data_filename.find(".")
      if data_filename[0: first_num_lastindex].isnumeric() and data_filename[first_num_lastindex + 1: len( data_filename )].isnumeric():
         # current file is "btwn_frames" file
         btwn_frames_files.append( data_filename )


for btwn_frames_file in btwn_frames_files:
   first_num_lastindex = btwn_frames_file.find(".")
   first_filenum = btwn_frames_file[0: first_num_lastindex]
   second_filenum = btwn_frames_file[first_num_lastindex + 1: len( btwn_frames_file )] 
   # delete and create folder
   if os.path.exists(staying_Lshapes_dir + first_filenum) == True:
      shutil.rmtree(staying_Lshapes_dir + first_filenum)
   os.makedirs( staying_Lshapes_dir + first_filenum )
   if os.path.exists(staying_Lshapes_dir + second_filenum) == True:
      shutil.rmtree(staying_Lshapes_dir + second_filenum)
   os.makedirs( staying_Lshapes_dir + second_filenum )  

# { "file1.file2": [ [ file1 shapeid, file2 shapeid ], ... ], "file2.file3": [ [ file2 shapeid, file3 shapeid ], ... ], ... }
all_btwn_frames_files = {}
for btwn_frames_file in btwn_frames_files:

   staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + btwn_frames_file + ".data"
   with open (staying_Lshapes1to2_dfile, 'rb') as fp:

      styLshapes1to2 = pickle.load(fp)
   fp.close()

   first_num_lastindex = btwn_frames_file.find(".")
   first_filenum = btwn_frames_file[0: first_num_lastindex]
   second_filenum = btwn_frames_file[first_num_lastindex + 1: len( btwn_frames_file )]  

   all_btwn_frames_files[ first_filenum + "." + second_filenum ] = styLshapes1to2


for file1_2names in all_btwn_frames_files:
   first_num_lastindex = file1_2names.find(".")
   first_filenum = file1_2names[0: first_num_lastindex]
   second_filenum = file1_2names[first_num_lastindex + 1: len( file1_2names )]
   for im1_2shapeids in all_btwn_frames_files[ file1_2names ]:

      im1_2shape_file = staying_Lshapes_dir + first_filenum + "/" + im1_2shapeids[0] + ".png" 
      image_functions.cr_im_from_shapeslist2( first_filenum, directory, [ im1_2shapeids[0] ], save_filepath=im1_2shape_file , shapes_rgb=( 0, 0, 255 ) )

      im1_2shape_file = staying_Lshapes_dir + second_filenum + "/" + im1_2shapeids[1] + ".png" 
      image_functions.cr_im_from_shapeslist2( second_filenum, directory, [ im1_2shapeids[1] ], save_filepath=im1_2shape_file , shapes_rgb=( 0, 0, 255 ) )  
   
   
      
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)      













