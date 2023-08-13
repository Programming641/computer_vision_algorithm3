
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions
from libraries.cv_globals import top_shapes_dir, styLshapes_wo_pixch
import pickle

import winsound
import sys

image1 = "10"
directory = "videos/street3/resized/min"
image2 = "11"
shapes_type = "intnl_spixcShp"


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

staying_Lshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"
staying_Lshapes_wo_pixch_dfile = staying_Lshapes_wo_pixch_Ddir + image1 + "." + image2 + ".data"
with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
   # [['79999', '79936', ['67590', '67196']]]
   # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
   sty_Lshapes_wo_pixch = pickle.load(fp)
fp.close()


# this is used for displaying closest matched images
root = tkinter.Tk()

for shape_pair in sty_Lshapes_wo_pixch:
   # displaying closest match images/
   
   window = tkinter.Toplevel(root)
   window.title( str(shape_pair[0]) + " " + str( shape_pair[1] ) )

   original_shape_file = top_shapes_dir + directory + "shapes/" + shapes_type + "/" + image1 + "/" + shape_pair[0] + ".png"
   compare_shape_file = top_shapes_dir + directory + "shapes/" + shapes_type + "/" + image2 + "/" + shape_pair[1] + ".png"
   
   img = ImageTk.PhotoImage(Image.open(original_shape_file))
   img2 = ImageTk.PhotoImage(Image.open(compare_shape_file))
  
   label1 = tkinter.Label(window, image = img, bg="white")
   label1.image = img
   label1.pack()
   
   label2 = tkinter.Label(window, image = img2, bg="white" )
   label2.image = img2
   label2.pack()
      
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)      

root.mainloop()









