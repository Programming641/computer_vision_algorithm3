
from libraries import  cv_globals, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions, btwn_amng_files_functions


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


shapes_dir = top_shapes_dir + directory + "shapes/"

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



if "min" in directory:
   min_colors = True
else:
   min_colors = False


result_matches = {}
ref_imagefile_op = False
im_width = None
im_height = None
im_size = None
frth_smallest_pixc = None
for each_files in all_matches_so_far:
   print(each_files)

   result_matches[each_files] = []
   
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


   for im1shapeid in im1shapes:
      if len( im1shapes[im1shapeid] ) < frth_smallest_pixc:
         continue
      
      check_not_found = [ temp_shapes for temp_shapes in all_matches_so_far[ each_files ] if temp_shapes[0] == im1shapeid ]
      
      if len( check_not_found ) == 0:
         # im1shapeid is not found yet
         # get im1shapeid's direct neighbor that is already matched from previous algorithms. make sure this neighbor has one to one match.
         # or combining or brokenUp that are turned into one to one by find_shapes_match_types.py algorithm.
         
         im1nbr_matches = [ [], [] ]
         matched = False
         for im1nbr in im1shapes_neighbors[ im1shapeid ]:
            if matched is True:
               continue
               
            _1to1_im1nbr_matches = [ temp_shapes for temp_shapes in one_to_one_m_shapes[ each_files ] if type(temp_shapes) is tuple and 
                                     temp_shapes[0] == im1nbr ]

            if len( _1to1_im1nbr_matches ) > 1:
               print("one to one match should only have one pair for both image1 and image2 shape")
               sys.exit(1)
            elif len( _1to1_im1nbr_matches ) == 1:

               im1nbr_matches[0].append( [ im1nbr ] )
               im1nbr_matches[1].append( [ _1to1_im1nbr_matches[0][1] ] )

                  
            elif len( _1to1_im1nbr_matches ) == 0:

               multiple_shapes_matches = [ temp_shapes for temp_shapes in one_to_one_m_shapes[ each_files ] if type(temp_shapes) is list and
                                             im1nbr in temp_shapes[0] ]
               
               if len( multiple_shapes_matches ) >= 1:
                  for im1nbr_match in multiple_shapes_matches:
                     
                     im1nbr_matches[0].append( im1nbr_match[0] )
                     im1nbr_matches[1].append( im1nbr_match[1] )



            
            # im1nbr_matches is now ready.
            if len( im1nbr_matches[0] ) == 0:
               continue            
            
            for cur_im_index in range( 0, len( im1nbr_matches[0] ) ):
            
               cur_im1pixels = set()
               cur_im1shapes = []
            
               for _im1nbr_match in im1nbr_matches[0][ cur_im_index ]:
                  cur_im1pixels |= im1shapes[_im1nbr_match]
                  cur_im1shapes.append( _im1nbr_match )
            
               cur_im1shapes_boundaries =  pixel_shapes_functions.get_boundary_pixels( cur_im1pixels )    

               cur_im1pixels |= im1shapes[im1shapeid ]
               cur_im1shapes.append( im1shapeid )
             
               cur_im2pixels = set()
               cur_im2shapes = []
               already_done_im2nbrs = []

               for im2nbr_match in im1nbr_matches[1][ cur_im_index ]:
                  cur_im2pixels |= im2shapes[im2nbr_match]
                  cur_im2shapes.append( im2nbr_match )
                  
               cur_im2shapes_boundaries = pixel_shapes_functions.get_boundary_pixels( cur_im2pixels )
            
               for im2matched_nbr in im1nbr_matches[1][ cur_im_index ]:
                  for im2nbr in im2shapes_neighbors[ im2matched_nbr ]:
                     if len( im2shapes[im2nbr] ) < frth_smallest_pixc or im2nbr in im1nbr_matches[1][ cur_im_index ] or im2nbr in already_done_im2nbrs:
                        continue
                     
                     if min_colors is True:
                        if im1shapes_colors[ im1shapeid ] != im2shapes_colors[ im2nbr ]:
                           continue
                     
                     else:
                        appear_diff = pixel_functions.compute_appearance_difference(im1shapes_colors[ im1shapeid ] , im2shapes_colors[ im2nbr ] )
                        if appear_diff is True:
                           # different appearance
                           continue
                  
                     already_done_im2nbrs.append( im2nbr )
                  
                     size_diff = size_is_too_diff( im1shapeid, im2nbr, im1shapes, im2shapes)
                     if size_diff is True:
                        continue
                  
                     cur_im2pixels |= im2shapes[im2nbr]
                     cur_im2shapes.append( im2nbr )
                  
                     im1nbr_shp_coord_xy  = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im1pixels, im_width, param_shp_type=1 )  
                     im2nbr_shp_coord_xy = pixel_shapes_functions.get_shape_pos_in_shp_coord( cur_im2pixels, im_width, param_shp_type=1 )  
                     
                     # matching from smaller shape.
                     if len( cur_im1pixels ) > len( cur_im2pixels ):
                        im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2nbr_shp_coord_xy, im1nbr_shp_coord_xy, match_threshold=0.25 )
                     else:
                        im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im1nbr_shp_coord_xy, im2nbr_shp_coord_xy, match_threshold=0.25 )

                     if im1im2nbr_match is not True:                  
                        continue

                     result = pixel_shapes_functions.check_shape_attached_near( cur_im1shapes_boundaries, pixel_shapes_functions.get_boundary_pixels( im1shapes[im1shapeid] ),
                                                                             cur_im2shapes_boundaries, pixel_shapes_functions.get_boundary_pixels( im2shapes[im2nbr] ), im1.size )
                     if result is True:
                        matched = True
 
                        result_matches[each_files].append( ( cur_im1shapes, cur_im2shapes ) )
                        break
                  
                  if matched is True:
                     break               

               if matched is True:
                  break               
            
            if matched is True:
               break



for each_files in result_matches:
   
   for each_shapes in result_matches[ each_files ]:
      
      matched_im1shape = each_shapes[0][-1]
      matched_im2shape = each_shapes[1][-1]
      
      if ( matched_im1shape, matched_im2shape ) not in all_matches_so_far[ each_files ]:
         all_matches_so_far[each_files].add( ( matched_im1shape, matched_im2shape ) )



possibe_matches_dir = top_shapes_dir + directory + scnd_stg_all_files + "/possible_matches/data/"
if os.path.exists(possibe_matches_dir ) == False:
   os.makedirs(possibe_matches_dir )


possible_matches_dfile = possibe_matches_dir + "1.data"
if os.path.exists(possible_matches_dfile):
   with open (possible_matches_dfile, 'rb') as fp:
      prev_matched_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in prev_matched_shapes:
      if each_files in result_matches.keys():
         for each_shapes in prev_matched_shapes[each_files]:
            if each_shapes not in result_matches[each_files]:
               result_matches[each_files].append( each_shapes )
         
      else:
         result_matches[each_files] = prev_matched_shapes[each_files]   




with open(possible_matches_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()

'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''















