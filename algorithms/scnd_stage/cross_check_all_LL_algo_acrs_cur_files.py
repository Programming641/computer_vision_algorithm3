import tkinter
from PIL import ImageTk, Image
from libraries import read_files_functions
from libraries.cv_globals import top_shapes_dir, pixch_sty_dir, styLshapes, styLshapes_wo_pixch, internal, snd_stg_alg_shp_nbrs_dir
from libraries.cv_globals import scnd_stg_all_files
import pickle
import sys, os


im1file = "14"
im2file = "15"
shapes_type = "intnl_spixcShp"
directory = "videos/street3/resized/min"


if len(sys.argv) > 1:
   im1file = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   im2file = sys.argv[1][0: len( sys.argv[1] ) - 4 ]
   directory = sys.argv[3]
   
   shapes_type = "intnl_spixcShp"

   print("execute script algorithms/styLshapes/find_styLshp_wo_pixch_btwn_frames.py file1 " + im1file + " file2 " + im2file + " directory " + directory )



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
   # [['79999', '79936', ['67590', '67196']]]
   # [ ['image1 shapeid', 'image2 shapeid' [ matched pixels ]], ... ]
   styLshapes_wo_pixch = pickle.load(fp)
fp.close()

# converting into set of tuples
styLshapes_wo_pixch = set( [ ( temp_shapes[0], temp_shapes[1] ) for temp_shapes in styLshapes_wo_pixch ] )

only_nfnd_pixch_sty2_Dir = top_shapes_dir + directory + snd_stg_alg_shp_nbrs_dir + "/only_nfnd_pixch_sty2/"
scnd_stage_alg_shp2_dfile = only_nfnd_pixch_sty2_Dir + im1file + "." + im2file + ".data"
with open (scnd_stage_alg_shp2_dfile, 'rb') as fp:
   # [[['3120', '11916'], ['4712', '11515']], [['3294', '2085'], ['4510', '4516']], ... ]
   # [ [ [ image1 shapeids ], [ image2 shapeids ] ], ... ]
   scnd_stage_alg_shp2 = pickle.load(fp)
fp.close()


mid_ch_dir = top_shapes_dir + directory + "pixch/ch_shapes/mid_ch_sty/"
mid_ch_dfile = mid_ch_dir + "data/" + im1file + "." + im2file + "verified.data"
with open (mid_ch_dfile, 'rb') as fp:
   # {('56582', '57397'), ('34163', '35293'), ... }
   mid_ch_shapes = pickle.load(fp)
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
         
         if matched is False:
            # search in scnd_stage_alg_shp2
            found_matches = [ True for temp_shapes in scnd_stage_alg_shp2 if shapes_pair[0] in temp_shapes[0] and shapes_pair[1] in temp_shapes[1] ]
            
            if len( found_matches ) >= 1:
               verified_shapes.add( shapes_pair )
               already_added.append( shapes_pair )
            
   elif type(target_file) is list:
      # target_file is scnd_stage_alg_shp2
      for shapes_pair in target_file:
         # shapes_pair -> [['3120', '11916'], ['4712', '11515']]
         for lindex, cur_im1shape in enumerate(shapes_pair[0]):
            
            if ( cur_im1shape, shapes_pair[1][lindex] ) in already_added:
               continue
            
            for cur_file in other_files:
               found_matches = [ True for temp_shapes in cur_file if cur_im1shape == temp_shapes[0] and shapes_pair[1][lindex] == temp_shapes[1] ]

               if len( found_matches ) >= 1:
                  
                  verified_shapes.add( ( cur_im1shape,shapes_pair[1][lindex] )  )
                  already_added.append( ( cur_im1shape,shapes_pair[1][lindex] )  )
                  
                  break
         


find_verified_shapes_across_all_files( pixch_sty_shapes, [styLshapes, styLshapes_wo_pixch, mid_ch_shapes ] )
find_verified_shapes_across_all_files( styLshapes, [pixch_sty_shapes, styLshapes_wo_pixch, mid_ch_shapes ] )
find_verified_shapes_across_all_files( styLshapes_wo_pixch, [pixch_sty_shapes,styLshapes, mid_ch_shapes ] )
find_verified_shapes_across_all_files( mid_ch_shapes, [pixch_sty_shapes,styLshapes, styLshapes_wo_pixch ] )
find_verified_shapes_across_all_files( scnd_stage_alg_shp2, [pixch_sty_shapes,styLshapes, styLshapes_wo_pixch, mid_ch_shapes ] )


across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
if os.path.exists(across_all_files_ddir ) == False:
   os.makedirs(across_all_files_ddir )

across_all_files_dfile = across_all_files_ddir + im1file + "." + im2file + ".data"
with open(across_all_files_dfile, 'wb') as fp:
   pickle.dump(verified_shapes, fp)
fp.close()
































