
from libraries import  read_files_functions, pixel_shapes_functions, pixel_functions, image_functions, btwn_amng_files_functions


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


across_all_files_dir = top_shapes_dir + directory + scnd_stg_all_files
relpos_nbr_dfile = across_all_files_dir + "/relpos_nbr/data/3.data"
with open (relpos_nbr_dfile, 'rb') as fp:
   relpos_nbr_shapes = pickle.load(fp)
fp.close()


shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
shapes_m_types_ddir = shapes_m_types_dir + "data/"
matched_pixels_dfile = shapes_m_types_ddir + "matched_pixels.data"
if os.path.exists( matched_pixels_dfile ):
   with open (matched_pixels_dfile, 'rb') as fp:
      shp_match_types = pickle.load(fp)
   fp.close()

else:
   shp_match_types = {}


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



relpos_matched_shapes = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_files in relpos_nbr_shapes:
   print(each_files)

   relpos_matched_shapes[each_files] = []

   cur_im1file = each_files.split(".")[0]
   cur_im2file = each_files.split(".")[1]

   if ref_imagefile_op is False:
      im1 = Image.open(top_images_dir + directory + cur_im1file + ".png" )
      im_size = im1.size
      im_width, im_height = im_size
      
      ref_imagefile_op = True

   shapes_dfile = shapes_dir + cur_im1file + "shapes.data"

   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im1shapes = pickle.load(fp)
   fp.close()   

   boundary_dir = top_shapes_dir + directory + "shapes/boundary/"
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


   done_matches = []
   for each_shapes in relpos_nbr_shapes[ each_files ]:
      if each_shapes in done_matches:
         continue
      
      if len( each_shapes[0] ) == 1:
         # target shape for getting all matches that contain this target shape
         same_shapes = [ temp_shapes for temp_shapes in relpos_nbr_shapes[ each_files ] if each_shapes[0] == temp_shapes[0] or 
                         each_shapes[0] in temp_shapes[0] ]


      elif len( each_shapes[1] ) == 1:
         # target shape for getting all matches that contain this target shape
         same_shapes = [ temp_shapes for temp_shapes in relpos_nbr_shapes[ each_files ] if each_shapes[1] == temp_shapes[1] or 
                         each_shapes[1] in temp_shapes[1] ]         
         
         
      else:
         print("ERROR in " + os.path.basename(__file__) + " there expected to be either one image1 shape or one image2 shape")
         sys.exit(1)


      '''
      best match calculation

      larger size the better match
      bigger the size difference the less match
         
      image1 size + image2 size = size total
      size total / 2 = average size
      size diff = abs( image1size - image2size )
      average size / size diff = size diff factor
      best match value = average size + ( size diff factor * size diff multiplier ) 
      '''
      best_match_value = None
      best_match = None
      for shapes_match in same_shapes:
            
         cur_im1shapes_len = 0
         for temp_im1shape in shapes_match[0]:
            cur_im1shapes_len += len( im1shapes[ temp_im1shape ] )
            
         cur_im2shapes_len = 0
         for temp_im2shape in shapes_match[1]:
            cur_im2shapes_len += len( im2shapes[ temp_im2shape ] )

         size_total = cur_im1shapes_len + cur_im2shapes_len
         size_average = size_total / 2
         size_diff = abs( cur_im1shapes_len - cur_im2shapes_len )
         if size_diff == 0:
            size_diff = 1
         size_diff_factor = size_average / size_diff            
         cur_match_value = size_average + ( size_diff_factor * 3 )
            
         if best_match is None:           
            best_match_value = cur_match_value
            best_match = shapes_match

         elif cur_match_value > best_match_value:
            best_match_value = cur_match_value
            best_match = shapes_match               
               
               
      done_matches.extend( same_shapes )
      relpos_matched_shapes[each_files].append( best_match )

      # putting best_match into shp_match_types
      temp_im1shapes_size = sum( [ len( im1shapes[ temp_shape ] ) for temp_shape in best_match[0] ] )
      temp_im2shapes_size = sum( [ len( im2shapes[ temp_shape ] ) for temp_shape in best_match[1] ] )

      _1to1size = check_if_1to1size( temp_im1shapes_size, temp_im2shapes_size, size_num=0.2, size_provided=True )
      if _1to1size is True:
         if each_files not in shp_match_types.keys():
            shp_match_types[ each_files ] = [best_match]
         else:
            if best_match not in shp_match_types[ each_files ]:
               shp_match_types[ each_files ].append( best_match )
         

      if len( best_match[0] ) == 1:
         for temp_im2shape in best_match[1]:
            if ( best_match[0][0], temp_im2shape ) not in all_matches_so_far[ each_files ]:
               all_matches_so_far[ each_files ].add( ( best_match[0][0], temp_im2shape ) )
         
      elif len( best_match[1] ) == 1:
         for temp_im1shape in best_match[0]:
            if  ( temp_im1shape, best_match[1][0] )  not in all_matches_so_far[ each_files ]:
               all_matches_so_far[ each_files ].add( ( temp_im1shape, best_match[1][0] ) )


relpos_nbr_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/data/"
relpos_nbr3_dfile = relpos_nbr_ddir + "verified3.data"
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


with open(matched_pixels_dfile, 'wb') as fp:
   pickle.dump(shp_match_types, fp)
fp.close()


with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()












