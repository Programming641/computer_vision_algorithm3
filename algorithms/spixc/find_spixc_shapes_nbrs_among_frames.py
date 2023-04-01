
from libraries import pixel_functions, image_functions, read_files_functions, btwn_frames_functions
import tkinter
from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import pathlib

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir


directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

spixcShp_nbrs_dir = top_shapes_dir + directory  + "spixc_shapes/nbrs/"
spixcShp_nbrs_ddir = spixcShp_nbrs_dir + "data/"

# loop all "btwn_frames" files
data_dir = pathlib.Path(spixcShp_nbrs_ddir)

btwn_frames_files = []
for data_file in data_dir.iterdir():
   data_filename = os.path.basename(data_file)
   data_filename = os.path.splitext(data_filename)[0]
   
   if "." in data_filename:
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
   
   with open (spixcShp_nbrs_ddir + ordered_btwn_frames_file + ".data", 'rb') as fp:
      # [[], [], [], [], [], [['555', '29056', 0.23620627479264333]], ... ]
      # [ [ image1 shapeid, image2 shapeid, match count. smaller the better match ], ... ]
      spixcShp_nbrs = pickle.load(fp)
   fp.close()


   # looping current 2 frames matches
   for btwn_frames_match in spixcShp_nbrs:
      if len( btwn_frames_match ) == 0:
         continue
      
      for each_btwn_match in btwn_frames_match:
      
         # initializing shapes_among_frames with image1 shapes
         if first_frame is True:
         
            shapes_among_frames_index = len( shapes_among_frames )
            shapes_among_frames.append( {} )
            shapes_among_frames[shapes_among_frames_index][ first_filenum ] = each_btwn_match[0] 
            shapes_among_frames[shapes_among_frames_index][ second_filenum ] = each_btwn_match[1] 
         
            first_frame = False
         else:
            # I have to find ordered_btwn_frames_file's first image file shapeid from shapes_among_frames
            found_btwn_frames_indexes = [ index for index, each_btwn_frames in enumerate( shapes_among_frames ) if each_btwn_match[0] in each_btwn_frames.values() ]
         
            for found_btwn_frames_index in found_btwn_frames_indexes:
               shapes_among_frames[ found_btwn_frames_index ][ second_filenum ] = each_btwn_match[1]
      
            # if each_btwn_match's first iamge file shapeid is not found then add it as new list into shapes_among_frames
            if len( found_btwn_frames_indexes ) == 0:
               shapes_among_frames.append( { first_filenum: each_btwn_match[0], second_filenum: each_btwn_match[1] } )
         


# this is used for displaying closest matched images
root = tkinter.Tk()

for each_shapes_among_frames in shapes_among_frames:
   labels = []

   window = tkinter.Toplevel(root)
   window_titile = ""
   for filename in each_shapes_among_frames:
      window_titile = window_titile + filename + "." + each_shapes_among_frames[filename] + "_"
      shape_image = spixcShp_nbrs_dir + filename + "/" + each_shapes_among_frames[filename] + ".png"
      img = ImageTk.PhotoImage(Image.open(shape_image))
      labels_index = len( labels )
      labels.append( tkinter.Label(window, image = img, bg="white") )
      labels[ labels_index ].image = img
      labels[ labels_index ].pack()
   
   window.title( window_titile  )


root.mainloop()























