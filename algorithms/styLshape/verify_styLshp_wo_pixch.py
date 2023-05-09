
import tkinter
from PIL import ImageTk, Image
from libraries import pixel_shapes_functions, read_files_functions, same_shapes_functions, pixel_functions
from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir, styLshapes_wo_pixch, spixc_shapes, internal
from libraries.cv_globals import third_smallest_pixc
import pickle
import math
import winsound
import sys, os

im1file = "14"
im2file = "15"
directory = "videos/street3/resized/min"

shapes_type = "intnl_spixcShp"



# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'


staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"
staying_Lshapes_wo_pixch_dfile = staying_Lshapes_Ddir + im1file + "." + im2file + ".data"
with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
   # [ ['3380', '3790', ['2989', '2988', ... ] ], ... ]
   # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
   styLshapes_wo_pixch = pickle.load(fp)
fp.close()


original_image = Image.open(top_images_dir + directory + im1file + ".png")
im_width, im_height = original_image.size


if shapes_type == "normal":
   print("shapes_type normal is not supported in " + os.path.basename(__file__) )
   sys.exit()
   

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"

   shapes_dir = s_pixcShp_intnl_dir + "shapes/"
   shapes_dfile = shapes_dir + im1file + "shapes.data"
   im2shapes_dfile = shapes_dir + im2file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()
     

   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()


   shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + im2file + "_shape_nbrs.txt"



# {'79999': ['71555', '73953', ...], ...}
im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(im1file, directory, shape_neighbors_file)
im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(im2file, directory, im2shape_neighbors_file)

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type)


verified_shapes = same_shapes_functions.verify_matches( styLshapes_wo_pixch, [ im1shapes, im2shapes ], [ im1shapes_colors, im2shapes_colors ],
                  [ im1shapes_neighbors, im2shapes_neighbors ], im_width )

print( len( verified_shapes ) )

with open(staying_Lshapes_Ddir + im1file + "." + im2file + "verified.data", 'wb') as fp:
   pickle.dump(verified_shapes, fp)
fp.close()


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)      


























