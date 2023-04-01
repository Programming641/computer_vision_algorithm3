# find small pixel count shapes with same large shape matches between frames
# this script takes the results of find_spixcShp_Dnbr_sharing_Lshapes.py from two frames and find matches between them.

from libraries import pixel_functions, image_functions, read_files_functions, pixel_shapes_functions

from PIL import Image
import os, sys
import pickle
import math

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir


image_filename1 = "11"
image_filename2 = "12"
directory = "videos/street3/resized/min"

shapes_type = "intnl_spixcShp"

if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]

   directory = sys.argv[1]

   print("execute script find_spixcShp_Dnbr_sharing_Lshapes.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'


spixcShp_w_same_Lshapes_ddir = top_shapes_dir + directory + "spixc_shapes/same_Lshapes/" + shapes_type + "/data/"
spixcShp_w_same_Lshapes_dfile1 = spixcShp_w_same_Lshapes_ddir + image_filename1 + ".data"
spixcShp_w_same_Lshapes_dfile2 = spixcShp_w_same_Lshapes_ddir + image_filename2 + ".data"
with open (spixcShp_w_same_Lshapes_dfile1, 'rb') as fp:
   # {'54905': [['55703'], {'56117', '56100'}]}
   # { 2nd smallest pixel count group shape: [[ 2nd smallest pixel count group shapes ], { shared large shapes } ] , ... }
   im1spixcShp_w_same_Lshapes = pickle.load(fp)
fp.close()
with open (spixcShp_w_same_Lshapes_dfile2, 'rb') as fp:
   im2spixcShp_w_same_Lshapes = pickle.load(fp)
fp.close()



shapes_intnl_s_pixcShp_dfile1 = top_shapes_dir + directory + "shapes/" + shapes_type + "/data/" + image_filename1 + "shapes.data"
shapes_intnl_s_pixcShp_dfile2 = top_shapes_dir + directory + "shapes/" + shapes_type + "/data/" + image_filename2 + "shapes.data"

with open (shapes_intnl_s_pixcShp_dfile1, 'rb') as fp:
   # { 'shapeid': [ pixel indexes ], ... }
   im1shapes = pickle.load(fp)
fp.close()
with open (shapes_intnl_s_pixcShp_dfile2, 'rb') as fp:
   # { 'shapeid': [ pixel indexes ], ... }
   im2shapes = pickle.load(fp)
fp.close()

last_results = []
for im1shapeid, im1spixcShp_n_Lshapes in im1spixcShp_w_same_Lshapes.items():
   # get all pixels of current im1spixcShp_w_same_Lshape
   cur_im1pixels = set()
   cur_im1pixels |= set( im1shapes[im1shapeid] )
   
   for im1spixcShp_n_Lshapes_iterator in range( 0, 2 ):
      for im1spixcShp_n_Lshape in im1spixcShp_n_Lshapes[ im1spixcShp_n_Lshapes_iterator ]:
         cur_im1pixels |= set( im1shapes[ im1spixcShp_n_Lshape ] )

   # [ 'image1shapeid', 'image2shapeid', match percentage ]
   cur_im1biggest_match = []
   for im2shapeid, im2spixcShp_n_Lshapes in im2spixcShp_w_same_Lshapes.items():
      # get all pixels of current im1spixcShp_w_same_Lshape
      cur_im2pixels = set()
      cur_im2pixels |= set( im2shapes[im2shapeid] )
   
      for im2spixcShp_n_Lshapes_iterator in range( 0, 2 ):
         for im2spixcShp_n_Lshape in im2spixcShp_n_Lshapes[ im2spixcShp_n_Lshapes_iterator ]:
            cur_im2pixels |= set( im2shapes[ im2spixcShp_n_Lshape ] )



      # check how many image1 pixels can be found in image2 pixels
      im1to2matched_pixels = cur_im1pixels.intersection( cur_im2pixels )
      im2to1matched_pixels = cur_im2pixels.intersection( cur_im1pixels )

      if len( im1to2matched_pixels ) >= len( cur_im1pixels ) * 0.8:
         match_percentage = len( im1to2matched_pixels ) / len( cur_im1pixels )
         cur_im1biggest_match.append( [ im1shapeid, im2shapeid, match_percentage ] )
      elif len( im2to1matched_pixels ) >= len( cur_im2pixels ) * 0.8:
         match_percentage = len( im1to2matched_pixels ) / len( cur_im2pixels )
         cur_im1biggest_match.append( [ im1shapeid, im2shapeid, match_percentage ] )
      
   if len( cur_im1biggest_match ) > 0:
      biggest_match_count = max ( [ match[2] for match in cur_im1biggest_match ] )
      biggest_match = [ match for match in cur_im1biggest_match if match[2] == biggest_match_count ]
      
      if len( biggest_match ) == 1:
         last_results.append( biggest_match[0] )
      else:
         print("ERROR biggest_match should contain only one element in this list")
         sys.exit()


with open(spixcShp_w_same_Lshapes_ddir + image_filename1 + "." + image_filename2 + ".data", 'wb') as fp:
   pickle.dump(last_results, fp)
fp.close()








