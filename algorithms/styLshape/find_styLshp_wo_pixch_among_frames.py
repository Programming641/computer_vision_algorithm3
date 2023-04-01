# find staying large shapes between frames.py
# if pixel changes ocurr only a little inside the shape and not at the boundaries, then this likely implies that
# shape is still at the same location.
# take out the pixel changes from the shape. then match based on the non-changed pixels.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
import pickle
import math
import winsound
import sys, os

filename1 = "11"
directory = "videos/street3/resized/min"
filename2 = "12"
filenames = [ filename1, filename2 ]
shapes_type = "intnl_spixcShp"



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


if shapes_type == "normal":
   styLshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/normal/data/"

elif shapes_type == "intnl_spixcShp":
   styLshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/intnl_spixcShp/data/"

else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()

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

# now that I have all the "btwn_frames" files, I need to put them in order.
# the order is that the small number file comes first.
# example. 10.11 -> 11.12 -> 12.13 ...
# if there are multiple same numbers before the comma, then the smallest second number after the comma should come first
# example. 10.11 -> 10.12 -> 10.13 ...
ordered_btwn_frames_files = btwn_frames_functions.put_btwn_frames_files_in_order( btwn_frames_files )


# [ { image file number: file's shapeid, image file number: file's shapeid, ... }, ... ]
shapes_among_frames = []
first_frame = True
for ordered_btwn_frames_file in ordered_btwn_frames_files:
   first_num_lastindex = ordered_btwn_frames_file.find(".")
   first_filenum = ordered_btwn_frames_file[0: first_num_lastindex] 
   second_filenum = ordered_btwn_frames_file[first_num_lastindex + 1: len( ordered_btwn_frames_file )] 
   
   with open (styLshapes_wo_pixch_Ddir + ordered_btwn_frames_file + ".data", 'rb') as fp:
      # [['21455', '22257'], ... ]
      stayingLshapes_wo_pixch = pickle.load(fp)
   fp.close()

   print( stayingLshapes_wo_pixch )
   
   sys.exit()
































