# if most of pixel changes occur near the shape boundaries and not inside the shape, then the shape
# moved only a little
from libraries import pixel_functions, read_files_functions, pixel_shapes_functions

import tkinter
from PIL import ImageTk, Image
import math
import os, sys
import winsound
import pickle
import pathlib

from libraries import btwn_amng_files_functions
from libraries.cv_globals import top_shapes_dir, top_images_dir, frth_smallest_pixc, Lshape_size, internal


directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


pixch_dir = top_shapes_dir + directory + "pixch/"
pixch_sty_shapes_ddir = pixch_dir + "sty_shapes/data/"


# loop all "sty_shapes" files
data_dir = pathlib.Path(pixch_sty_shapes_ddir)

btwn_frames_files = []
for data_file in data_dir.iterdir():
   data_filename = os.path.basename(data_file)
   
   # check if the file has the following form. if so, then the target file is found
   # 10.11verified.data   11.12verified.data and so on.
   filename_split_by_period = data_filename.split(".")
   
   if len( filename_split_by_period ) != 3:
      continue
   
   fst_filename = filename_split_by_period[0]
   scnd_filename = filename_split_by_period[1].strip("verified")
   data_extension = filename_split_by_period[2]
   
   if not fst_filename.isnumeric() or not scnd_filename.isnumeric() or data_extension != "data":
      continue   
   
   btwn_frames_files.append( fst_filename + "." + scnd_filename )


# ordered_files -> ['10.11', '11.12', '12.13']
ordered_files = btwn_amng_files_functions.put_btwn_frames_files_in_order( btwn_frames_files )


# [ [ [ 10.11, 11.12, 12.13, ... ], [ ( "111", "444"), ( "444", "80" ), ( "80", "9" ), ... ] ], ... ]
# [ [ [ filename1, filename2, filename3... ], [ ( file 10's shapeid, file 11's shapeid ), ( file 11's shapeid, file 12's shapeid ), 
#     ( file 12's shapeid, file 13's shapeid ), ... ] ], ... ]
#
consecutive_matches = []
prev_filename = None
prev_pixch_sty_shapes = None
for data_file in ordered_files:
   print("current file " + data_file )
   # filename has the following form. 10.11.10
   # filename1.filename2.main filename
   filename_splitby_period = data_file.split(".")
      
   filename1 = filename_splitby_period[0]
   filename2 = filename_splitby_period[1]
      
   with open (pixch_sty_shapes_ddir + data_file + "verified.data", 'rb') as fp:
      # [('1367', '1366'), ('2072', '2874'), ... ]
      # [ ( matched image1 shapeid , matched image2 shapeid ), ... ]
      pixch_sty_shapes = pickle.load(fp)
   fp.close()
      

   if prev_pixch_sty_shapes is None:
      prev_pixch_sty_shapes = pixch_sty_shapes
      prev_filename = filename1 + "." + filename2
   
   else:

      for prev_shapes in prev_pixch_sty_shapes:
         found_prev_shapes = [ shapes for shapes in pixch_sty_shapes if shapes[0] == prev_shapes[1] ]
         
         
         for found_prev_shape in found_prev_shapes:
            # check if prev_shapes image1 shape can be found from consecutive_matches
            # check if prev_filename is not the first file
            found_consec_lindexes = []
            if prev_filename != ordered_files[0]:
               
               for consec_lindex, consecutive_match in enumerate(consecutive_matches):
                  # consecutive_match -> [ [ 10.11, 11.12, 12.13, ... ], [ ( "111", "444"), ( "444", "80" ), ( "80", "9" ), ... ] ]
                  
                  for lindex, consec_filename in enumerate(consecutive_match[0]):
                     # checking if prev_shapes image1 shapeid can be found from consecutive_match
                     if consec_filename == prev_filename and consecutive_match[1][lindex][1] == prev_shapes[0]:
                        found_consec_lindexes.append( consec_lindex )
                  
               for found_consec_lindex in found_consec_lindexes:
                  # add filename
                  consecutive_matches[found_consec_lindex][0].append( filename1 + "." + filename2 )
                  consecutive_matches[found_consec_lindex][1].append( found_prev_shape )
               
            if len( found_consec_lindexes ) == 0:
               consecutive_matches.append( [ [ prev_filename, filename1 + "." + filename2 ], [ prev_shapes, found_prev_shape ] ] )


      prev_filename = filename1 + "." + filename2
      prev_pixch_sty_shapes = pixch_sty_shapes

                  


with open(pixch_sty_shapes_ddir + "consecutives.data", 'wb') as fp:
   pickle.dump(consecutive_matches, fp)
fp.close()

               
                  
root = tkinter.Tk()

for consecutive_shapes in consecutive_matches:
   # consecutive_shapes -> [ [ 10.11, 11.12, 12.13, ... ], [ ( "111", "444"), ( "444", "80" ), ( "80", "9" ), ... ] ]

   labels = []
   window = tkinter.Toplevel(root)
   window_titile = ""
   
   prev_im2shape = None
   for lindex, btwn_file in enumerate(consecutive_shapes[0]):
      
      filename1 = btwn_file.split(".")[0]
      filename2 = btwn_file.split(".")[1]
      
      file1shape = consecutive_shapes[1][lindex][0]
      file2shape = consecutive_shapes[1][lindex][1]
      
      if prev_im2shape is None:
      
         window_titile += filename1 + "." + file1shape + "." + filename2 + "." + file2shape + "."
      
         shape_image = top_shapes_dir + directory + "shapes/" + shapes_type + "/" + filename1 + "/" + file1shape + ".png"
         img = ImageTk.PhotoImage(Image.open(shape_image))
         labels_index = len( labels )
         labels.append( tkinter.Label(window, image = img, bg="white") )
         labels[ labels_index ].image = img
         labels[ labels_index ].pack()

         shape_image = top_shapes_dir + directory + "shapes/" + shapes_type + "/" + filename2 + "/" + file2shape + ".png"
         img = ImageTk.PhotoImage(Image.open(shape_image))
         labels_index = len( labels )
         labels.append( tkinter.Label(window, image = img, bg="white") )
         labels[ labels_index ].image = img
         labels[ labels_index ].pack()        

      elif prev_im2shape == file1shape:
         
         window_titile += filename2 + "." + file2shape + "."
         
         shape_image = top_shapes_dir + directory + "shapes/" + shapes_type + "/" + filename2 + "/" + file2shape + ".png"
         img = ImageTk.PhotoImage(Image.open(shape_image))
         labels_index = len( labels )
         labels.append( tkinter.Label(window, image = img, bg="white") )
         labels[ labels_index ].image = img
         labels[ labels_index ].pack()           


      prev_im2shape = file2shape

   window.title( window_titile  )


root.mainloop()



















      
   
   

































