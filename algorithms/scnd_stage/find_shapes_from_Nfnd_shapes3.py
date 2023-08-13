
from libraries import  read_files_functions, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions, shapes_results_functions


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

shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
one_to_one_matched_dfile = shapes_m_types_dir + "data/matched_pixels.data"
with open (one_to_one_matched_dfile, 'rb') as fp:
      # image file num: [ ('57125', '57529'), ... ]
      # or 
      # image file num: [ [ [ [image1 shapes], [image2 shapes] ] ], ... ]
   one_to_one_m_shapes = pickle.load(fp)
fp.close()


def size_is_too_diff( param_im1shapeid, param_im2shapeid, param_im1shapes, param_im2shapes, size_num=1, len_provided=False ):
   # check if size is too different
   
   if len_provided is False:
      im1shapes_total = len( param_im1shapes[param_im1shapeid] )
      im2shapes_total = len( param_im2shapes[param_im2shapeid] )
   else:
      im1shapes_total = param_im1shapeid
      im2shapes_total = param_im2shapeid
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > size_num:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > size_num:
            return True

   return False     






result_matches = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
for each_files in all_matches_so_far:
   print(each_files)

   result_matches[each_files] = []
   
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


   im1shapes_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      
      for temp_p in im1shapes[shapeid]:
         im1shapes_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels   



   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   


   im2shape_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shape_by_pindex[temp_p] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels  

 

   im1shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im1file + "_shape_nbrs.txt"
   im2shape_neighbors_file = s_pixcShp_intnl_dir + "shape_nbrs/" + cur_im2file + "_shape_nbrs.txt"

   im1shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im1file, directory, im1shape_neighbors_file)
   im2shapes_neighbors = read_files_functions.rd_dict_k_v_l(cur_im2file, directory, im2shape_neighbors_file)

   im1shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im1file, directory, shapes_type=shapes_type, min_colors=True)
   im2shapes_colors = pixel_shapes_functions.get_all_shapes_colors(cur_im2file, directory, shapes_type=shapes_type, min_colors=True)


   for im1shapeid in im1shapes:
      if len( im1shapes[im1shapeid] ) < frth_smallest_pixc:
         continue
      
      check_not_found = [ temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[0] == im1shapeid ]
      
      if len( check_not_found ) == 0:
         # im1shapeid is not found yet
         # get im1shapeid's direct neighbor that is already matched from previous algorithms. make sure this neighbor has one to one match.
         # or combining or brokenUp that are turned into one to one by find_shapes_match_types.py algorithm.
         
         im1nbr_matches = [ ]
         matched = False
         for im1nbr in im1shapes_neighbors[ im1shapeid ]:
            if matched is True:
               continue
               
            _im1nbr_matches = [ temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[0] == im1nbr ]

            if len( _im1nbr_matches ) == 1:
               # one to one type of match
               im1nbr_matches.append( [ [ _im1nbr_matches[0][0] ], [ _im1nbr_matches[0][1] ] ] )
            
            elif len( _im1nbr_matches ) > 1:
               # combining or breakup type of match
               # [('57330', '57336'), ('57330', '44478'), ('57330', '45718')]

               temp_im2shapes = []
               for _im1nbr_match in _im1nbr_matches:
                  temp_im2shapes.append( _im1nbr_match[1] )
               
               im1nbr_matches.append( [ [ im1nbr ], temp_im2shapes ] )
                  
            
  
         # im1nbr_matches is now ready 
         # [[['77260'], ['79640']], [['79659'], ['79663', '64868']]]
         
         im2shapes_from_nbr_matches = []
         for im1nbr_match in im1nbr_matches:
            im2shapes_from_nbr_matches.extend( im1nbr_match[1] )
         
         for im1nbr_match in im1nbr_matches:
            for im2shape in im1nbr_match[1]:
            
               size_too_diff = size_is_too_diff( im1shapeid, im2shape, im1shapes, im2shapes, size_num=10 )
               if size_too_diff is True:
                  continue
               
               for possible_im2match in im2shapes_neighbors[ im2shape ]:
                  if len( im2shapes[ possible_im2match ] ) < frth_smallest_pixc or possible_im2match in im2shapes_from_nbr_matches:
                     continue

                  size_too_diff = size_is_too_diff( im1shapeid, possible_im2match, im1shapes, im2shapes, size_num=10 )
                  if size_too_diff is True:
                     continue
                 
                  im1shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[im1shapeid], im_width, param_shp_type=1 )  
                  im2shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[possible_im2match], im_width, param_shp_type=1 )  
                     
                  # matching from smaller shape.
                  if len( im1shapes[im1shapeid] ) > len( im2shapes[possible_im2match] ):
                     im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2shp_coord_xy, im1shp_coord_xy, match_threshold=0.25 )
                  else:
                     im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1shp_coord_xy, im2shp_coord_xy, match_threshold=0.25 )

                  if im1im2nbr_match is not True:                  
                     continue                  

                  verified = shapes_results_functions.verify_matches( [ (im1shapeid, possible_im2match ) ], [ im1shapes, im2shapes ], 
                             [ im1shapes_colors, im2shapes_colors ], [ im1shapes_neighbors, im2shapes_neighbors ], im_width, match_nbr_count=0.6 )
                  if len( verified ) >= 1:
                     result_matches[ each_files ].append( ( im1shapeid, possible_im2match ) )
                  



           



for each_files in result_matches:
   
   for each_shapes in result_matches[ each_files ]:
      
      matched_im1shape = each_shapes[0][-1]
      matched_im2shape = each_shapes[1][-1]
      
      if ( matched_im1shape, matched_im2shape ) not in all_matches_so_far[ each_files ]:
         all_matches_so_far[each_files].add( ( matched_im1shape, matched_im2shape ) )


possibe_matches_dir = top_shapes_dir + directory + scnd_stg_all_files + "/possible_matches/data/"
possibe_matches_file = possibe_matches_dir + "3.data"
if os.path.exists(possibe_matches_file):
   with open (possibe_matches_file, 'rb') as fp:
      prev_matched_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in prev_matched_shapes:
      if each_files in result_matches.keys():
         for each_shapes in prev_matched_shapes[each_files]:
            if each_shapes not in result_matches[each_files]:
               result_matches[each_files].append( each_shapes )
         
      else:
         result_matches[each_files] = prev_matched_shapes[each_files]   




with open(possibe_matches_file, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()
'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''















