# this is after executing algorithms/scnd_stage/cross_check_all_LL_algo_acrs_cur_files.py
# and cross_check_all_low_level_algo_acrs_all_files.py
# and algorithms/scnd_stage/find_missing_shapes.py
#
# this algorithm is used only for one-one matched shapes. that is, any other matches like "combining in the next image" or 
# "break up into pieces", this algorithm can not be applied to.
# 
# explanation of algorithm
#
# Shapes in this algorithm. 
# image1 shape and image1 shape's neighbor. image2 shape and image2 shape's neighbor
# Provided that image1 shape and image2 shape are the match.
#
# check if image1 shape's neighbor and image2 shape's neighbor is the match
# get center pixel of image1 shape and center pixel of image2 shape
# see if the pixel of image1 shape's neighbor is in the image2 shape's neighbor
# if 60% or more of pixels found, then both neighbors are the match
#
# this is for one-to-one type of match
from libraries import  cv_globals, pixel_shapes_functions, pixel_functions, btwn_amng_files_functions

import tkinter
from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files

directory = sys.argv[1]

if directory != "" and directory[-1] != '/':
   directory +='/'

across_all_files_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/data/"
across_all_files_dfile = across_all_files_ddir + "all_files.data"
with open (across_all_files_dfile, 'rb') as fp:
   # {'10.11': [('79935', '58671'), ('39441', '39842'), ('45331', '36516')], '11.12': [('39842', '40243'), ('26336', '27137'), ... ], ... }
   acrs_all_files_shapes = pickle.load(fp)
fp.close()

all_matches_so_far_dfile = across_all_files_ddir + "all_matches.data"
if os.path.exists( all_matches_so_far_dfile ):
   with open (all_matches_so_far_dfile, 'rb') as fp:
      all_matches_so_far = pickle.load(fp)
   fp.close()

else:
   all_matches_so_far = acrs_all_files_shapes


shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
shapes_m_types_ddir = shapes_m_types_dir + "data/"
matched_pixels_dfile = shapes_m_types_ddir + "matched_pixels.data"
matched_pixels_dfile
with open (matched_pixels_dfile, 'rb') as fp:
   one_to_one_m_shapes = pickle.load(fp)
fp.close()

shapes_dir = top_shapes_dir + directory + "shapes/"


def check_if_1to1size( param_shape1, param_shape2, size_threshold=0.5 ):
   im1shapes_total = len( param_shape1 )
   im2shapes_total = len( param_shape2 )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_threshold:
           return False
      else:
         if im1_2pixels_diff / im1shapes_total > size_threshold:
            return False  

   return True


if "min" in directory:
   min_colors = True
else:
   min_colors = False

shp_by_index_dir = shapes_dir + 'shapeids_by_pindex/'


relpos_matched_shapes = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
frth_smallest_pixc = None
for each_files in all_matches_so_far:
   print(each_files)

   relpos_matched_shapes[each_files] = []

   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im_size = im1.size
      im_width, im_height = im_size
      
      frth_smallest_pixc = cv_globals.get_frth_smallest_pixc( im_size )
      
      ref_imagefile_op = True

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()   

   boundary_dir = shapes_dir + "boundary/"
   boundary_dfile = boundary_dir + cur_im1file + ".data"
   with open (boundary_dfile, 'rb') as fp:
      im1shapes_boundaries = pickle.load(fp)
   fp.close()

   for shapeid in im1shapes:
      cur_pixels = set()
      
      for temp_p in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels

   shp_by_index_dfile = shp_by_index_dir + cur_im1file + ".data"
   with open (shp_by_index_dfile, 'rb') as fp:
      # { pindex: { shapeids }, ... }
      im1shapes_by_pindex = pickle.load(fp)
   fp.close()   

   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   

   boundary_dfile2 = boundary_dir + cur_im2file + ".data"
   with open (boundary_dfile2, 'rb') as fp:
      im2shapes_boundaries = pickle.load(fp)
   fp.close()


   for shapeid in im2shapes:
      cur_pixels = set()
      for temp_p in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels
    

   im1shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.data"
   im2shape_neighbors_file = shapes_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.data"

   with open (im1shape_neighbors_file, 'rb') as fp:
      im1shapes_neighbors = pickle.load(fp)
   fp.close()   

   with open (im2shape_neighbors_file, 'rb') as fp:
      im2shapes_neighbors = pickle.load(fp)
   fp.close()   

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, min_colors=min_colors)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, min_colors=min_colors)

   for each_shape in one_to_one_m_shapes[each_files]:
      # each_shape -> ('57125', '57529') or [ [image1 shapes], [image2 shapes] ]  
      
      cur_im1shapes = set()
      cur_im2_shapes = set()
      if type( each_shape ) is tuple:
         cur_im1shapes.add( each_shape[0] )
         cur_im2_shapes.add( each_shape[1] )
      else:
         for temp_im1shape in each_shape[0]:
            cur_im1shapes.add( temp_im1shape )
         for temp_im2shape in each_shape[1]:
            cur_im2_shapes.add( temp_im2shape )
      
      for temp_im1shape in cur_im1shapes:
         for cur_im1shp_nbr in im1shapes_neighbors[ temp_im1shape ]:
            if len( im1shapes[cur_im1shp_nbr] ) < frth_smallest_pixc:
               continue

            for temp_im2shape in cur_im2_shapes:
               for cur_im2shp_nbr in im2shapes_neighbors[ temp_im2shape ]:
                  if len( im2shapes[cur_im2shp_nbr] ) < frth_smallest_pixc:
                     continue
                  
                  if min_colors is True:
                     if im1shapes_colors[ cur_im1shp_nbr ] != im2shapes_colors[ cur_im2shp_nbr ]:
                        continue
                  else:
                     appear_diff = pixel_functions.compute_appearance_difference(im1shapes_colors[ cur_im1shp_nbr ] , im2shapes_colors[ cur_im2shp_nbr ] )
                     if appear_diff is True:
                        # different appearance
                        continue

            
                  if ( cur_im1shp_nbr, cur_im2shp_nbr ) in relpos_matched_shapes[each_files]:
                     # already added
                     continue
            
                  if ( cur_im1shp_nbr, cur_im2shp_nbr ) in all_matches_so_far[each_files]:
                     continue
      
      
                  # check if this is one-one type of match
                  size_within_threshold = check_if_1to1size( im1shapes[ cur_im1shp_nbr ], im2shapes[ cur_im2shp_nbr ], size_threshold=1 )    
                  if size_within_threshold is False:
                     continue

                  debug_im2nbr_relpos_pix = []

                  # ( x,y )
                  im1shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( im1shapes[ temp_im1shape ] , im_width, pixel_xy=True )
                  im1shape_average_pix = ( round( im1shape_average_pix[0] ), round( im1shape_average_pix[1] ) )
                  im2shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( im2shapes[ temp_im2shape ] , im_width, pixel_xy=True )
                  im2shape_average_pix = ( round( im2shape_average_pix[0] ), round( im2shape_average_pix[1] ) )

                  # see if image1 neighbor matches with image2 neighbor. check for one-one type of match or break up into pieces type of match.
                  # but not combining type of match.
                  cur_im2nbr_m_count = 0
                  for cur_im1nbr_pix in im1shapes[cur_im1shp_nbr]:
               
                     diff_x = cur_im1nbr_pix[0] - im1shape_average_pix[0]
                     diff_y = cur_im1nbr_pix[1] - im1shape_average_pix[1]
               
                     im2nbr_relpos_pix = ( im2shape_average_pix[0] + diff_x, im2shape_average_pix[1] + diff_y )
                     if im2nbr_relpos_pix[0] >= im_width or im2nbr_relpos_pix[0] < 0:
                        # pixel out of image range
                        continue
                     if im2nbr_relpos_pix[1] < 0 or im2nbr_relpos_pix[1] >= im_height:
                        continue
               
                     debug_im2nbr_relpos_pix.append( im2nbr_relpos_pix )
               
                     if im2nbr_relpos_pix in im2shapes[ cur_im2shp_nbr ]:
                        cur_im2nbr_m_count += 1
            
                  if cur_im2nbr_m_count / len( im1shapes[cur_im1shp_nbr] ) > 0.6:
                     # now check attachment
                     result =   pixel_shapes_functions.check_shape_attached_near( im1shapes_boundaries[ temp_im1shape ], im1shapes_boundaries[cur_im1shp_nbr], im2shapes_boundaries[ temp_im2shape ],
                                                                 im2shapes_boundaries[cur_im2shp_nbr], im1.size )

                     if result is True:
                        relpos_matched_shapes[each_files].append( ( cur_im1shp_nbr, cur_im2shp_nbr ) )
                  
                        if len( im1shapes[cur_im1shp_nbr] ) < len( im2shapes[cur_im2shp_nbr] ):
                           # size is within one to one match threshold but image2 shape is bigger. so make sure to get all image1 shapes
                           # that are inside the superimposed image2 shapes.
                     
                           im1shapes_at_superimposed_pix = {}
                           for cur_im2nbr_pix in im2shapes[cur_im2shp_nbr]:
               
                              diff_x = cur_im2nbr_pix[0] - im2shape_average_pix[0]
                              diff_y = cur_im2nbr_pix[1] - im2shape_average_pix[1]
                
                              # image1 superimposed pixel
                              im1nbr_relpos_pix = ( im1shape_average_pix[0] + diff_x, im1shape_average_pix[1] + diff_y )
                              if im1nbr_relpos_pix[0] >= im_width or im1nbr_relpos_pix[0] < 0:
                                 # pixel out of image range
                                 continue
                              if im1nbr_relpos_pix[1] < 0 or im1nbr_relpos_pix[1] >= im_height:
                                 continue                     
                        
                              pindex = pixel_functions.convert_xy_to_pindex( im1nbr_relpos_pix, im_width )
                        
                              for cur_im1shape in im1shapes_by_pindex[pindex]:
                                 if cur_im1shape in im1shapes_at_superimposed_pix.keys():
                                    im1shapes_at_superimposed_pix[cur_im1shape] += 1
                                 else:
                                    im1shapes_at_superimposed_pix[cur_im1shape] = 1
                    
                     
                           for temp_im1shapeid in im1shapes_at_superimposed_pix:
                              if im1shapes_at_superimposed_pix[temp_im1shapeid] >= len( im1shapes[temp_im1shapeid] ) * 0.6:
                                 relpos_matched_shapes[each_files].append( ( temp_im1shapeid, cur_im2shp_nbr ) )


   if len( relpos_matched_shapes[each_files] ) == 0:
      relpos_matched_shapes.pop(each_files)


# first, put current execution results into all_matches_so_far
for each_files in relpos_matched_shapes:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = relpos_matched_shapes[ each_files ]
      
   else:
      for each_shapes in relpos_matched_shapes[ each_files ]:
         if each_shapes not in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].add( each_shapes )


# add previous execution results into current results
relpos_shp_nbr2_dfile = across_all_files_ddir + "verified2.data"
if os.path.exists( relpos_shp_nbr2_dfile ):
   with open (relpos_shp_nbr2_dfile, 'rb') as fp:
      # {'11.12': [('37380', '26582'), ... ], ... }
      relpos_shp_nbr2 = pickle.load(fp)
   fp.close()
   
   for each_files in relpos_shp_nbr2:
      if each_files not in relpos_matched_shapes.keys():
         relpos_matched_shapes[ each_files ] = relpos_shp_nbr2[ each_files ]
      
      else:
         for each_shapes in relpos_shp_nbr2[ each_files ]:
            if each_shapes not in relpos_matched_shapes[ each_files ]:
               relpos_matched_shapes[ each_files ].append( each_shapes )



relpos_shp_nbr_match_file = across_all_files_ddir + "verified2.data"
with open(relpos_shp_nbr_match_file, 'wb') as fp:
   pickle.dump(relpos_matched_shapes, fp)
fp.close()

with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()













