import tkinter
from PIL import ImageTk, Image
from libraries import read_files_functions, btwn_amng_files_functions
from libraries.cv_globals import top_shapes_dir, pixch_sty_dir, styLshapes, styLshapes_wo_pixch, internal, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import scnd_stg_all_files
import pickle
import sys, os


im1file = "25"
im2file = "26"
shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min1"


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"

   print("execute script algorithms/scnd_stage/cross_check_all_LL_algo_acrs_cur_files.py file1 " + im1file + " file2 " + im2file + " directory " + directory )



# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'


pixch_dir = top_shapes_dir + directory + "pixch/"
pixch_sty_shapes_ddir = pixch_dir + "sty_shapes/data/"
sty_shapes_file = pixch_sty_shapes_ddir + im1file + "." + im2file + "verified.data"
with open (sty_shapes_file, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   pixch_sty_shapes = pickle.load(fp)
fp.close()

# converting into set of tuples
pixch_sty_shapes = set( pixch_sty_shapes )

# staying large shapes. current file
staying_Lshapes_Ddir = top_shapes_dir + directory + styLshapes + "/" + shapes_type + "/data/"
staying_Lshapes1to2_dfile = staying_Lshapes_Ddir + im1file + "." + im2file + ".data"
with open (staying_Lshapes1to2_dfile, 'rb') as fp:
   # [['56099', '56105'], ... ]
   styLshapes = pickle.load(fp)
fp.close()

# converting into set of tuples
styLshapes = set( [ ( temp_shapes[0], temp_shapes[1] ) for temp_shapes in styLshapes ] )

staying_Lshapes_wo_pixch_Ddir = top_shapes_dir + directory + styLshapes_wo_pixch + "/" + shapes_type + "/data/"
staying_Lshapes_wo_pixch_dfile = staying_Lshapes_wo_pixch_Ddir + im1file + "." + im2file + "verified.data"
with open (staying_Lshapes_wo_pixch_dfile, 'rb') as fp:
   styLshapes_wo_pixch = pickle.load(fp)
fp.close()

# converting into set of tuples
styLshapes_wo_pixch = set( [ ( temp_shapes[0], temp_shapes[1] ) for temp_shapes in styLshapes_wo_pixch ] )


pixch_shapes_dir = top_shapes_dir + directory + "pixch/ch_shapes/pixch_shapes/"
pixch_shapes_dfile = pixch_shapes_dir + "data/" + im1file + "." + im2file + ".data"
with open (pixch_shapes_dfile, 'rb') as fp:
   # [('1270', '2072'), ('2062', '2062'), ... ]
   # [ ( image1 shapeid, image2 shapeid ), ... ]
   pixch_shapes = pickle.load(fp)
fp.close()

template_dir = top_shapes_dir + directory + "template/"
image_template_dir = template_dir + "image_pixels/"
image_template_ddir = image_template_dir + "data/"
image_template_dfile = image_template_ddir + im1file + "." + im2file + ".data"
with open (image_template_dfile, 'rb') as fp:
   # { ('59428', '59426'), ('39679', '38065'), ... }
   matched_shapes_by_im_tmpl = pickle.load(fp)
fp.close()


# comparing with other current file shapes, if the type of match is one to one match, then matching the same 
# image1 and image2 shapes will verify the match
# for example. match from pixch_sty_shapes im1 is 100. im2 is 200. match type is one to one
#              match from styLshapes, im1 is 100. im2 is 200. match type is one to one
#              image1 100 and image2 200 are verified.

verified_shapes = set()
already_added = []
def find_verified_shapes_across_all_files( target_file, other_files ):
   
   if type(target_file) is set:
      for shapes_pair in target_file:
         # shapes_pair -> ('30026', '44819')
         if shapes_pair in already_added:
            continue
         
         cur_shapes_pair = set()
         cur_shapes_pair.add( shapes_pair )
         matched = False
         for other_file in other_files:
            found_matches = cur_shapes_pair.intersection( other_file )
            
            if len( found_matches ) >= 1:
               verified_shapes.add( shapes_pair )
               already_added.append( shapes_pair )
               matched = True
               break
         


find_verified_shapes_across_all_files( pixch_sty_shapes, [styLshapes, styLshapes_wo_pixch, pixch_shapes, matched_shapes_by_im_tmpl ] )
find_verified_shapes_across_all_files( styLshapes, [pixch_sty_shapes, styLshapes_wo_pixch, pixch_shapes, matched_shapes_by_im_tmpl ] )
find_verified_shapes_across_all_files( styLshapes_wo_pixch, [pixch_sty_shapes,styLshapes, pixch_shapes, matched_shapes_by_im_tmpl ] )
find_verified_shapes_across_all_files( pixch_shapes, [ pixch_sty_shapes, styLshapes, styLshapes_wo_pixch, matched_shapes_by_im_tmpl ] )
find_verified_shapes_across_all_files( matched_shapes_by_im_tmpl, [ pixch_sty_shapes, styLshapes, styLshapes_wo_pixch, pixch_shapes ] )


across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
if os.path.exists(across_all_files_ddir ) == False:
   os.makedirs(across_all_files_ddir )


across_all_files_dfile = across_all_files_ddir + im1file + "." + im2file + ".data"
with open(across_all_files_dfile, 'wb') as fp:
   pickle.dump(verified_shapes, fp)
fp.close()
































