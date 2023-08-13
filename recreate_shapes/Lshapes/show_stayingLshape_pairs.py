
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions
from libraries.cv_globals import proj_dir, top_shapes_dir
import pickle

import winsound
import sys


image1 = "10"
directory = "videos/street3/resized/min"
image2 = "11"

# specify either one but not both
image1shapeid = "45331"
image2shapeid = ""


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

staying_Lshapes_Ddir = top_shapes_dir + directory + "staying_Lshapes/data/"


staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + image1 + "to" + image2 + ".data"
staying_Lshapes2to1_dfile = staying_Lshapes_Ddir + image2 + "to" + image1 + ".data"

staying_Lshapes_wo_pixch_Ddir = top_shapes_dir + directory + "staying_Lshapes_wo_pixch/data/"
staying_Lshapes_wo_pixch_dfile = staying_Lshapes_wo_pixch_Ddir + image1 + "." + image2 + ".data"

with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
   # [['79999', '79936', ['67590', '67196']]]
   # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
   sty_Lshapes_wo_pixch = pickle.load(fp)
fp.close()

all_im_shape_pairs = []
if image1shapeid != "":
   im1shape_pairs = [image_shapeids[1] for image_shapeids in sty_Lshapes_wo_pixch if image1shapeid == image_shapeids[0]]
   all_im_shape_pairs.extend( im1shape_pairs )
elif image2shapeid != "":
   im2shape_pairs = [image_shapeids[0] for image_shapeids in sty_Lshapes_wo_pixch if image2shapeid == image_shapeids[1]]
   all_im_shape_pairs.extend( im2shape_pairs )


with open (staying_Lshapes1to2_dfile, 'rb') as fp:

   styLshapes1to2 = pickle.load(fp)
fp.close()

with open (staying_Lshapes2to1_dfile, 'rb') as fp:

   styLshapes2to1 = pickle.load(fp)
fp.close()

unique_sty_im1_2_shapes = [value for value in styLshapes1to2 if value not in styLshapes2to1]
unique_sty_im2_1_shapes = [value for value in styLshapes2to1 if value not in styLshapes1to2]
common_sty_im1_2_shapes = [value for value in styLshapes2to1 if value in styLshapes1to2]

all_sty_im1_2_shapes = unique_sty_im1_2_shapes + unique_sty_im2_1_shapes + common_sty_im1_2_shapes


if image1shapeid != "":
   im1shape_pairs = [image_shapeids[1] for image_shapeids in all_sty_im1_2_shapes if image1shapeid == image_shapeids[0]]
   all_im_shape_pairs.extend( im1shape_pairs )
elif image2shapeid != "":
   im2shape_pairs = [image_shapeids[0] for image_shapeids in sty_Lshapes_wo_pixch if image2shapeid == image_shapeids[1]]
   all_im_shape_pairs.extend( im2shape_pairs )




# this is used for displaying closest matched images
root = tkinter.Tk()

for matched_shape in all_im_shape_pairs:
   # displaying closest match images/
   
   main_shapeid = ""
   if image1shapeid != "":
      main_shapeid = image1shapeid
   elif image2shapeid != "":
      main_shapeid = image2shapeid
   
   window = tkinter.Toplevel(root)
   window.title( str(main_shapeid) + " " + str( matched_shape ) )

   original_shape_file = top_shapes_dir + directory + "shapes/" + image1 + "_shapes/" + main_shapeid + ".png"
   compare_shape_file = top_shapes_dir + directory + "shapes/" + image2 + "_shapes/" + matched_shape + ".png"
   
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












