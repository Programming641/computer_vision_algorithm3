
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, same_shapes_btwn_frames, read_files_functions, image_functions
from libraries.cv_globals import top_shapes_dir, styLshapes_wo_pixch
import pickle, shutil

import sys, os

im1file = "14"
im2file = "15"
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"
verified = ""


# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/"
staying_Lshapes_wo_pixch_dfile = staying_Lshapes_Ddir + "data/" + im1file + "." + im2file + verified + ".data"
with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
   # [['79999', '79936', ['67590', '67196']]]
   # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
   sty_Lshapes_wo_pixch = pickle.load(fp)
fp.close()


sty_Lshapes_wo_pixch_imdir = staying_Lshapes_Ddir + im1file + "." + im2file + "/"
# delete and create folder
if os.path.exists(sty_Lshapes_wo_pixch_imdir) == True:
   shutil.rmtree(sty_Lshapes_wo_pixch_imdir)
os.makedirs(sty_Lshapes_wo_pixch_imdir)


for each_shapes in sty_Lshapes_wo_pixch:
   save_im1fpath = sty_Lshapes_wo_pixch_imdir + each_shapes[0] + "." + each_shapes[1] + "im1.png"
   image_functions.cr_im_from_shapeslist2( im1file, directory, [each_shapes[0]], save_filepath=save_im1fpath , shapes_rgb=(255,0,0) )

   save_im2fpath = sty_Lshapes_wo_pixch_imdir + each_shapes[0] + "." + each_shapes[1] + "im2.png"
   image_functions.cr_im_from_shapeslist2( im2file, directory, [each_shapes[1]], save_filepath=save_im2fpath , shapes_rgb=(0,0,255) )
      











 




















