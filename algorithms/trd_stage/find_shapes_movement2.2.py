
from libraries import  btwn_amng_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
from statistics import mean
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files
from libraries.cv_globals import scnd_stg_spixc_dir, scnd_stg_ch_btwn_frames_dir
from libraries import cv_globals

directory = "videos/street3/resized/min1"

if len( sys.argv ) >= 2:
   directory = sys.argv[1]

# directory is specified but does not contain /
if directory != "" and directory[-1] != '/':
   directory +='/'

shapes_dir = top_shapes_dir + directory  + "shapes/"


all_matches_ddir = top_shapes_dir + directory + "all_matches" + "/data/"
all_matches_dfile = all_matches_ddir + "1.data"
with open (all_matches_dfile, 'rb') as fp:
   acrs_all_files_shapes = pickle.load(fp)
fp.close()

all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes


if "min" in directory:
   min_colors = True
else:
   min_colors = False

result_shapes = {}

ref_imagefile_op = False
im_width = None
im_height = None
im_size = None

max_progress_num = len( all_matches_so_far )
cur_progress_num = len( all_matches_so_far )
prev_progress_num = len( all_matches_so_far )
remaining_chars = ""
for each_files in all_matches_so_far:
   remaining_chars = btwn_amng_files_functions.show_progress( max_progress_num, cur_progress_num, prev_progress_num, remaining_chars=remaining_chars )
   prev_progress_num = cur_progress_num
   cur_progress_num -= 1   
   
   
   result_shapes[each_files] = []
   
   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )

      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { 79999: [79999, ... ], ... }
      # { shapeid: [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()

   shapes_im2dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (shapes_im2dfile, 'rb') as fp:
      im2shapes = pickle.load(fp)
   fp.close()   

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, min_colors=min_colors)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, min_colors=min_colors)

   already_done = set()
   for each_shapes in all_matches_so_far[ each_files ]:
      if each_shapes in already_done:
         continue
      
      
      size_diff = same_shapes_functions.check_size_by_pixels( im1shapes[ each_shapes[0] ], im2shapes[ each_shapes[1] ], size_threshold=1 )
      if size_diff is False:
         # { pixel index: pixel color }
         app_im1shapes_pixels = {}
         app_im2shapes_pixels = {}
         for temp_pixel in im1shapes[ each_shapes[0] ]:
            app_im1shapes_pixels[temp_pixel] = im1shapes_colors[ each_shapes[0] ]
         for temp_pixel in im2shapes[ each_shapes[1] ]:
            app_im2shapes_pixels[temp_pixel] = im2shapes_colors[ each_shapes[1] ]

         # im1im2_match {8192, 8193, 8198, 8208, ... }. movement (0,0). movement ( right left, up down )
         im1im2_match, movement = same_shapes_functions.match_shape_while_moving_it2( app_im1shapes_pixels, app_im2shapes_pixels, im_size, min_colors, best_match=True )
         if len(im1im2_match) == 0:
            # partial match
            continue

         result_shapes[each_files].append( ( {each_shapes[0]}, {each_shapes[1]}, movement ) )


      found_shapes = { temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if each_shapes[0] == temp_shapes[0] or each_shapes[1] == temp_shapes[1] }
      if len(found_shapes) == 1:
         # this is already taken above
         continue
      
      # { pixel index: pixel color }
      app_im1shapes_pixels = {}
      app_im2shapes_pixels = {}
      
      app_im1shapeids = set()
      app_im2shapeids = set()
      for each_found_shapes in found_shapes:
         app_im1shapeids.add( each_found_shapes[0] )
         app_im2shapeids.add( each_found_shapes[1] )
         
         for temp_pixel in im1shapes[ each_found_shapes[0] ]:
            app_im1shapes_pixels[temp_pixel] = im1shapes_colors[ each_found_shapes[0] ]
         
         for temp_pixel in im2shapes[ each_found_shapes[1] ]:
            app_im2shapes_pixels[temp_pixel] = im2shapes_colors[ each_found_shapes[1] ]
         
      
      size_diff = same_shapes_functions.check_size_by_pixels( app_im1shapes_pixels, app_im2shapes_pixels, size_threshold=1 )
      if size_diff is True:
         continue
      
      # im1im2_match {8192, 8193, 8198, 8208, ... }. movement (0,0). movement ( right left, up down )
      im1im2_match, movement = same_shapes_functions.match_shape_while_moving_it2( app_im1shapes_pixels, app_im2shapes_pixels, im_size, min_colors, best_match=True )
      if len(im1im2_match) == 0:
         # partial match
         continue
      already_done |= found_shapes
      
      result_shapes[each_files].append( ( app_im1shapeids, app_im2shapeids, movement ) )


move_shapes_dfile = all_matches_ddir + "move_shapes2.data"
with open(move_shapes_dfile, 'wb') as fp:
   pickle.dump(result_shapes, fp)
fp.close()





'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''















