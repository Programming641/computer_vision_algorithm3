# what is different from match_neighbor_by_relpos_shp_nbr.py is that this algorithm checks for break up into pieces type of match
# whereas match_neighbor_by_relpos_shp_nbr.py checks for one to one type of match
# 
# explanation of algorithm
#
# image1 shape and image1 shape's neighbor. image2 shape and image2 shape's neighbor
# Provided that image1 shape and image2 shape are the match.
# check if image1 shape's neighbor and image2 shape's neighbor is the match
# get average pixel of image1 shape and average pixel of image2 shape
# 
# take the larger neighbor as the one that needs to be matched with all smaller broken up shapes
# see if this larger neighbor pixels match 65% or more with all broken up pieces shapes
from libraries import cv_globals, pixel_shapes_functions, pixel_functions, image_functions, shapes_results_functions, btwn_amng_files_functions


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
   # {'10.11': {('79935', '58671'), ('39441', '39842'), ('45331', '36516')}, '11.12': {('39842', '40243'), ('26336', '27137'), ... }, ... }
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
one_to_one_matched_dfile = shapes_m_types_dir + "data/matched_pixels.data"
with open (one_to_one_matched_dfile, 'rb') as fp:
      # image file num: [ ('57125', '57529'), ... ]
      # or 
      # image file num: [ [ [ [image1 shapes], [image2 shapes] ] ], ... ]
   one_to_one_m_shapes = pickle.load(fp)
fp.close()

shapes_dir = top_shapes_dir + directory  + "shapes/"

def check_if_1to1size( param_shape1, param_shape2, size_num=1, size_provided=False ):
   if size_provided is False:
      im1shapes_total = len( param_shape1 )
      im2shapes_total = len( param_shape2 )
   else:
      im1shapes_total = param_shape1
      im2shapes_total = param_shape2
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_num:
           return False
      else:
         if im1_2pixels_diff / im1shapes_total > size_num:
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
      im1shapeids_by_pindex = pickle.load(fp)
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

   shp_by_index_dfile2 = shp_by_index_dir + cur_im2file + ".data"
   with open (shp_by_index_dfile2, 'rb') as fp:
      # { pindex: { shapeids }, ... }
      im2shapeids_by_pindex = pickle.load(fp)
   fp.close()      

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
     
      _1to1im1shapes = []
      _1to1im2shapes = []
      if type( each_shape ) is tuple:
         _1to1im1shapes.append( each_shape[0] )
         _1to1im2shapes.append( each_shape[1] )

      else:
         # temp_shapes -> [ [image1 shapes], [image2 shapes] ]
         _1to1im1shapes.extend( each_shape[0] )
         _1to1im2shapes.extend( each_shape[1] )

      _im1neighbors = []
      _im2neighbors = []
      _1to1im1shapes_pixels = set()
      _1to1im2shapes_pixels = set()
      for temp_shape in _1to1im1shapes:
         _1to1im1shapes_pixels |= im1shapes[ temp_shape ]
         for temp_nbr in im1shapes_neighbors[ temp_shape ]:
            _im1neighbors.append( temp_nbr )

      for temp_shape in _1to1im2shapes:
         _1to1im2shapes_pixels |= im2shapes[ temp_shape ]      
         for temp_nbr in im2shapes_neighbors[ temp_shape ]:
            _im2neighbors.append( temp_nbr )

      # ( x,y )
      im1shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( _1to1im1shapes_pixels , im_width, pixel_xy=True )
      # rounding to whole number
      im1shape_average_pix = ( round( im1shape_average_pix[0] ), round( im1shape_average_pix[1] ) )
      im2shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( _1to1im2shapes_pixels , im_width, pixel_xy=True )
      im2shape_average_pix = ( round( im2shape_average_pix[0] ), round( im2shape_average_pix[1] ) )


      for cur_im1shp_nbr in _im1neighbors:
         if len( im1shapes[cur_im1shp_nbr] ) < frth_smallest_pixc or cur_im1shp_nbr in _1to1im1shapes:
            continue
         

         # see if image1 neighbor matches with image2 neighbor
         # found_im2shapes -> { shapeid: how many pixels have been found for this shape, ... }
         found_im2shapes = {}
         skipped_pixels = 0
         debug_im2pixels = set()
         for cur_im1nbr_pix in im1shapes[cur_im1shp_nbr]:
               
            diff_x = cur_im1nbr_pix[0] - im1shape_average_pix[0]
            diff_y = cur_im1nbr_pix[1] - im1shape_average_pix[1]
               
            im2_relpos_pix = ( im2shape_average_pix[0] + diff_x, im2shape_average_pix[1] + diff_y )

            if im2_relpos_pix[0] >= im_width or im2_relpos_pix[0] < 0:
               # pixel out of image range
               skipped_pixels += 1
               continue
            if im2_relpos_pix[1] < 0 or im2_relpos_pix[1] >= im_height:
               skipped_pixels += 1
               continue
            
            debug_im2pixels.add( im2_relpos_pix )
            im2_relpos_pix = pixel_functions.convert_xy_to_pindex( im2_relpos_pix, im_width )

            # get image2 shape that has im2_relpos_pix
            for temp_shapeid in im2shapeids_by_pindex[im2_relpos_pix]:
               if temp_shapeid not in found_im2shapes.keys():
                  found_im2shapes[ temp_shapeid ] = 1
               else:
                  found_im2shapes[ temp_shapeid ] += 1            
            

         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [cur_im1shp_nbr], save_filepath=None , shapes_rgb=(255,0,0) )
         #image_functions.cr_im_from_pixels( cur_im2file, directory, debug_im2pixels, save_filepath=None , pixels_rgb=(0,0,255) )
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, list( found_im2shapes.keys() ), save_filepath=None , shapes_rgb=None )

         found_im2shapes_size = 0
         matched_im2shapes = []
         im1neighbor_len = len( im1shapes[ cur_im1shp_nbr ] )
         for temp_im2shape in found_im2shapes:
            if min_colors is True:
               if im1shapes_colors[ cur_im1shp_nbr ] != im2shapes_colors[ temp_im2shape ]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(im1shapes_colors[ cur_im1shp_nbr ] , im2shapes_colors[ temp_im2shape ] )
               if appear_diff is True:
                  # different appearance
                  continue
            
            if found_im2shapes[temp_im2shape] / len( im2shapes[ temp_im2shape ] ) >= 0.4:
               found_im2shapes_size += len( im2shapes[ temp_im2shape ] )
               matched_im2shapes.append( temp_im2shape )

         if found_im2shapes_size / im1neighbor_len >= 0.63:         
            _1to1size = check_if_1to1size( found_im2shapes_size, im1neighbor_len, size_num=1.2, size_provided=True )
            if _1to1size is True:
               if [ [cur_im1shp_nbr], matched_im2shapes ] not in relpos_matched_shapes[each_files]:
                  relpos_matched_shapes[each_files].append( [ [cur_im1shp_nbr], matched_im2shapes ] )


         im1nbr_matched_pixels = 0
         matched_im2shapes = []
         for found_im2shape in found_im2shapes:
            if min_colors is True:
               if im1shapes_colors[ cur_im1shp_nbr ] != im2shapes_colors[ found_im2shape ]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(im1shapes_colors[ cur_im1shp_nbr ], im2shapes_colors[ found_im2shape ] )
               if appear_diff is True:
                  # different appearance
                  continue


            if ( cur_im1shp_nbr, found_im2shape ) in all_matches_so_far[each_files]:
               continue

            
            # check if 60% or more pixels matched
            if found_im2shapes[found_im2shape] / len( im2shapes[found_im2shape] ) >= 0.6:
               matched_im2shapes.append( found_im2shape )
               im1nbr_matched_pixels += found_im2shapes[found_im2shape]
               
               #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, [ found_im2shape ], save_filepath=None , shapes_rgb=None )


         # lastly check if enough pixels of cur_im1shp_nbr have been matched

         # be lenient on matching for the amount of pixels skipped
         if ( im1nbr_matched_pixels + ( skipped_pixels / 10 ) ) / len( im1shapes[ cur_im1shp_nbr ] ) >= 0.6:
            # match is found. add all matched image2 shapes

            if [ [cur_im1shp_nbr], matched_im2shapes ] not in relpos_matched_shapes[ each_files ]:
               relpos_matched_shapes[each_files].append( [ [cur_im1shp_nbr], matched_im2shapes ] )


      #  --------------           looking for combining type of shapes. pieces shape combine to become the bigger shape in the next image        ----------------
      for cur_im2shp_nbr in _im2neighbors:
         if len( im2shapes[cur_im2shp_nbr] ) < frth_smallest_pixc or cur_im2shp_nbr in _1to1im2shapes:
            continue
         
         #image_functions.cr_im_from_shapeslist2( cur_im2file, directory, ["59292"], save_filepath=None , shapes_rgb=None )

         # see if image2 neighbor matches with image1 neighbor
         # found_im1shapes -> { shapeid: how many pixels have been found for this shape, ... }
         found_im1shapes = {}
         skipped_pixels = 0
         
         debug_im1pixels = []
         for cur_im2nbr_pix in im2shapes[cur_im2shp_nbr]:
               
            diff_x = cur_im2nbr_pix[0] - im2shape_average_pix[0]
            diff_y = cur_im2nbr_pix[1] - im2shape_average_pix[1]
               
            im1_relpos_pix = ( im1shape_average_pix[0] + diff_x, im1shape_average_pix[1] + diff_y )

            if im1_relpos_pix[0] >= im_width or im1_relpos_pix[0] < 0:
               # pixel out of image range
               skipped_pixels += 1
               continue
            if im1_relpos_pix[1] < 0 or im1_relpos_pix[1] >= im_height:
               skipped_pixels += 1
               continue
            
            debug_im1pixels.append( im1_relpos_pix )
            
            im1_relpos_pix = pixel_functions.convert_xy_to_pindex( im1_relpos_pix, im_width )

            # get image1 shape that has im1_relpos_pix
            for temp_shapeid in im1shapeids_by_pindex[im1_relpos_pix]:

               if temp_shapeid not in found_im1shapes.keys():
                  found_im1shapes[ temp_shapeid ] = 1
               else:
                  found_im1shapes[ temp_shapeid ] += 1            
            
         
         #image_functions.cr_im_from_pixels( cur_im1file, directory, debug_im1pixels, save_filepath=None , pixels_rgb=None )
         #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, list( found_im1shapes.keys() ), save_filepath=None , shapes_rgb=None )


         found_im1shapes_size = 0
         matched_im1shapes = []
         im2neighbor_len = len( im2shapes[ cur_im2shp_nbr ] )
         for temp_im1shape in found_im1shapes:
            if min_colors is True:
               if im2shapes_colors[ cur_im2shp_nbr ] != im1shapes_colors[ temp_im1shape ]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(im2shapes_colors[ cur_im2shp_nbr ], im1shapes_colors[ temp_im1shape ] )
               if appear_diff is True:
                  # different appearance
                  continue
            
            if found_im1shapes[temp_im1shape] / len( im1shapes[temp_im1shape] ) >= 0.4:
               found_im1shapes_size += len( im1shapes[ temp_im1shape ] )
               matched_im1shapes.append( temp_im1shape )
         
         if found_im1shapes_size / im2neighbor_len >= 0.63:
            _1to1size = check_if_1to1size( found_im1shapes_size, im2neighbor_len, size_num=1.2, size_provided=True )
            if _1to1size is True:
               if [ matched_im1shapes, [cur_im2shp_nbr] ] not in relpos_matched_shapes[each_files]:
                  relpos_matched_shapes[each_files].append( [ matched_im1shapes, [cur_im2shp_nbr] ] )
               
               #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [ temp_im1shape ], save_filepath=None , shapes_rgb=None )


         im2nbr_matched_pixels = 0
         matched_im1shapes = []
         for found_im1shape in found_im1shapes:
            if min_colors is True:
               if im2shapes_colors[ cur_im2shp_nbr ] != im1shapes_colors[ found_im1shape ]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference( im2shapes_colors[ cur_im2shp_nbr ], im1shapes_colors[ found_im1shape ] )
               if appear_diff is True:
                  # different appearance
                  continue

            if ( found_im1shape, cur_im2shp_nbr ) in all_matches_so_far[each_files]:
               continue

            
            # check if 60% or more pixels matched
            if found_im1shapes[found_im1shape] / len( im1shapes[found_im1shape] ) >= 0.6:
               matched_im1shapes.append( found_im1shape )
               im2nbr_matched_pixels += found_im1shapes[found_im1shape]
               
               #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [ found_im1shape ], save_filepath=None , shapes_rgb=None )
            

         # lastly check if enough pixels of cur_im2shp_nbr have been matched

         # be lenient on matching for the amount of pixels skipped
         if ( im2nbr_matched_pixels + ( skipped_pixels / 10 ) ) / len( im2shapes[ cur_im2shp_nbr ] ) >= 0.6:
            # match is found. add all matched image2 shapes
            
            if [ matched_im1shapes, [cur_im2shp_nbr] ] not in relpos_matched_shapes[each_files]:
               #image_functions.cr_im_from_shapeslist2( cur_im1file, directory, [ matched_im1shape ], save_filepath=None , shapes_rgb=None )
               relpos_matched_shapes[each_files].append( [ matched_im1shapes, [cur_im2shp_nbr] ] )


   results_shapes = []
   for temp_matched_shapes in relpos_matched_shapes[ each_files ]:
      matched_shapes = shapes_results_functions.rm_vsmall_isolated_shapes( temp_matched_shapes, [ im1shapes, im2shapes ],
                       [ im1shapes_boundaries, im2shapes_boundaries ], [ im1shapeids_by_pindex, im2shapeids_by_pindex ], im_size)

      if len( matched_shapes[0] ) >= 1 and len( matched_shapes[1] ) >= 1:
         results_shapes.append( matched_shapes )
         
   relpos_matched_shapes[ each_files ] = results_shapes


   if len( relpos_matched_shapes[each_files] ) == 0:
      relpos_matched_shapes.pop(each_files) 













relpos_nbr_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/data/"
relpos_nbr3_dfile = relpos_nbr_ddir + "3.data"
if os.path.exists( relpos_nbr3_dfile ):
   with open (relpos_nbr3_dfile, 'rb') as fp:
      relpos_shp_nbr3 = pickle.load(fp)
   fp.close()

   for each_files in relpos_shp_nbr3:
      if each_files not in relpos_matched_shapes.keys():
         relpos_matched_shapes[ each_files ] = relpos_shp_nbr3[ each_files ]
      
      else:
         for each_shapes in relpos_shp_nbr3[ each_files ]:
            if each_shapes not in relpos_matched_shapes[ each_files ]:
               relpos_matched_shapes[ each_files ].append( each_shapes )


with open(relpos_nbr3_dfile, 'wb') as fp:
   pickle.dump(relpos_matched_shapes, fp)
fp.close()











