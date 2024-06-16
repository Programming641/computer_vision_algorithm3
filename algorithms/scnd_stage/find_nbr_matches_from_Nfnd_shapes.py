
from libraries import  cv_globals, pixel_shapes_functions, pixel_functions, image_functions, same_shapes_functions, btwn_amng_files_functions


from PIL import ImageTk, Image
import os, sys
import pickle
import copy
import math
import shutil

from libraries.cv_globals import top_shapes_dir, top_images_dir, internal, scnd_stg_all_files

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

shapes_dir = top_shapes_dir + directory + "shapes/"


def check_shape_size( param_im1shapeid, param_im2shapeid, param_shapes, param_ano_shapes ):
   # check if size is too different
   im1shapes_total = len( param_shapes[param_im1shapeid] )
   im2shapes_total = len( param_ano_shapes[param_im2shapeid] )
      
   im1_2pixels_diff = abs( im1shapes_total - im2shapes_total )
   if im1_2pixels_diff != 0:
      if im1shapes_total > im2shapes_total:
         if im1_2pixels_diff / im2shapes_total > 1:
            return True
      else:
         if im1_2pixels_diff / im1shapes_total > 1:
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

   result_matches[each_files] = set()

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

   boundary_dir = top_shapes_dir + directory + "shapes/boundary/"
   boundary_dfile = boundary_dir + cur_im1file + ".data"
   with open (boundary_dfile, 'rb') as fp:
      im1shapes_boundaries = pickle.load(fp)
   fp.close()



   im1shapes_in_shape_coord = {}
   for shapeid in im1shapes:
      cur_pixels = set()
      
      for temp_p in im1shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im1shapes[shapeid] = cur_pixels   
      im1shapes_in_shape_coord[shapeid] = pixel_shapes_functions.get_shape_pos_in_shp_coord( im1shapes[ shapeid ], im_width, param_shp_type=1 )  


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

   im2shapes_in_shape_coord = {}
   for shapeid in im2shapes:
      cur_pixels = set()
      
      for temp_p in im2shapes[shapeid]:
         xy = pixel_functions.convert_pindex_to_xy( temp_p, im_width )
         
         cur_pixels.add( xy )
      
      im2shapes[shapeid] = cur_pixels  
      im2shapes_in_shape_coord[shapeid] = pixel_shapes_functions.get_shape_pos_in_shp_coord( im2shapes[ shapeid ], im_width, param_shp_type=1 )  
      

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


   for each_shape in acrs_all_files_shapes[each_files]:
      # each_shape -> ('79935', '58671')

      for im1nbr in im1shapes_neighbors[ each_shape[0] ]:
         if len( im1shapes[ im1nbr ] ) < frth_smallest_pixc:
            continue
         
         im1nbr_already_matched = [ temp_shapes for temp_shapes in acrs_all_files_shapes[each_files] if temp_shapes[0] == im1nbr ]
         if len( im1nbr_already_matched ) >= 1:
            continue
         
         # im1nbr not found
         for im2nbr in im2shapes_neighbors[ each_shape[1] ]:
            if len( im2shapes[ im2nbr ] ) < frth_smallest_pixc:
               continue
            
            if min_colors is True:
               if im1shapes_colors[ im1nbr ] != im2shapes_colors[im2nbr]:
                  continue
            else:
               appear_diff = pixel_functions.compute_appearance_difference(im1shapes_colors[ im1nbr ] , im2shapes_colors[im2nbr] )
               if appear_diff is True:
                  # different appearance
                  continue


            size_too_diff = check_shape_size( im1nbr, im2nbr, im1shapes, im2shapes )
            if size_too_diff is True:
               continue                     

            result = pixel_shapes_functions.check_shape_attached_near( im1shapes_boundaries[ each_shape[0] ], im1shapes_boundaries[im1nbr], 
                                                                       im2shapes_boundaries[ each_shape[1] ], im2shapes_boundaries[im2nbr], im1.size )
            if result is not True:
               continue

            im1nbr_shp_coord_xy  = im1shapes_in_shape_coord[ im1nbr ]
            im2nbr_shp_coord_xy = im2shapes_in_shape_coord[ im2nbr ]
                     
            # matching from smaller shape.
            if len( im1shapes[ im1nbr ] ) > len( im2shapes[ im2nbr] ):
               im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2nbr_shp_coord_xy, im2nbr_shp_coord_xy, match_threshold=0.6 )
            else:
               im1im2nbr_match = same_shapes_functions.match_shape_while_moving_it( im2nbr_shp_coord_xy, im2nbr_shp_coord_xy, match_threshold=0.6 )

            if im1im2nbr_match is not True:
               continue           

            result_matches[each_files].add( ( im1nbr, im2nbr ) )




result_dfile = across_all_files_ddir + "nbr_matches.data"
if os.path.exists(result_dfile):
   with open (result_dfile, 'rb') as fp:
      result_shapes = pickle.load(fp)
   fp.close()
   
   for each_files in result_shapes:
      if each_files in result_matches.keys():
         for each_shapes in result_shapes[each_files]:
            if each_shapes not in result_matches[each_files]:
               result_matches[each_files].add( each_shapes )
         
      else:
         result_matches[each_files] = result_shapes[each_files]   





with open(result_dfile, 'wb') as fp:
   pickle.dump(result_matches, fp)
fp.close()















