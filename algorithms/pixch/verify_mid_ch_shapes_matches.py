from libraries import pixel_functions, read_files_functions, pixel_shapes_functions, image_functions, shapes_results_functions

from PIL import Image
import math
import os, sys
import winsound, time
import pickle

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, frth_smallest_pixc, third_smallest_pixc


im1file = '14'
im2file = "15"
shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min"

if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]

   print("execute script algorithms/styLshapes/find_styLshp_wo_pixch_btwn_frames.py file1 " + im1file + " file2 " + im2file + " directory " + directory )


# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


mid_ch_dir = top_shapes_dir + directory + "pixch/ch_shapes/mid_ch_sty/"
mid_ch_dfile = mid_ch_dir + "data/" + im1file + "." + im2file + "." + im1file + ".data"
with open (mid_ch_dfile, 'rb') as fp:
   # [('8423', '10023'), ('12444', '10846'), ... ]
   mid_ch_shapes = pickle.load(fp)
fp.close()

mid_ch_dfile = mid_ch_dir + "data/" + im1file + "." + im2file + "." + im2file + ".data"
with open (mid_ch_dfile, 'rb') as fp:
   mid_ch_shapes2 = pickle.load(fp)
fp.close()

mid_ch_shapes = set( mid_ch_shapes )
mid_ch_shapes |= set( mid_ch_shapes2 )


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

im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im1file, directory, shapes_type=shapes_type, min_colors=True)
im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(im2file, directory, shapes_type=shapes_type, min_colors=True)


print( len( mid_ch_shapes ) )


verified_matches = shapes_results_functions.verify_matches( mid_ch_shapes, [ im1shapes, im2shapes ], [ im1shapes_colors, im2shapes_colors ], 
                   [ im1shapes_neighbors, im2shapes_neighbors ], im_width  )

print( len( verified_matches ) )

with open(mid_ch_dir + "data/" + im1file + "." + im2file + "verified.data", 'wb') as fp:
   pickle.dump(verified_matches, fp)
fp.close()

































