# find small pixel count shapes neighbors
from libraries import pixel_functions, image_functions, read_files_functions

import tkinter
from PIL import ImageTk, Image
import os, sys
import pickle
import copy

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir

image_filename1 = '11'
image_filename2 = "12"

directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


if directory != "" and directory[-1] != '/':
   directory +='/'


spixcShp_w_same_Lshapes_dir = top_shapes_dir + directory + "spixc_shapes/same_Lshapes/" + shapes_type + "/"
target_file = spixcShp_w_same_Lshapes_dir + "data/" + image_filename1 + "." + image_filename2 + ".data"


with open (target_file, 'rb') as fp:
   # [['2', '26000', 0.9470517448856799], ... ]
   # [ [image1, image2, match count ], ... ]
   target_data = pickle.load(fp)
fp.close()


# this is used for displaying closest matched images
root = tkinter.Tk()

for each_math in target_data:
   window = tkinter.Toplevel(root)
   window.title( each_math[0] + " " + each_math[1] )

   original_shape_file = spixcShp_w_same_Lshapes_dir  + image_filename1 + "/" + each_math[0] + ".png"
   compare_shape_file = spixcShp_w_same_Lshapes_dir + image_filename2 + "/" + each_math[1] + ".png"
   
   img = ImageTk.PhotoImage(Image.open(original_shape_file))
   img2 = ImageTk.PhotoImage(Image.open(compare_shape_file))
  
   label1 = tkinter.Label(window, image = img, bg="white")
   label1.image = img
   label1.pack()
   
   label2 = tkinter.Label(window, image = img2, bg="white" )
   label2.image = img2
   label2.pack()   


root.mainloop()




























