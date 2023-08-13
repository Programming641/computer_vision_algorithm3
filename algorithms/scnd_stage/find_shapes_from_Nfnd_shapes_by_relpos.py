
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


shapes_m_types_dir = top_shapes_dir + directory + scnd_stg_all_files + "/shp_match_types/"
one_to_one_matched_dfile = shapes_m_types_dir + "data/matched_pixels.data"
with open (one_to_one_matched_dfile, 'rb') as fp:
      # image file num: [ ('57125', '57529'), ... ]
      # or 
      # image file num: [ [ [image1 shapes], [image2 shapes] ], ... ]
   one_to_one_m_shapes = pickle.load(fp)
fp.close()


if shapes_type == "normal":
   print("ERROR. shapes_type normal is not supported")
   sys.exit()

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/" + internal + "/"
   
   shapes_dir = s_pixcShp_intnl_dir + "shapes/"


else:
   print("ERROR at " + str( os.path.basename(__file__) ) + " shapes_type " + shapes_type + " is not supported")
   sys.exit()



def size_is_too_diff( param_im1shapeid, param_im2shapeid, param_im1shapes, param_im2shapes, size_num=1 ):
   # check if size is too different
   im1shapes_total = len( param_im1shapes[param_im1shapeid] )
   im2shapes_total = len( param_im2shapes[param_im2shapeid] )
      
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

   result_matches[each_files] = set() 

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

   im1shapes_boundaries = {}
   im1shapes_by_pindex = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      
      for temp_p in im1shapes[shapeid]:
         im1shapes_by_pindex[ temp_p ] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels   
      im1shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_pixels )


   im2shapes_dfile = shapes_dir + cur_im2file + "shapes.data"
   with open (im2shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im2shapes = pickle.load(fp)
   fp.close()   

   im2shapes_boundaries = {}
   im2shapes_by_pindex = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         im2shapes_by_pindex[temp_p] = shapeid
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels  
      im2shapes_boundaries[shapeid] = pixel_shapes_functions.get_boundary_pixels( cur_pixels )



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
      
      found_nearest_matched_nbr = None
      if len( check_not_found ) == 0:
         # im1shapeid is not found yet
         # get im1shapeid's nearest found neighbor. make sure this neighbor has one to one match.
         # this algorithm only works if the neighbor moved the same as the im1shapeid
         vicinity_counter = 1
         vicinity_limit = 15
         matched = False
         done_near_matches = []
         while vicinity_counter <= vicinity_limit and matched is False:
            # {(231, 63), (244, 82), ... }
            vicinity_pixels = pixel_shapes_functions.get_shape_vicinity_pixels( im1shapes_boundaries[im1shapeid], vicinity_counter, im_size, param_shp_type=1 )
            vicinity_counter += 1
            
            pindexes = [ pixel_functions.convert_xy_to_pindex( pixel, im_width ) for pixel in vicinity_pixels ]
            near_im1shapes = set()
            for pindex in pindexes:
               near_im1shapes.add( im1shapes_by_pindex[ str( pindex ) ] )
            
            for near_im1shape in near_im1shapes:
               if matched is True:
                  break
               
               found_nearest_matched_nbr = [ temp_shapes for temp_shapes in one_to_one_m_shapes[ each_files ] if ( type( temp_shapes ) is tuple and temp_shapes[0] == near_im1shape ) or
                             ( type( temp_shapes[0] ) is list and near_im1shape in temp_shapes[0] ) ]
               
               if len( found_nearest_matched_nbr ) >= 1:
                  skip = False
                  for each_nearest_match in found_nearest_matched_nbr:
                     if each_nearest_match in done_near_matches:
                        skip = True
                        break
                  
                  if skip is True:
                     continue
                  
                  done_near_matches.extend( found_nearest_matched_nbr )

                  # found_nearest_matched_nbr -> [[['39782', '37774', '38183', '34575'], ['38185']], [['38183'], ['38185', '27385']]]
                  im1shapes_pixels = set()
                  im2shapes_pixels = set()
                  
                  for each_found_nbr in found_nearest_matched_nbr:
                     if matched is True:
                        break
            
                     if type( each_found_nbr[0] ) is str:
                        im1shapes_pixels |= im1shapes[ each_found_nbr[0] ]
                     else:
                        for temp_im1shape in each_found_nbr[0]:
                           im1shapes_pixels |= im1shapes[ temp_im1shape ]   
                  
                     if type( each_found_nbr[1] ) is str:
                        im2shapes_pixels |= im2shapes[ each_found_nbr[1] ]
                     else:
                        for temp_im2shape in each_found_nbr[1]:
                           im2shapes_pixels |= im2shapes[ temp_im2shape ]
            
                     #image_functions.cr_im_from_pixels( cur_im1file, directory, im1shapes_pixels, save_filepath=None , pixels_rgb=None )
                     #image_functions.cr_im_from_pixels( cur_im2file, directory, im2shapes_pixels, save_filepath=None , pixels_rgb=None )

                     # now, I found nearest matched neighbor
                     im1shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( im1shapes_pixels , im_width, pixel_xy=True )
                     # rounding to whole number
                     im1shape_average_pix = ( round( im1shape_average_pix[0] ), round( im1shape_average_pix[1] ) )
                     im2shape_average_pix = pixel_shapes_functions.get_shape_average_pixel( im2shapes_pixels , im_width, pixel_xy=True )
                     im2shape_average_pix = ( round( im2shape_average_pix[0] ), round( im2shape_average_pix[1] ) )        
         
                     debug_pixels = set()
                     im2shapes_in_relpos = {}
                     for im1not_found_shape_pix in im1shapes[im1shapeid]:
               
                        diff_x = im1not_found_shape_pix[0] - im1shape_average_pix[0]
                        diff_y = im1not_found_shape_pix[1] - im1shape_average_pix[1]
                  
                        relpos_pix = ( im2shape_average_pix[0] + diff_x, im2shape_average_pix[1] + diff_y )
   
                        if relpos_pix[0] >= im_width or relpos_pix[0] < 0:
                           # pixel out of image range
                          continue
                        if relpos_pix[1] < 0 or relpos_pix[1] >= im_height:
                           continue
            
                        debug_pixels.add( relpos_pix )
                        pindex = pixel_functions.convert_xy_to_pindex( relpos_pix, im_width )
            
                        if im2shapes_by_pindex[str(pindex)] in im2shapes_in_relpos.keys():
                           im2shapes_in_relpos[ im2shapes_by_pindex[str(pindex)] ] += 1
                        else:
                           im2shapes_in_relpos[ im2shapes_by_pindex[str(pindex)] ] = 1
            
            
                     #image_functions.cr_im_from_pixels( cur_im2file, directory, debug_pixels, save_filepath=None , pixels_rgb=None )

                     
                     for im2shapeid in im2shapes_in_relpos:
                        if im1shapes_colors[ im1shapeid ] != im2shapes_colors[ im2shapeid ] or len( im2shapes[ im2shapeid ] ) < frth_smallest_pixc:
                           continue
               
                        size_diff = size_is_too_diff( im1shapeid, im2shapeid, im1shapes, im2shapes, size_num=1 )
                        if size_diff is True:
                           # size is too different
                           continue        
               
                        if im2shapes_in_relpos[im2shapeid] > len( im2shapes[im2shapeid] ) * 0.6:
                           result_matches[each_files].add( (im1shapeid, im2shapeid) )
                           matched = True
                           break
                  
                        elif im2shapes_in_relpos[im2shapeid] > len( im1shapes[im1shapeid] ) * 0.6:
                           result_matches[each_files].add( (im1shapeid, im2shapeid) )
                           matched = True
                           break

                  


for each_files in result_matches:
      
   if each_files not in all_matches_so_far.keys():
      all_matches_so_far[ each_files ] = result_matches[ each_files ]
      
   else:
      for each_shapes in result_matches[ each_files ]:
         if each_shapes not in all_matches_so_far[ each_files ]:
            all_matches_so_far[ each_files ].add( each_shapes )               



relpos_nbr_ddir = top_shapes_dir + directory + scnd_stg_all_files + "/relpos_nbr/data/"
if os.path.exists(relpos_nbr_ddir ) == False:
   os.makedirs(relpos_nbr_ddir )

relpos_nbr_dfile = relpos_nbr_ddir + "1.data"
if os.path.exists( relpos_nbr_dfile ):
   with open (relpos_nbr_dfile, 'rb') as fp:
      relpos_nbr_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in relpos_nbr_shapes:
      if each_files not in result_matches.keys():
         result_matches[ each_files ] = relpos_nbr_shapes[ each_files ]
      else:
      
         for each_shapes in relpos_nbr_shapes[ each_files ]:
            if each_shapes not in result_matches[ each_files ]:
               result_matches[ each_files ].add( each_shapes )       



with open(relpos_nbr_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()


'''
with open(all_matches_so_far_dfile, 'wb') as fp:
   pickle.dump(all_matches_so_far, fp)
fp.close()
'''















