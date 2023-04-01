# find staying large shapes between frames.py
# if pixel changes ocurr only a little inside the shape and not at the boundaries, then this likely implies that
# shape is still at the same location.
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions, pixel_functions, btwn_frames_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir
import pickle
import winsound
import sys, os
import pathlib

###########################                    user input begin                ##################################
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"
###########################                    user input end                  ##################################


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

if shapes_type == "normal":
   staying_Lshapes_dir = top_shapes_dir + directory + styLshapes + "/" + shapes_type + "/"
   staying_Lshapes_Ddir = staying_Lshapes_dir + "data/"
   
   
elif shapes_type == "intnl_spixcShp":
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
   
   with open (staying_Lshapes_Ddir + ordered_btwn_frames_file + ".data", 'rb') as fp:
      # [['21455', '22257'], ... ]
      stayingLshapes = pickle.load(fp)
   fp.close()


   # looping current 2 frames matches
   for btwn_frames_match in stayingLshapes:
      if len( btwn_frames_match ) == 0:
         continue
      
      # initializing shapes_among_frames with image1 shapes
      if first_frame is True:
         
         shapes_among_frames_index = len( shapes_among_frames )
         shapes_among_frames.append( {} )
         shapes_among_frames[shapes_among_frames_index][ first_filenum ] = btwn_frames_match[0] 
         shapes_among_frames[shapes_among_frames_index][ second_filenum ] = btwn_frames_match[1] 
         
         first_frame = False
      else:
         # I have to find ordered_btwn_frames_file's first image file shapeid from shapes_among_frames
         found_btwn_frames_indexes = [ index for index, each_btwn_frames in enumerate( shapes_among_frames ) if btwn_frames_match[0] in each_btwn_frames.values() ]
         
         for found_btwn_frames_index in found_btwn_frames_indexes:
            shapes_among_frames[ found_btwn_frames_index ][ second_filenum ] = btwn_frames_match[1]
      
         # if btwn_frames_match's first iamge file shapeid is not found then add it as new list into shapes_among_frames
         if len( found_btwn_frames_indexes ) == 0:
            shapes_among_frames.append( { first_filenum: btwn_frames_match[0], second_filenum: btwn_frames_match[1] } )
         

# this is used for displaying closest matched images
root = tkinter.Tk()

for each_shapes_among_frames in shapes_among_frames:
   labels = []

   window = tkinter.Toplevel(root)
   window_titile = ""
   for filename in each_shapes_among_frames:
      window_titile = window_titile + filename + "." + each_shapes_among_frames[filename] + "_"
      shape_image = staying_Lshapes_dir + filename + "/" + each_shapes_among_frames[filename] + ".png"
      img = ImageTk.PhotoImage(Image.open(shape_image))
      labels_index = len( labels )
      labels.append( tkinter.Label(window, image = img, bg="white") )
      labels[ labels_index ].image = img
      labels[ labels_index ].pack()
   
   window.title( window_titile  )


root.mainloop()


































