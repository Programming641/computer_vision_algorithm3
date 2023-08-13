
from libraries import  read_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions

from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil


from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files, frth_smallest_pixc, third_smallest_pixc

directory = sys.argv[1]
shapes_type = "intnl_spixcShp"


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



if shapes_type == "normal":
   print("ERROR. shapes_type normal is not supported")
   sys.exit()

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()


def is_it_1to1_in_size( param_shape1, param_shape2, len_provided=False ):
   if len_provided is False:
      im1shapes_total = len( param_shape1 )
      im2shapes_total = len( param_shape2 )
   elif len_provided is True:
      im1shapes_total = param_shape1
      im2shapes_total = param_shape2
      
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > 0.2:
           return False
      else:
         if im1_2pixels_diff / im1shapes_total > 0.2:
            return False  

   return True



all_shapes_pixels = {}
not_classified_shapes = {}

ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_files in all_matches_so_far:
   print(each_files)

   all_shapes_pixels[ each_files ] = []
   not_classified_shapes[ each_files ] = []
   

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

   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels  


   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)

   alrdy_included_shapes = []
   for each_shape in all_matches_so_far[each_files]:
   
      if each_shape in alrdy_included_shapes:
         continue
      
      _1to1_in_size_rslt = is_it_1to1_in_size( im1shapes[ each_shape[0] ], im2shapes[ each_shape[1] ] )
      if _1to1_in_size_rslt is True:
         # in terms of size, it is one to one type of match but to be really one to one type of match, image1 shape and 
         # image2 shape only matches with each other and not with other shapes.
         
         cur_im1_1to1_matches = [ temp_shapes for temp_shapes in all_matches_so_far[each_files] if temp_shapes[0] == each_shape[0] ]
         cur_im2_1to1_matches = [ temp_shapes for temp_shapes in all_matches_so_far[each_files] if temp_shapes[1] == each_shape[1] ]
         
         if len( cur_im1_1to1_matches ) == 1 and len( cur_im2_1to1_matches ) == 1:
            all_shapes_pixels[ each_files ].append( each_shape )

            continue

      
      # check for combining type of match
      cur_im2shp_matched_im1shapes = [ temp_shapes[0] for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[1] == each_shape[1] ]
      if len( cur_im2shp_matched_im1shapes ) > 1:
         
         
         _im1shapes_len = 0
         _im2shapes_len = 0
         
         for temp_im1shape in cur_im2shp_matched_im1shapes:
            _im1shapes_len += len( im1shapes[temp_im1shape] )
         
         _im2shapes_len = len( im2shapes[each_shape[1]] )
         
         _1to1_in_size_rslt = is_it_1to1_in_size( _im1shapes_len, _im2shapes_len, len_provided=True )
         if _1to1_in_size_rslt is True:

            all_shapes_pixels[ each_files ].append( [ cur_im2shp_matched_im1shapes, [ each_shape[1] ] ] )
           
            for im1shape in cur_im2shp_matched_im1shapes:
               alrdy_included_shapes.append( ( im1shape, each_shape[1] ) )

            continue

      
      # broken up into pieces type of match
      cur_im1shp_matched_im2shapes = [ temp_shapes[1] for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[0] == each_shape[0] ]
      if len( cur_im1shp_matched_im2shapes ) > 1:

         _im1shapes_len = 0
         _im2shapes_len = 0
         
         for temp_im2shape in cur_im1shp_matched_im2shapes:
            _im2shapes_len += len( im2shapes[temp_im2shape] )
         
         _im1shapes_len = len( im1shapes[each_shape[0]] )

         _1to1_in_size_rslt = is_it_1to1_in_size( _im1shapes_len, _im2shapes_len, len_provided=True )
         if _1to1_in_size_rslt is True:

            all_shapes_pixels[each_files].append( [ [each_shape[0]], cur_im1shp_matched_im2shapes ] )
            
            for im2shape in cur_im1shp_matched_im2shapes:
               alrdy_included_shapes.append( ( each_shape[0], im2shape ) )

            continue


      # if reached this far, it did not hit any of the match types above
      not_classified_shapes[each_files].append( each_shape )
         


shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
shapes_m_types_ddir = shapes_m_types_dir + "data/"
if os.path.exists(shapes_m_types_ddir ) == False:
   os.makedirs(shapes_m_types_ddir )


# removing duplicates
# duplicate types that exist in all_shapes_pixels
# ('57925', '58321'), [['57925'], ['58321']]
# [['57268', '56861'], ['58436']], [['57268', '56861'], ['58436']]
# [['59983'], ['57187', '59592', '53991', '53993']], [['59983'], ['53993', '59592', '57187', '53991']]
for each_files in all_shapes_pixels:
   cur_results = []
   
   duplicate_matches = []
   
   for each_shape in all_shapes_pixels[ each_files ]:
      if each_shape in duplicate_matches:
         continue
      
      for ano_each_shape in all_shapes_pixels[ each_files ]:

         if type( each_shape ) is tuple and type( ano_each_shape ) is list:
            if each_shape[0] in ano_each_shape[0] and each_shape[1] in ano_each_shape[1]:
               # tuple duplicate found. one is tuple and another is list and they contain the same shapes
               duplicate_matches.append( ano_each_shape )
               
               cur_results.append( each_shape )
               
         elif type( each_shape ) is list and type( ano_each_shape[0] ) is list:
            im1found_counter = 0
            im2found_counter = 0
            
            for temp_im1shape in each_shape[0]:
               if temp_im1shape in ano_each_shape[0]:
                  im1found_counter += 1
            for temp_im2shape in each_shape[1]:
               if temp_im2shape in ano_each_shape[1]:
                  im2found_counter += 1
            
            if len( each_shape[0] ) == im1found_counter and len( each_shape[1] ) == im2found_counter and \
               len( each_shape[0] ) == len( ano_each_shape[0] ) and len( each_shape[1] ) == len( ano_each_shape[1] ):
               
               cur_results.append( each_shape )
               duplicate_matches.append( ano_each_shape )
          
         elif type( each_shape ) is tuple and type( ano_each_shape ) is tuple:
            if each_shape == ano_each_shape:
               cur_results.append( each_shape )
          
         elif type( each_shape ) is list and type( ano_each_shape ) is tuple:
            # if list each_shape is the same as tuple ano_each_shape, this result is already taken when each_shape is tuple
            continue
   
   '''
   if len( all_shapes_pixels[ each_files ] ) == len( cur_results ):
      print("no duplicates found")
   else:
      print("duplicates found")
      all_shapes_pixels[ each_files ] = cur_results
   '''


matched_pixels_dfile = shapes_m_types_ddir + "matched_pixels.data"
with open(matched_pixels_dfile, 'wb') as fp:
   pickle.dump(all_shapes_pixels, fp)
fp.close()

not_classified_dfile = shapes_m_types_ddir + "not_classified.data"
with open(not_classified_dfile, 'wb') as fp:
   pickle.dump(not_classified_shapes, fp)
fp.close()










